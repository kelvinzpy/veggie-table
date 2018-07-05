import VTbackend as VT

if __name__=='__main__':
    
    # Converts excel sheet to list in script
    datasheet = VT.excelToList('testsheet.xlsx')
    outputFile = 'testoutput'

    # Opens up the PyGame interactive window
    windowSurface = VT.initScreen()
    
    try:
        sampleNum = int(VT.inputData(windowSurface))
    except ValueError:
        sampleNum = 0
    
    
    
    for i in range(len(datasheet)):
        VT.vidPlayback(windowSurface, i, datasheet, sampleNum, outputFile)
                         
    # if program is run to completion (no early terminations),
    # print (datasheet)
    VT.fidcheck(datasheet, sampleNum) # do a fidelity check before program ends
    VT.writefile(datasheet, sampleNum, outputFile)


