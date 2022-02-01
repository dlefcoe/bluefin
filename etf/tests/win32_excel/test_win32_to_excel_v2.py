'''
https://stackoverflow.com/questions/11836319/pywin32-and-excel-exception-when-writing-large-quantities-of-data
'''


import win32com.client
from win32com.client import constants as c

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


