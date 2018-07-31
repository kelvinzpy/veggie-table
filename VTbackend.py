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

def excelToList(file):
    wb = open_workbook(file)
    for s in wb.sheets():
        datasheet = []
        for row in range(1,s.nrows): # 1 if headers, 0 if no headers
            col_value = []
            for col in range(2):
                value  = (s.cell(row,col).value)
                try : value = str(int(value))
                except : pass
                col_value.append(value)
            datasheet.append(col_value)
    return datasheet

# Opens frame/timing data from the MatLab programme to index the video into multiple trials
def timingToList(file):
    wb = open_workbook(file)
    for s in wb.sheets():
        timingsheet = []
        for row in range(1,s.nrows): # 1 if headers, 0 if no headers
            col_value = []
            for col in range(4):
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
        input_boxes.append(FoodBox(x, 60 + 60*j, 140, 32, foodlist[j]))
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
    if win == True:
        pygame.draw.rect(screen, (0, 200, 0), (0,0,9999,100), 0)
    elif win == False:
        pygame.draw.rect(screen, (200, 0, 0), (0,0,9999,100), 0)
    pygame.display.update()

def vidPlayback(screen, trialnum = 15, partnum, datasheet, LFoodList, RFoodList, sampleNum, txtfile):

    overlay = screen.fill((30, 30, 30)) # call this to reset the screen
    
    # initialize data in row partnum of datasheet
    entry = datasheet[partnum]
    for j in range(trialnum):
        entry.append("")
    video = entry[1]

    print ("Now playing", (video))
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
    
    while running:
      # Capture frame-by-frame
      clock.tick(30) # determines the FPS of the playing video, try changing if there are issues e.g. if playback speed is weird
      ret, frame = cap.read()
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
            entry[2] = sampleLFood
            selectedLFood = True
            
        if selectedRFood == False:
            sampleRFood = selectFood(screen, min((windowW - 100 - 140), windowW*14/15), RFoodList)
            print ("You chose:", sampleRFood)
            entry[3] = sampleRFood
            selectedRFood = True
            
        
        for event in pygame.event.get():
            
            # to record a selection of the left sample
            if (event.type == KEYDOWN and event.key == K_LEFT) or (event.type == KEYDOWN and event.key == K_a):
                print ("LEFT sample choice recorded")
                recordIndicator(screen, (leftborder + 2 + leftcount*13), min((videoheight + 105), (windowH - 45)))
                entry[4] += "0"
                leftcount += 1
                pass
            
            # to record a selection of the right sample
            if event.type == KEYDOWN and event.key == K_RIGHT or (event.type == KEYDOWN and event.key == K_d):
                print ("RIGHT sample choice recorded")
                recordIndicator(screen, (rightborder - 9 - rightcount*13), min((videoheight + 105), (windowH - 45)))
                entry[4] += "1"
                rightcount += 1
                pass            
            
            # if terminating video early, will skip to next video
            if event.type == KEYDOWN and event.key == K_ESCAPE and entry[0] != datasheet[-1][0]:
                print ("Skipping to next video")
                overlay
                pygame.display.update()
                running = False
                break
            
            # if terminating video early (last video) - will run fidelity check and end the program
            if event.type == KEYDOWN and event.key == K_ESCAPE and entry[0] == datasheet[-1][0]:
                fidcheck(datasheet, sampleNum) # do a fidelity check before terminating the program
                writefile(datasheet, sampleNum, txtfile)
                break

      # Break the loop
      else: 
        break
    
    # When everything done, release the video capture object
    cap.release()
     
    # Closes all the frames
    cv2.destroyAllWindows()

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


# function which compiles the generated data into a .csv (technically .txt) file for data collection purposes, then terminates the program
# OPENING THE .TXT FILE IN EXCEL WILL REMOVE LEADING 0s FROM THE RECORDED DATA (e.g. 00010 -> 10). PLEASE USE Data -> Import TXT IN EXCEL AND SELECT THE .TXT FILE MANUALLY. (see README)
def writefile(datasheet, sampleNum, file = 'testoutput', filetype = '.txt'):  # change filetype to '.csv' for a csv file instead
    headers = ['Participant Number', 'Movie Link', 'Recorded Data', 'Left Food Sample', 'Right Food Sample']
    file += filetype
    datasheet.insert(0, headers)
    datasheet[0].append("Number of inputs:" + str(sampleNum))
    done = False

    while not done:
        
        with open(file, "w") as output:
            try:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerows(datasheet)
                done = True
            except PermissionError: # if the .txt file is open on the computer or requires admin privileges to edit
                print ("Please close the file if it is open on your computer. Retrying in 10 seconds")
                time.sleep(10)
                
    print ("Data written to file", file, "- please check for any inaccuracies")
    print ("Make sure to open the .csv file from Excel -> Data -> Import TXT instead of directly through Excel! (See README for clarification.)")
    print ("Program shutting down in 5 seconds...")
    pygame.quit()
    sys.exit()    




