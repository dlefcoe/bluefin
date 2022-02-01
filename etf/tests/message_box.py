import ctypes
ctypes.windll.user32.MessageBoxW(None,"Hello world","Bluefin Trading",0)


# message box options
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10


# yes/no box
ctypes.windll.user32.MessageBoxW(None,"Hello world","Bluefin Trading", MB_YESNO)



