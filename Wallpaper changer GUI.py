#(c) RedUp152 2025. All rights reserved.

from ctypes import windll
from datetime import datetime
from os import path
from win10toast import ToastNotifier
from pytz import timezone
from subprocess import run, check_output, DEVNULL, CREATE_NO_WINDOW, CalledProcessError
from tkinter import Button, Label, BooleanVar, Tk
from tkinter import ttk
from tkinter.ttk import Combobox, Checkbutton
from sys import exit, executable
from pyuac import isUserAdmin, runAsAdmin

ProgrammName = "Wallpaper Changer"
folderpath = path.join(path.dirname(executable),"EarthWallpapers")
TaskProgrammPath = path.join(path.dirname(executable), ProgrammName.replace(" ", "-") + ".exe")
iconpath = path.join(path.dirname(executable),"icon.ico")
if path.exists(path=iconpath): pass
else: iconpath = None

def ErrorMessage(Error):
    try:
        Error = str(Error)
        if Error == "NoFileFound": Message = "Файл обоев не найден."
        elif Error == "RunAsAdminError": Message = "Не удалось запустить программу от имени администратора."
        elif Error == "AddTaskError": Message = "Не удалось включить выполнение по расписанию. Программа не сможет запускаться самостоятельно."
        elif Error == "RemoveTaskError": Message = f"Не удалось выключить выполнение задачи по расписанию. Вы можете отключить его самостоятельно отключив задачи \"{ProgrammName}_Hourly\",\"{ProgrammName}_OnStart\"."
        else: Message = "Возникла непредвиденная ошибка. Если это происходит часто переустановите программу или свяжитесь с разрботчиком. Код ошибки: " + str(Error) + "."
    except: Message = "Возникла непредвиденная ошибка. Если это происходит часто переустановите программу или свяжитесь с разрботчиком."
    ToastNotifier().show_toast(title="Во время работы программы произошла ошибка.",msg=Message,icon_path=iconpath,duration=5,threaded=True)

def ChangeWallpaper(Time=datetime.now(timezone("UTC")).hour):
    try:
        if Time == "12" or Time == "18" or Time == "21": Time = int(Time) - 1
        Wallpaper = path.join(folderpath, str(Time) + ".png")
        if path.exists(path=Wallpaper):
           windll.user32.SystemParametersInfoW(20,0,Wallpaper, 0)
        else: ErrorMessage("NoFileFound")
    except Exception as Error: ErrorMessage(Error)

def WallpaperUpdate():
    try:
        ChangeWallpaper(WalllpapersCombobox.get())
    except Exception as Error: ErrorMessage(Error)

def HourlyTask():
        AddHourlyTask = f'schtasks /Create /SC HOURLY /TN "{ProgrammName}_Hourly" /TR "{TaskProgrammPath}" /F'
        RemoveHourlyTask = f'schtasks /Delete /TN "{ProgrammName}_Hourly" /F'
        if HourlyCheckbox.get():
             try:
                run(AddHourlyTask,shell=False,check=True,stdout=DEVNULL,stderr=DEVNULL,creationflags=CREATE_NO_WINDOW)
             except: ErrorMessage("AddTaskError"); HourlyCheckbox.set(False)
        else:
            try:
                run(RemoveHourlyTask,shell=False,check=True, stdout=DEVNULL,stderr=DEVNULL,creationflags=CREATE_NO_WINDOW)
            except CalledProcessError: 
                if HourlyTaskExists() and isUserAdmin() == False: RunProgrammAsAdministrator()
            except: ErrorMessage("RemoveTaskError")

def OnStartTask():
    try:
        AddOnStartTask = f'schtasks /Create /SC ONSTART /TN "{ProgrammName}_OnStart" /TR "{TaskProgrammPath}" /F'
        RemoveOnStartTask = f'schtasks /Delete /TN "{ProgrammName}_OnStart" /F'
        if OnStartCheckbox.get():
            if isUserAdmin():
                run(AddOnStartTask,shell=False,check=True, stdout=DEVNULL,stderr=DEVNULL,creationflags=CREATE_NO_WINDOW)
            else: 
                RunProgrammAsAdministrator()
                OnStartCheckbox.set(False)
        else:
            try:
                run(RemoveOnStartTask,shell=False,check=True, stdout=DEVNULL,stderr=DEVNULL,creationflags=CREATE_NO_WINDOW)
            except CalledProcessError: 
                if OnStartTaskExists() and isUserAdmin() == False: RunProgrammAsAdministrator()
            except: ErrorMessage("RemoveTaskError")
    except  Exception as Error: ErrorMessage(Error); OnStartCheckbox.set(False)

def HourlyTaskExists():
    try: check_output(f'schtasks /Query /TN "{ProgrammName}_Hourly"',stderr=DEVNULL,creationflags=CREATE_NO_WINDOW); return(True)
    except CalledProcessError: return(False)

def OnStartTaskExists():
    try: check_output(f'schtasks /Query /TN "{ProgrammName}_OnStart"',stderr=DEVNULL,creationflags=CREATE_NO_WINDOW); return(True)
    except CalledProcessError: return(False)

def RunProgrammAsAdministrator():
    try:
        runAsAdmin(wait=False)
    except: ErrorMessage("RunAsAdminError"); return
    exit()

window = Tk()

HourlyCheckbox = BooleanVar()
OnStartCheckbox = BooleanVar()
HourlyCheckbox.set(HourlyTaskExists())
OnStartCheckbox.set(OnStartTaskExists())

window.title(ProgrammName)
window.resizable(False,False)
window.geometry("500x250")
window["bg"] = "#02235f"
window.iconbitmap(iconpath)

ttk.Style().configure("Custom.TCheckbutton", background="#02235f", foreground = "yellow")
ttk.Style().configure("CustomForCB.TLabel",background="#02505f", foreground = "yellow")

Label(window,text = ProgrammName,bg="#02225f",fg="yellow",anchor="n",font=("TkDefaultFont", 20,"bold")).grid(column=0,row = 0)
  
Label(window, text="Вы можете выбрать время самостоятельно (Часовой пояс - UTC)",bg="#02225f",fg="yellow").grid(column=0,row=2)

WalllpapersCombobox = Combobox(window,justify="center",state="readonly",style="CustomForCB.TLabel",takefocus=False, cursor="hand2")
WalllpapersCombobox["values"] = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23)
WalllpapersCombobox.current(datetime.now(timezone("UTC")).hour)
WalllpapersCombobox.grid(column=1,row=2)
WalllpapersCombobox.bind("<<ComboboxSelected>>", lambda _: WalllpapersCombobox.selection_clear()) 

Label(text="",master=window, background="#02235f").grid(row=3)
Label(text="",master=window, background="#02235f").grid(row=4)
Label(text="",master=window, background="#02235f").grid(row=5)

Checkbutton(window, text="Менять обои каждый час", variable=HourlyCheckbox,style="Custom.TCheckbutton",takefocus=False, cursor="hand2",command=HourlyTask).grid(column=0,row=6)
Checkbutton(window, text="Менять обои при запуске устройства", variable=OnStartCheckbox, style="Custom.TCheckbutton",takefocus=False, cursor="hand2",command=OnStartTask).grid(column=0,row=7)
Label(text="(Могут потребоваться права администратора.)",master=window,foreground="yellow",background="#02235f",font=("TkDefaultFont",8,"italic")).grid(row=8)


Label(text="",master=window, background="#02235f").grid(row=9)

Button(window,text="Обновить обои",command=WallpaperUpdate,bg="#10025f",fg="yellow",anchor="se",cursor="hand2").grid(column=1,row=10)

window.mainloop()