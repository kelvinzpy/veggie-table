import VTbackend as VT
import sys
import pygame

if __name__=='__main__':
    

    
    ''' will probably put this whole thing below in a loop for each video of each subject '''

##################### PROGRAM SETTINGS ##################### 
    inputsheet = 'testsheet.xlsx' # change this to change the name of the excel sheet being used as input (the one with participant number, video link etc.)
    timingsheet = 'testtiming.xlsx' # change this to change the name of the excel sheet that contains frame and timing data (probably will be from MatLab programme)
    outputFile = 'testoutput' # change this to change the name of the output file - it will automatically append the subID and block name to each output file
    outputType = '.csv' # change this to change the type of the output file (.txt or .csv)
##################### PROGRAM SETTINGS #####################    
    
###################### VIDEO SETTINGS ######################
    fullscreen = False # setting this to True means the video window will open in borderless fullscreen
    w = 1920 # change these to change dimensions of window opened for video playback (default/recommended is 1920x1080)
    h = 1080  # only need to set these if (fullscreen = False)
#   *** If the resolution is too small, it may affect video playback clarity
    FastForwardRatio = 5 # change this to make it run x times faster when 'T' is pressed (default 5x speed)
###################### VIDEO SETTINGS #######################

##################### PROGRAM RUNS HERE #####################
    # Converts the provided input excel sheet into a list for interpretation
    datasheet1, datasheet2 = VT.listToUsableData(VT.inputToList(inputsheet))
#    print (datasheet)
    # Opens up the PyGame interactive window
    Window = VT.initScreen(w, h, fullscreen) 
    for i in datasheet1:
        print (i)
    
    print ("")
    
    for j in datasheet2:
        print (j)
    # Plays videos in succession
    for datasheet in [datasheet1, datasheet2]:
        outputData = VT.vidPlayback(Window, datasheet, outputFile, FastForwardRatio)
        outputData, subID, blocktype = VT.semiCompile(outputData)    
                     
        # if program is run to completion (no early terminations):
        VT.fidcheck(outputData) # does a teeny (probably not very useful) fidelity check - check console for any glaring errors it finds
        VT.writefile(outputData, outputFile + "_" + str(subID) + "_" + str(blocktype), outputType) # writes outputs to file and terminates program 
    ''' (don't put any functions after this ^ function) '''
    pygame.quit()
    sys.exit()
##################### PROGRAM ENDS HERE #####################
