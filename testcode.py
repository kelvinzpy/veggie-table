from xlrd import open_workbook # various excel-related imports

def inputToList(file):
    wb = open_workbook(file)
    for s in wb.sheets():
        datasheet = []
        for row in range(1,s.nrows): # 1 if headers, 0 if no headers
            col_value = []
            for col in range(12):
                value  = (s.cell(row,col).value)
                try : value = str(int(value))
                except : pass
                col_value.append(value)
            datasheet.append(col_value)
        return datasheet

datasheet = inputToList("testsheet.xlsx")
print (datasheet)