import dotnet 

dotnet.add_assemblies(r'C:/Program Files (x86)/Bluefin Trading/PubSubExcel')
dotnet.load_assembly(r'Bluefin.Servers.PubSub.Excel')

from Bluefin.Servers.PubSub.Excel import *

rtdPub = ExcelFunctions()
while True:
	choice = raw_input("> ")
	rtdPub.P2PPublish("lon","rick","test",choice)
