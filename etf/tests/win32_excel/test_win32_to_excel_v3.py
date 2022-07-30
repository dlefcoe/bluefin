'''
https://pythonexcels.com/python/2009/10/05/python-excel-mini-cookbook

https://stackoverflow.com/questions/11836319/pywin32-and-excel-exception-when-writing-large-quantities-of-data

'''

import random
import win32com.client

xl = win32com.client.gencache.EnsureDispatch("Excel.Application")
xl.Interactive = True
xl.Visible = True

my_excel_file = r'Y:\DL_trade\code\python\tests\test_excel_rtd.xlsx'

# Workbook = xl.Workbooks.Add()
Workbook = xl.Workbooks.Open(my_excel_file)
Sheets = Workbook.Sheets

Sheets(1).Cells(1,2).Value = "Test"
Sheets(1).Cells(2,2).Value = "darren"

print(Sheets(1).Cells(1,2).Value)

# write a cell
Sheets(2).Cells(1,2).Value = ["xxx","best"]
# write a row
Sheets(2).Range("b1:c1").Value = ["xxx","yyy"]
# write a column

for j in range(100):
    for i in range(10):
        range_entry = 'd'+str(i+1)
        print('range entry: ' + range_entry)
        print(type(range_entry))
        some_string = 'hello world ' + str(random.randint(1 , 1000) )
        Sheets(2).Range(range_entry).Value = some_string

        Sheets(3).Cells(i+1,j+1).Value = some_string



# xl.Application.Quit()

