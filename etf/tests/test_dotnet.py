
import sys
import dotnet

# sys.path.append(r'C:/Program Files (x86)/Bluefin Trading/PubSubExcel')


print('dotnet is imported')

folder_to_point = r'C:/Program Files (x86)/Bluefin Trading/PubSubExcel'
folder_to_point = r'Y:/Useful Code/PubSubRTDWrapper'
file_name = r'Bluefin.Servers.PubSub.Excel'

dotnet.add_assemblies(folder_to_point)
dotnet.load_assembly(file_name)


from Bluefin.Servers.PubSub.Excel import *

print('got here')


rtdPub = ExcelFunctions()
while True:
	choice = raw_input("> ")
	rtdPub.P2PPublish("lon","rick","test",choice)




# import winreg


# x = winreg.ConnectRegistry(None, '44803')


# print(x)




