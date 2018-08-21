from xlrd import open_workbook # various excel-related imports
import time

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

datasheet = inputToList("testsheet.xlsx")

usabledatasheet = listToUsableData(datasheet)

#print (listToUsableData(test))
#for item in listToUsableData(test):
#    print (item)
#
#for i in listToUsableData(test)[-1]:
#    print (i)
#    
#trialWinLoss = []
#for item in listToUsableData(test)[-1]:
#    trialWinLoss.append((item[0], item[-1]))
#print (trialWinLoss[0][1])


#x = [1, 2, 3, "", "", ""]
#print (x)

count = 0
lista = []
while True:
    time.sleep(1)
    count += 1
    
    if count % 10 == 0:
        lista.append(banana)
        
        banana = count
        
        
        
    
    
    
    