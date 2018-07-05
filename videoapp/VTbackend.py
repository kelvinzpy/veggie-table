"""
Created on Wed Jul  4 23:14:07 2018

@author: Kelvin Zhou
"""
import cv2
import numpy as np
import pygame # using pygame as the overall GUI! hooray
from pygame.locals import *
import time
import sys
import csv
from xlrd import open_workbook # various excel-related imports


pygame.init()

def initScreen():
    pygame.display.set_caption("Veggie-Table")
    clock = pygame.time.Clock()
    size = [1920, 850] # set these two options to change the size of the opened window (recm. 1920x850)
    windowSurface = pygame.display.set_mode(size, 0, 32)
    windowSurface.fill([0,0,0])
    print ("Please enter the number of expected samples in each video, and press Enter.")
    return windowSurface


# function for writing stuff on the screen
def screenwrite(screen, text, x, y, w, h, size = 45, textcolor = (200, 0, 0), bgcolor = (30, 30, 30), font_type = None): 
    basicfont = pygame.font.SysFont(font_type, 48)
    text = basicfont.render(text, True, textcolor, bgcolor)
    textrect = pygame.Rect(x, y, w, h)
    screen.blit(text, textrect)
    pygame.display.update()
        
#function for indicating (with a green light) when a recording is registered - basically draws little green bar markers to show how many times each side has been chosen
def recordIndicator(screen, x, y, w = 7, h = 40, color = (0, 200, 0)):
    pygame.draw.rect(screen, (0, 200, 0), (x,y,w,h), 0)
    pygame.display.update()
#    overlay = pygame.draw.rect(screen, (30, 30, 30), (0, 800, 1920, 100), 0)

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
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    try:
                        int(self.text)
                        self.num = self.text
                        print("ok, your number is", self.num,"- press ESC to confirm")
                        screenwrite(screen, "press ESC to confirm.", 600, 500, 140, 32, textcolor = pygame.Color('dodgerblue2'))
                        time.sleep(1)
                        pass
                    except ValueError:
                        print("Please type a number.")
                        screenwrite(screen, "Please type a number.", 800, 300, 140, 32)
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
        # Resize the box if the input is too long. (should not be likely)
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
    input_box1 = NumberBox(865, 375, 90, 100)
    input_boxes = [input_box1]
    done = False
    inputNum = 0 # this is the number that is returned when the user enters the number for sample
    screenwrite(screen, "Please enter the number of expected samples in each video, and press Enter.", 200, 400, 140, 32, bgcolor = (0, 0, 0))
    time.sleep(3)
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                for box in input_boxes:
                    inputNum = box.storevalue()
                    return inputNum
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
    inputFood = 'idk' # if no box is selected it will return 'idk' by default (idk being a placeholder that throws up an indicator during final fidelity checks)

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

def vidPlayback(screen, num, datasheet, sampleNum, txtfile):
    

    # initialize data in row num of datasheet
    entry = datasheet[num]
    for j in range(3):
        entry.append("")
    video = entry[1]

    print ("Now playing", (video))
    
    # Create a VideoCapture object and read from provided video link
    cap = cv2.VideoCapture(video)
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
        cv2.flip(frame,1,frame) #for some reason output is mirrored and has to be flipped again (?)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)

        screen.blit(frame, (0,0))
        pygame.display.update()
    
        if selectedLFood == False:
            sampleLFood = selectFood(screen, 100, ["banana", "orange", "idk"])
            print (sampleLFood)
            entry[3] = sampleLFood
            selectedLFood = True
            
        if selectedRFood == False:
            sampleRFood = selectFood(screen, 1600, ["watermelon", "mango", "idk"])
            print (sampleRFood)
            entry[4] = sampleRFood
            selectedRFood = True
        
        for event in pygame.event.get():
            
            # to record a selection of the left sample
            if event.type == KEYDOWN and event.key == K_LEFT:
                print ("LEFT sample choice recorded")
                recordIndicator(screen, (15 + leftcount*13), 805)
                entry[2] += "0"
                leftcount += 1
                pass
            
            # to record a selection of the right sample
            if event.type == KEYDOWN and event.key == K_RIGHT:
                print ("RIGHT sample choice recorded")
                recordIndicator(screen, (1898 - rightcount*13), 805)
                entry[2] += "1"
                rightcount += 1
                pass            
            
            # if terminating video early, will skip to next video
            if event.type == KEYDOWN and event.key == K_ESCAPE and entry[0] != datasheet[-1][0]:
                print ("Skipping to next video")
                pygame.draw.rect(screen, (30, 30, 30), (0, 800, 1920, 100), 0) # resets green bars for both sides
                pygame.display.update()
                running = False
                break
            
            # if terminating video early (last video) - will run fidelity check and end the program
            if event.type == KEYDOWN and event.key == K_ESCAPE and entry[0] == datasheet[-1][0]:
#                print (entry[2])
#                print (datasheet)   
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
    rightLength = 0                 # as the number of times the particpant chose a food
    totalCount = len(datasheet)
    print ("Checking for fidelity...")
    for entry in datasheet:
        if len(entry[2]) == sampleNum:
            rightLength += 1
        if len(entry[2]) != sampleNum:
            print ("ERROR: Entry number", entry[0], "did not have an accurate recorded number of choices (with", len(entry[2]), "instead of", sampleNum,"choices)")
        if entry[3] == "idk" or entry[4] == "idk":
            print ("ERROR: One or more food options for entry", entry[0], "are incomplete. Consider rectifying")
        
    print (rightLength, "entries with the indicated length out of", totalCount, "total entries")
    if sampleNum == 0:
        print ("ERROR: Required number of choices should not be 0 - please recheck")
    if totalCount == rightLength and sampleNum != 0:
        print ("FIDELITY CHECK COMPLETE - no errors! :)")
    if totalCount != rightLength:
        print ("ERROR:", (totalCount - rightLength), "entries out of", totalCount, "did not match provided sample number. Advise restarting")


# function which compiles the generated data into a .csv (technically .txt) file for data collection purposes, then terminates the program
# OPENING THE .TXT FILE IN EXCEL WILL REMOVE LEADING 0s FROM THE RECORDED DATA (e.g. 00010 -> 10). PLEASE USE Data -> Import TXT IN EXCEL AND SELECT THE .TXT FILE MANUALLY.
def writefile(datasheet, sampleNum, txtfile = 'testoutput'):
    headers = ['Participant Number', 'Movie Link', 'Recorded Data', 'Left Food Sample', 'Right Food Sample']
    txtfile += '.txt' # change to '.csv' for a csv file instead
    datasheet.insert(0, headers)
    datasheet[0].append("Number of inputs:" + str(sampleNum))
    done = False

    while not done:
        
        with open(txtfile, "w") as output:
            try:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerows(datasheet)
                done = True
            except PermissionError: # if the .txt file is open on the computer or requires admin privileges to edit
                print ("Please close the file if it is open on your computer. Retrying in 10 seconds")
                time.sleep(10)
                
    print ("Data written to file", txtfile, "- please check for any inaccuracies")
    print ("Make sure to open the .csv file from Excel -> Data -> Import TXT instead of directly through Excel! (See README for clarification.)")
    
    pygame.quit()
    sys.exit()    




