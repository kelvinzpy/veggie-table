import cv2
import numpy as np
import keyboard

# various excel-related imports
from xlrd import open_workbook

    

# Opens the provided table with a list of participant's numbers and corresponding video link (in local directory format, i.e. C:\etc\example.mkv)
wb = open_workbook('testsheet.xlsx')
for s in wb.sheets():
    #print 'Sheet:',s.name
    datasheet = []
    for row in range(1,s.nrows): # 1 if headers, 0 if no headers
        col_value = []
        for col in range(2):
            value  = (s.cell(row,col).value)
            try : value = str(int(value))
            except : pass
            col_value.append(value)
        datasheet.append(col_value)
print (datasheet)

for entry in datasheet:
    video = entry[1]
    print ("Now playing", (video))
    entry.append("")
    print (entry[2])
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture(video)
     
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
      print("Error opening video stream or file")
     
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
      ret, frame = cap.read()
      if ret == True:
     
        # Display the resulting frame
        cv2.imshow('Frame',frame)
     
#         # Press A on keyboard to indicate a choice of the left sample on the video
#        if keyboard.KEYDOWN('a'):
#          entry[2] += "0"
#     
        # Press Q on keyboard to exit current video (and move on to the next if there is one)
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break
     
      # Break the loop
      else: 
        break
     
    # When everything done, release the video capture object
    cap.release()
     
    # Closes all the frames
    cv2.destroyAllWindows()
    
    # Prints the recorded result (as a series of 0s and 1s)
    print (entry[2])


