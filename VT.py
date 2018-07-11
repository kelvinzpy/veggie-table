import VTbackend as VT

if __name__=='__main__':
    
##################### PROGRAM SETTINGS ##################### 
    inputsheet = 'testsheet.xlsx' # change this to change the name of the excel sheet being used as input (the one with participant number, video link etc.)
    outputFile = 'testoutput' # change this to change the name of the output file
    outputType = '.txt' # change this to change the type of the output file (.txt or .csv)
    
    LFoodList = ["banana", "orange", "idk"] # change the entries in these lists to change the possible foods that L/R side could be
    RFoodList = ["watermelon", "mango", "idk"] 
##################### PROGRAM SETTINGS #####################    
    
###################### VIDEO SETTINGS ######################
    fullscreen = True # setting this to True means the video window will open in borderless fullscreen
    w = 1920 # change these to change dimensions of window opened for video playback (default/recommended is 1920x850)
    h = 850  # only need to set these if (fullscreen = False)
#   *** If the resolution is too small, it may affect video playback clarity
###################### VIDEO SETTINGS #######################

##################### PROGRAM RUNS HERE #####################
    # Converts the provided input excel sheet into a list for interpretation
    datasheet = VT.excelToList(inputsheet)
    # Opens up the PyGame interactive window
    Window = VT.initScreen(w, h, fullscreen) 
    
    # Receives input data for intended sample number (default is 0 and will hence need manual modifying afterwards if number is not set)
    sampleNum = VT.initSampleNum(Window)
        
    # Plays videos in succession
    for i in range(len(datasheet)):
        VT.vidPlayback(Window, i, datasheet, LFoodList, RFoodList, sampleNum, outputFile)
                         
    # if program is run to completion (no early terminations):
    VT.fidcheck(datasheet, sampleNum) # does a fidelity check before program ends - check console for any errors
    VT.writefile(datasheet, sampleNum, outputFile, outputType) # writes outputs to file and terminates program
##################### PROGRAM ENDS HERE #####################
