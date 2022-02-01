
import sys
import dotnet
import ctypes


print('dotnet is imported')

dll_path = r'Y:/Useful Code/PubSubRTDWrapper'
dll_file = r'Bluefin.Servers.PubSub.Excel.dll'
dll_path_and_file = dll_path + '/' + dll_file


# method 1
# sys.path.append(r'C:/Program Files (x86)/Bluefin Trading/PubSubExcel')
my_dll = ctypes.WinDLL(dll_path_and_file)


result = my_dll.__dict__
print(result)

# method 2
dll_library = ctypes.cdll.LoadLibrary(dll_path_and_file)


print(dll_library.__dict__)


dotnet.add_assemblies(dll_path)
dotnet.load_assembly(r'Bluefin.Servers.PubSub.Excel')

from Bluefin.Servers.PubSub.Excel import *

rtdPub = ExcelFunctions()
while True:
	choice = raw_input("> ")
	rtdPub.P2PPublish("lon","rick","test",choice)




# import winreg


# x = winreg.ConnectRegistry(None, '44803')


# print(x)




