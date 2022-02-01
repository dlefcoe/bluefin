'''
https://stackoverflow.com/questions/62923189/rtd-client-in-python


@darrenlefcoe

requires:
pip install pywin32

'''


import pythoncom
from rtd import RTDClient

if __name__ == '__main__':
    time = RTDClient('xrtd.xrtd')
    time.connect()
    time.register_topic('EUCA')

    while 1:
        pythoncom.PumpWaitingMessages()

        if time.update():
            print (time.get('EUCA'))


