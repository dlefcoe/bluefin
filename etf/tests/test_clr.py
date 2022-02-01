
import sys
import dotnet
import clr

sys.path.append(r'C:/Program Files (x86)/Bluefin Trading/PubSubExcel')

clr.AddReference(r'C:/Program Files (x86)/Bluefin Trading/PubSubExcel/Bluefin.Servers.PubSub.Excel.dll')

print('dotnet is imported')

dotnet.add_assemblies(r'C:/Program Files (x86)/Bluefin Trading/PubSubExcel')
dotnet.load_assembly(r'Bluefin.Servers.PubSub.Excel')

from Bluefin.Servers.PubSub.Excel import *

rtdPub = ExcelFunctions()
while True:
	choice = raw_input("> ")
	rtdPub.P2PPublish("lon","rick","test",choice)




# import winreg


# x = winreg.ConnectRegistry(None, '44803')


# print(x)




