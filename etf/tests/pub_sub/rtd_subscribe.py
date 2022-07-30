import dotnet 

#dotnet.add_assemblies(r'c:/Dev/testing/ExcelPubSubRTDWrapper/ExcelPubSubRTDWrapper/bin/Debug/')
dotnet.add_assemblies(r'Y:/Useful Code/PubSubRTDWrapper/')
dotnet.load_assembly(r'ExcelPubSubRTDWrapper')

from ExcelPubSubRTDWrapper import *

def disconnect():
	print "disconnected"
def data(rtdData):
	print "data in"
	print rtdData

rtd = RTDWrap()
rtd.SetDisconnectCallback(disconnect)
rtd.SetDataCallback(data)

count =1
while True:
	choice = raw_input("> ")
	count+=1
	#rtd.Subscribe(count,"lon",choice,"test")
	rtd.Subscribe(count,"lon","rick","age")
	choice = choice.lower() #Convert input to "lowercase"
