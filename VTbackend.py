"""
Created on Wed Jul  4 23:14:07 2018

@author: Kelvin Zhou
"""
import cv2
import numpy as np
import pygame # using pygame as the overall GUI
from pygame.locals import *
import time
import sys
import csv
from xlrd import open_workbook # various excel-related imports


pygame.init()

def initScreen(w = 1920, h = 850, fullscreen = True):
    pygame.display.set_caption("Veggie-Table")
    if fullscreen == False:   
        size = [w, h]
        windowSurface = pygame.display.set_mode(size, 0, 32)
    else:
        windowSurface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        w, h = pygame.display.Info().current_w, pygame.display.Info().current_h # if fullscreen, sets w and h to resolution of the current screen
        
    global windowW
    global windowH
    windowW, windowH = int(w), int(h)
    
    windowSurface.fill((30,30,30))
    pygame.display.update()
    print ("Please enter the number of expected samples in each video, and press Enter.")
    return windowSurface


# function for writing stuff on the screen - text is centralized
def screenwrite(screen, text, y, size = 45, textcolor = (200, 0, 0), bgcolor = (30, 30, 30), font_type = None): 
    basicfont = pygame.font.SysFont(font_type, 48)
    text = basicfont.render(text, True, textcolor, bgcolor)
    textrect = text.get_rect(center=(windowW/2, (y+24)))
    screen.blit(text, textrect)
    pygame.display.update()
        
#function for indicating (with a green light) when a recording is registered - basically draws little green bar markers to show how many times each side has been chosen
def recordIndicator(screen, x, y, w = 7, h = 40, color = (0, 200, 0)):
    pygame.draw.rect(screen, (0, 200, 0), (x,y,w,h), 0)
    pygame.display.update()
    
# Opens the provided table with a list of participant's numbers and corresponding video link (in local directory format, i.e. C:\etc\example.mkv)
def inputToList(file):
    column_number = 12 # number of columns in the file
    wb = open_workbook(file)
    for s in wb.sheets():
        datasheet = []
        for row in range(1,s.nrows): # 1 if headers, 0 if no headers
            col_value = []
            for col in range(column_number):
                value  = (s.cell(row,col).value)
                try : value = int(value)
                except : pass
                col_value.append(value)
            datasheet.append(col_value)
        return datasheet


# this converts the datasheet into a form more suitable for manipulation.
        # 1st item: subject ID (e.g. 996)
        # 2nd item: link to video
        # 3rd item: identity of sweet food
        # 4th item: identity of salty food
        # 5th item: boolean for if sweet food is on the left
        # 6th item: iterated list of lists of data for each trial, arranged in order of trial (so each trial has a corresponding list of data):
            # 1st entry: trial number (1, 2, 3 etc.)
            # 2nd entry: block item in text (e.g. money, food)
            # 3rd entry: block item's ID number
            # 4th entry: frame number on which reward feedback time begins --> this is used for checking if the current trial playing in the video was a win or a loss
            # 5th entry: colour of the feedback state in text (e.g. orange, blue)
            # 6th entry: feedback state colour's ID number
            # 7th entry: if the trial was a win or a loss
def listToUsableData(datasheet):
    datasheet[0].insert(0,"")
    subID = datasheet[0][1]
    videoLink = datasheet[0][2]
    sweetFood = datasheet[0][3]
    saltFood = datasheet[0][4]
    isSweetLeft = datasheet[0][5]
    variableData = []
    for entry in range(len(datasheet)):
        entryData = []
        for i in range(-7, 0):
            entryData.append(datasheet[entry][i])
        entryData[2], entryData[0] = entryData[0], entryData[2]
        entryData[4], entryData[5] = entryData[5], entryData[4]
        variableData.append(entryData)
    datasheet = [subID, videoLink, sweetFood, saltFood, isSweetLeft, variableData]
    return datasheet
    
    
# Opens frame/timing data from the MatLab programme to index the video into multiple trials
def timingToList(file):
    column_number = 4 # number of columns in the file
    wb = open_workbook(file)
    for s in wb.sheets():
        timingsheet = []
        for row in range(1,s.nrows): # 1 if headers, 0 if no headers
            col_value = []
            for col in range(column_number):
                value  = (s.cell(row,col).value)
#                try : value = str(float(value))
#                except : pass
                col_value.append(value)
            timingsheet.append(col_value)
    return timingsheet


class NumberBox:
    
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dodgerblue2')
        self.text = text
        self.txt_surface = pygame.font.Font(None, 100).render(text, True, self.color)
        self.active = True
        self.num = ''

    def handle_event(self, event, screen):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    try:
                        int(self.text)
                        self.num = self.text
                        print("ok, your number is", self.num,"- press ESC to confirm")
                        screenwrite(screen, str("Press ESC to confirm that your number is " + str(self.num)),(windowH/2 + 70), textcolor = pygame.Color('dodgerblue2'))
                        time.sleep(1)
                        pass
                    except ValueError:
                        print("Please type a number.")
                        screenwrite(screen, "Please type a number.", (windowH/2 - 120))
                        time.sleep(1)
                        self.text = "0"
                        
                    if int(self.text) > 0:
                        self.num = self.text
                        return self.num
                    
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(None, 100).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the input number is too long. (should not be likely)
        width = max(100, self.txt_surface.get_width()+10)
        self.rect.w = width
        
    def storevalue(self):
        self.num = self.text
        return self.num

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def inputData(screen):
    
    clock = pygame.time.Clock()
    input_box1 = NumberBox((windowW/2 - 45), (windowH/2 - 45), 90, 90)
    input_boxes = [input_box1]
    done = False
    finished_reading_message = False
    inputNum = 0 # this is the number that is returned when the user enters the number for sample
    screenwrite(screen, "Please enter the number of expected samples in each video, and press Enter.", (windowH/2 - 25), bgcolor = (30, 30, 30))
    screenwrite(screen, "(Press any key or click to continue.)", (windowH/2 + 25), bgcolor = (30, 30, 30))

    while not finished_reading_message:
        for event in pygame.event.get():
                if event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    finished_reading_message = True
                else:
                    pass
    while not done:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                for box in input_boxes:
                    inputNum = box.storevalue()
                    return inputNum
            if event.type == pygame.QUIT:
                sys.exit() # terminates the program early if 'X' button is pressed
                done = True
            for box in input_boxes:
                box.handle_event(event, screen)
                
        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def initSampleNum(screen):
    try:
        sampleNum = int(inputData(screen))
    except ValueError:
        sampleNum = 0
        print ("invalid input, sample number set to 0")
    return sampleNum

class FoodBox:

    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (142,229,238)
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, (255, 255, 255))
        self.active = False
        self.num = ''

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the box.
            self.color = (0,0,238) if self.active else (142,229,238)
        if self.active:
            return self.text

    def storevalue(self):
        self.num = self.text
        return self.num

    def draw(self, screen):
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect
        pygame.draw.rect(screen, self.color, self.rect, 4)

def selectFood(screen, x, foodlist): # x = 100 for left column, x = 1600 for right column
    clock = pygame.time.Clock()
    input_boxes = []
    for j in range(len(foodlist)):
        input_boxes.append(FoodBox(x, 200 + 60*j, 140, 32, foodlist[j]))
    done = False
    inputFood = 'idk' # if no box is selected it will return 'idk' by default ('idk' being a placeholder that throws up an indicator during final fidelity checks)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == KEYDOWN and event.key == K_RETURN):
                for box in input_boxes:
                    if box.active:
                        inputFood = box.storevalue()
#                        print ("the selection for the food is", inputNum)
                if inputFood == None:
                    inputFood = "idk"
                return inputFood
                done = True
            for box in input_boxes:
                box.handle_event(event)

#        windowSurface.fill((30, 30, 30, 0)) 
        for box in input_boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)

# draws a green banner on top part of screen if the trial is indicated as a win, red banner if trial is indicated as loss
def winlossBanner(screen, win):
    if win == 1:
        pygame.draw.rect(screen, (0, 200, 0), (0,0,windowW,200), 0)
    elif win == 0:
        pygame.draw.rect(screen, (200, 0, 0), (0,0,windowW,200), 0)
    pygame.display.update()

def checkWin():
    ''' forgot what I was supposed to do here'''

def vidPlayback(screen, datasheet, LFoodList, RFoodList, sampleNum, txtfile, trialnum = 10):

    overlay = pygame.draw.rect(screen, (30, 30, 30), (0,0,windowW,windowH), 0) # call this to reset the screen
    
    subID = datasheet[0]
    video = datasheet[1]
    sweetFood = datasheet[2]
    saltFood = datasheet[3]
    isSweetLeft = datasheet[4]
    trialData = datasheet[5]
    allIndexes = [] # list of all frame numbers where reward feedback becomes active
    for item in trialData:
        allIndexes.append(item[3])
    trialWinLoss = [] # list of tuples in the format --> ("trial number", "1 if win and 0 if loss")
    for item in trialData:
        trialWinLoss.append((item[0], item[-1]))

    outputData = []
    for i in range(len(allIndexes)):
        outputData.append("")

    print ("Now playing video of subject number", subID)
    overlay
    
    # Create a VideoCapture object and read from provided video link
    cap = cv2.VideoCapture(video)
    
    videowidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # constants that determine dimensions of video playing
    videoheight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if (windowW - videowidth) <= 0:
        leftborder = 0
        rightborder = windowW
    else:
        leftborder = (windowW - videowidth)/2 # the x-value of the left border of the video
        rightborder = (windowW - (windowW - videowidth)/2) # the x-value of the right border of the video
    clock = pygame.time.Clock()
    running = True 
    leftcount = 0
    rightcount = 0
    selectedLFood = False
    selectedRFood = False
    framecount = 0
    #                     0      1       2          3           4       5  6  7  8  9  10 11   12      13   14   15    16   17
    defaultOutputRow = [subID, video, sweetFood, saltFood, isSweetLeft, 0, "","","","","","", "NaN", "NaN",  0 , 0 , "NaN", ""]

    while running:
      # Capture frame-by-frame
      clock.tick(30) # determines the FPS of the playing video. Highly discourage changing as this is tied to a bunch of other input data that assumes 30fps
      ret, frame = cap.read()
      
      if framecount in allIndexes: # i.e. if the video has reached the point where feedback state has become active for the previous trial
          
          pygame.draw.rect(screen, (30, 30, 30), (0,(windowH - 150),windowW,150), 0)
          pygame.display.update()
          
          index = allIndexes.index(framecount)
          relevantTrial = trialWinLoss[index]
          trialnum = relevantTrial[0]
          isWin = relevantTrial[1]
          winlossBanner(screen, isWin)
          screenwrite(screen, "END OF TRIAL #"+str(trialnum), 20, textcolor = (255,255,255))
          pygame.display.update()
          
          
          
          print ("the current row is:", defaultOutputRow)
          print ()
          
          for item in outputData:
              print (item)
          
          trialnumber = trialData[index][0]
          blockText = trialData[index][1]
          blockID = trialData[index][2]
          feedbackFrame = trialData[index][3]
          feedbackColor = trialData[index][4]
          feedbackID = trialData[index][5]  
          winloss = trialData[index][6]
          
          defaultOutputRow[5], defaultOutputRow[6], defaultOutputRow[7], defaultOutputRow[8], defaultOutputRow[9], defaultOutputRow[10], defaultOutputRow[11] = trialnumber, feedbackFrame, blockText, blockID, feedbackID, feedbackColor, winloss
          # ^ this is more spaghetti code than a tech start-up in Rome
          
''' WHY DOES THE CODE ABOVE CHANGE ALL THE EXISTING ROWS INSTEAD OF ONLY THE LAST ONE??????????????????????????????? '''

          print ()
          for item in outputData:
              print (item)

          '''
          FORMAT OF OUTPUT DATA (in order as they appear in the list):
              0 - subject ID
              1 - video link
              2 - sweet food (in text)
              3 - salty food (in text)
              4 - binary 1/0 for whether sweet food is on the left
              5 - trial number
              6 - frame on which reward feedback begins
              7 - block text
              8 - block ID number
              9 - feedback state ID
              10 - feedback state color
              11 - if trial was win/loss
              12 - unicode number of key pressed by coder
              13 - key pressed by coder
              14 - coder error? 1/0
              15 - subject error? 1/0 (as observed by coder)
              16 - subject win AND if he chose left (1 if win + left, 0 if win + right, NaN otherwise)
              17 - result (in text) (e.g. left, right, subject error, coder error)
          '''
          
          if defaultOutputRow[11] == 1:
              defaultOutputRow[17] = "error_sub"
          if defaultOutputRow[11] == 0:
              defaultOutputRow[17] = "loss"

      if ret == True:
     
        # Display the resulting frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.flip(frame,1,frame) # for some reason output is mirrored and has to be flipped again (?)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)

        screen.blit(frame, (((windowW - videowidth)/2),100))
        pygame.display.update()
    
        # These two if statements ensure that a food is chosen for both left and right samples per video
        if selectedLFood == False:
            sampleLFood = selectFood(screen, min(100, windowW/15), LFoodList)
            print ("You chose:", sampleLFood)
#            entry[2] = sampleLFood
            selectedLFood = True
            
        if selectedRFood == False:
            sampleRFood = selectFood(screen, min((windowW - 100 - 140), windowW*14/15), RFoodList)
            print ("You chose:", sampleRFood)
#            entry[3] = sampleRFood
            selectedRFood = True
            
        
        for event in pygame.event.get():
            
            # to record a selection of the left sample
            if event.type == KEYDOWN and event.key == K_c:
#                print ("LEFT sample choice recorded")
#                recordIndicator(screen, (leftborder + 2 + leftcount*13), min((videoheight + 105), (windowH - 45)))
#                entry[4] += "0"
#                leftcount += 1
                
                ''' draw some indicator that 'left' was pressed ''' 
                pygame.draw.rect(screen, (30, 30, 30), (0,(windowH - 150),windowW,150), 0)
                pygame.draw.rect(screen, (0, 200, 0), (0,(windowH - 150),700,150), 0)
                pygame.display.update()
                
                if defaultOutputRow[11] == 1:
                    defaultOutputRow[12] = 67
                    defaultOutputRow[13] = "c"
                    defaultOutputRow[14] = 0
                    defaultOutputRow[15] = 0
                    defaultOutputRow[16] = 1
                    defaultOutputRow[17] = "left"
                if defaultOutputRow[11] == 0:
                    defaultOutputRow[12] = 67
                    defaultOutputRow[13] = "c"
                    defaultOutputRow[14] = 0
                    defaultOutputRow[15] = 1
                    defaultOutputRow[16] = "NaN"
                    defaultOutputRow[17] = "error_sub"
                pass
            
            # to record a selection of the right sample
            if event.type == KEYDOWN and event.key == K_m:
#                print ("RIGHT sample choice recorded")
#                recordIndicator(screen, (rightborder - 9 - rightcount*13), min((videoheight + 105), (windowH - 45)))
#                entry[4] += "1"
#                rightcount += 1

                ''' draw some indicator that 'right' was pressed '''                
                pygame.draw.rect(screen, (30, 30, 30), (0,(windowH - 150),windowW,150), 0)
                pygame.draw.rect(screen, (0, 200, 0), (windowW,(windowH - 150),-700,150), 0)
                pygame.display.update()

                if defaultOutputRow[11] == 1:
                    defaultOutputRow[12] = 77
                    defaultOutputRow[13] = "m"
                    defaultOutputRow[14] = 0
                    defaultOutputRow[15] = 0
                    defaultOutputRow[16] = 0
                    defaultOutputRow[17] = "right"
                if defaultOutputRow[11] == 0:
                    defaultOutputRow[12] = 77
                    defaultOutputRow[13] = "m"
                    defaultOutputRow[14] = 0
                    defaultOutputRow[15] = 1
                    defaultOutputRow[16] = "NaN"
                    defaultOutputRow[17] = "error_sub"
                pass            
            
            
            if event.type == KEYDOWN and event.key == K_SPACE:
                
                ''' draw some indicator that 'space' was pressed, i.e. 'the subject has not chosen anything' or 'the coder accidentally pressed C/M and wants to takesiesbacksies' ''' 
                pygame.draw.rect(screen, (30, 30, 30), (0,(windowH - 150),windowW,150), 0)
                pygame.display.update()


                if defaultOutputRow[11] == 1:
                    defaultOutputRow[12] = "NaN"
                    defaultOutputRow[13] = "NaN"
                    defaultOutputRow[14] = 0
                    defaultOutputRow[15] = 1
                    defaultOutputRow[16] = "NaN"
                    defaultOutputRow[17] = "error_sub"
                if defaultOutputRow[11] == 0:
                    defaultOutputRow[12] = "NaN"
                    defaultOutputRow[13] = "NaN"
                    defaultOutputRow[14] = 0
                    defaultOutputRow[15] = 0
                    defaultOutputRow[16] = "NaN"
                    defaultOutputRow[17] = "loss"
                pass
            
            if event.type == KEYDOWN and event.key == K_k:
                print (defaultOutputRow)
            
            
            # if terminating video early, will skip to next video
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                print ("Skipping to next subject")
                running = False
                break
            
        framecount += 1
#        print (framecount)
        if framecount in allIndexes:
            try:
                outputData[index] = defaultOutputRow
            except UnboundLocalError:
                pass
            
      # Break the loop
      else: 
          break
    
    # When everything done, release the video capture object
    cap.release()
    
    print (outputData)
     
    # Closes all the frames
    cv2.destroyAllWindows()
    return outputData


# TO REVISE
'''
# function which includes final checks on obtained recordings and terminates the program
def fidcheck(datasheet, sampleNum): # where datasheet is the end-product excel table (with 1's and 0's),  
                                    # and sampleNum is the initial number provided at the start 
    rightLength = 0                 # as the number of times the participant chose a food
    totalCount = len(datasheet)

    print ("Checking for fidelity...")
    for entry in datasheet:
        choiceNumber = entry[4]         # Number of inputs made during each entry
        if len(choiceNumber) == sampleNum:
            rightLength += 1
        if len(choiceNumber) != sampleNum:
            print ("ERROR: Entry number", entry[0], "did not have an accurate recorded number of choices (with", len(choiceNumber), "instead of", sampleNum,"choices)")
        if entry[2] == "idk" or entry[3] == "idk":
            print ("ERROR: One or more food options for entry", entry[0], "are incomplete. Consider rectifying")
        
    print (rightLength, "entries with the indicated length out of", totalCount, "total entries")
    if sampleNum == 0: # if the expected number of samples was not set in the beginning, or set to 0
        print ("ERROR: Required number of choices should not be 0 - please recheck")
    if totalCount == rightLength and sampleNum != 0: # if inputs during all videos matched the expected number, and sample number was not 0 -> successful fidelity check
        print ("FIDELITY CHECK COMPLETE - all entries matched the expected number of samples! :)")
    if totalCount != rightLength:
        print ("ERROR:", (totalCount - rightLength), "entries out of", totalCount, "did not match provided sample number. Advise restarting")
'''

# function which compiles the generated data into a .csv (technically .txt) file for data collection purposes, then terminates the program
# OPENING THE .TXT FILE IN EXCEL WILL REMOVE LEADING 0s FROM THE RECORDED DATA (e.g. 00010 -> 10). PLEASE USE Data -> Import TXT IN EXCEL AND SELECT THE .TXT FILE MANUALLY. (see README)
def writefile(outputData, file = 'testoutput', filetype = '.txt'):  # change filetype to '.csv' for a csv file instead
    headers = ['subID', 'video_link', 'food_text_sweet', 'food_text_salt', 'sweet_loc_left', 'trial_num', 'reward_feedback_on', 'blockText', 'blockID', 'feedback_state', 'feedback_state_color', 'trial_win',	'code_numeric',	'code_keypress', 'coder_error', 'sub_error', 'choose_left', 'code_text']
    file += filetype
    outputData.insert(0, headers)
    done = False
    while not done:
        
        
        try:
            with open(file, "w") as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerows(outputData)
                done = True
        except PermissionError: # if the .txt file is open on the computer or requires admin privileges to edit
            print ("Please close the file if it is open on your computer. Retrying in 10 seconds")
            time.sleep(10)
                
    print ("Data written to file", file, "- please check for any inaccuracies")
    print ("Make sure to open the .csv file from Excel -> Data -> Import TXT instead of directly through Excel! (See README for clarification.)")
    print ("Program shutting down in 5 seconds...")
    pygame.quit()
    sys.exit()    




