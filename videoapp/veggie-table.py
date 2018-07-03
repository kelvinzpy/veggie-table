import cv2
import numpy as np
import pygame # using pygame as the overall GUI! hooray
from pygame.locals import *
import time
import csv
from xlrd import open_workbook # various excel-related imports

def text_to_screen(screen, text, x, y, size = 50, color = (000, 000, 000), font_type = None):
    
    try:
        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception:
        print ('Font Error, oops :(')
        

# Opens the provided table with a list of participant's numbers and corresponding video link (in local directory format, i.e. C:\etc\example.mkv)
wb = open_workbook('testsheet.xlsx')
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
#print (datasheet)

# Opens up the PyGame interactive window
pygame.init()
pygame.display.set_caption("Video playing on PyGame")

size = [1920, 850] # set these two options to change the size of the opened window (recm. 1920x800)

windowSurface = pygame.display.set_mode(size, 0, 32)
windowSurface.fill([0,0,0])
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class NumberBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_ACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = True
        self.num = ''

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    try:
                        int(self.text)
                        self.num = self.text
                        print("ok, your number is", self.num,"- press ESC to confirm")
                        pass
                    except ValueError:
                        print("Please type a number.")
                        text_to_screen(windowSurface, "Please type a number.", 100, 200) # this doesn't work!!!
                        self.text = "Please type a number." # why doesn't this work :<
                        time.sleep(1)

                        self.text = "0"
                        
                    if int(self.text) > 0:
                        self.num = self.text
                        return self.num
#                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        
    def storevalue(self):
        self.num = self.text
        return self.num

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def inputdata():
    clock = pygame.time.Clock()
    input_box1 = NumberBox(900, 450, 140, 32)
#    input_box2 = NumberBox(100, 300, 140, 32)
    input_boxes = [input_box1]
    done = False
    inputNum = '0' # this is the number that is returned when the user enters the number for sample

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                for box in input_boxes:
                    inputNum = box.storevalue()
#                    print ("the input for", box, "is", inputNum)
                    return inputNum
                done = True
            for box in input_boxes:
                box.handle_event(event)
                
        for box in input_boxes:
            box.update()

        windowSurface.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(windowSurface)

        pygame.display.flip()
        clock.tick(30)


# function which includes final checks on obtained recordings and terminates the program
def fidcheck(datasheet, sampleNum): # where datasheet is the end-product excel table (with 1's and 0's),  
                                    # and sampleNum is the initial number provided at the start 
    rightLength = 0                 # as the number of times the particpant chose a food)
    totalCount = len(datasheet)
    print ("Checking for fidelity...")
    for entry in datasheet:
        if len(entry[2]) == sampleNum:
            rightLength += 1
        else:
            print ("Entry number", entry[0], "did not have an accurate recorded number of choices (with", len(entry[2]), "instead of", sampleNum,"choices)")
            
    print (rightLength, "entries with the proper length out of", totalCount, "total entries")
    if totalCount == 0:
        print ("Required number of choices should not be 0 - please recheck")
    if totalCount == rightLength and totalCount != 0:
        print ("Fidelity check complete, no errors")
    if totalCount != rightLength:
        print ((totalCount - rightLength), "entries out of", totalCount, "did not match provided sample number. Advise restarting")


# function which compiles the generated data into a .csv file for data collection purposes, then terminates the program
# OPENING THE .CSV FILE IN EXCEL WILL REMOVE LEADING 0s FROM THE RECORDED DATA (e.g. 00010 -> 10). PLEASE USE Data -> Import Data IN EXCEL AND SELECT THE .CSV FILE MANUALLY.
def writefile(datasheet):
    headers = ['Participant Number', 'Movie Link', 'Recorded Data']
    csvfile = "testsheetv2.txt"
    datasheet.insert(0, headers)
#    for entry in datasheet:
#        if entry[2][0] == '0':
#            entry[2] = ("'" + entry[2]) # this is to prevent e.g. '0010' from showing up as '10' on the .csv file
    with open(csvfile, "w") as output:
        try:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(datasheet)
        except PermissionError: # if the .csv file is open on the computer or requires admin privileges to edit
            print ("Please close the file if it is open on your computer.")
            pass
    print ("Data written to file", csvfile, "- please check for any inaccuracies")
    print ("Make sure to open the .csv file from Excel -> Data -> Import Data instead of directly through Excel!")
    
    pygame.quit()
#    print (datasheet)
    exit()    


try:
    sampleNum = int(inputdata())
except ValueError:
    sampleNum = 0

for entry in datasheet:
    video = entry[1]
    print ("Now playing", (video))
    entry.append("")
    print (entry[2])
    
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(video)
    running = True 

    while running:
        
      # Capture frame-by-frame
      ret, frame = cap.read()
      if ret == True:
     
        # Display the resulting frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.flip(frame,1,frame) #for some reason output is mirrored and has to be flipped again (?)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        windowSurface.blit(frame, (0,0))
        pygame.display.update()

        for event in pygame.event.get():
            # to record a selection of the right sample
            if event.type == KEYDOWN and event.key == K_RIGHT:
                print ("RIGHT sample choice recorded")
                entry[2] += "1"
                pass
            
            # to record a selection of the left sample
            if event.type == KEYDOWN and event.key == K_LEFT:
                print ("LEFT sample choice recorded")
                entry[2] += "0"
                pass
            
            # if terminating video early
            if event.type == KEYDOWN and event.key == K_ESCAPE and entry[0] != datasheet[-1][0]:
                print ("Skipping to next video")
                running = False
                break
            
            # if terminating video early (last video)
            if event.type == KEYDOWN and event.key == K_ESCAPE and entry[0] == datasheet[-1][0]:
                print (entry[2])
                print (datasheet) 
                fidcheck(datasheet, sampleNum) # do a fidelity check before terminating the program
                writefile(datasheet)
                break
            
      # Break the loop
      else: 
        break
     
    # When everything done, release the video capture object
    cap.release()
     
    # Closes all the frames
    cv2.destroyAllWindows()
    
    # Prints the recorded result (as a series of 0s and 1s)
    # print (entry[2])


# if program is run to completion (no early terminations)
# print (datasheet)
fidcheck(datasheet, sampleNum) # do a fidelity check before program ends
writefile(datasheet)


