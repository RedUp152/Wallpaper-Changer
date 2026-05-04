#(c) RedUp152 2025. All rights reserved.

from datetime import datetime
from pytz import timezone
from ctypes import windll
from os import path
from win10toast import ToastNotifier
from sys import executable,exit

folderpath = path.join(path.dirname(executable),"EarthWallpapers")
iconpath = path.join(path.dirname(executable),"icon.ico")
if path.exists(path=iconpath): pass
else: iconpath = None

def ChangeWallpaper(Time=datetime.now(timezone("UTC")).hour):
    try:
        if Time == "12" or Time == "18" or Time == "21": Time = int(Time) - 1
        Wallpaper = path.join(folderpath, str(Time) + ".png")
        if path.exists(path=Wallpaper):
           windll.user32.SystemParametersInfoW(20,0,Wallpaper, 0)
        else:
            ToastNotifier.show_toast(title="Во время смены обоев произошла ошибка.", msg="Файл обоев не найден.", duration=5,threaded=False,icon_path=iconpath)
            exit(1)
    except Exception as Error:
        ToastNotifier.show_toast(title="Во время смены обоев произошла ошибка.", msg="Возникла непредвиденная ошибка. Если это происходит часто переустановите программу или свяжитесь с разрботчиком. Код ошибки: " + str(Error) + ".", duration=5,threaded=False,icon_path=iconpath)
        exit(1)

ChangeWallpaper()