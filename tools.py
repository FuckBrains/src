import psutil
import os

def killpid():
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
        except:
            continue
        kill_list = ['chrome.exe','chromedriver.exe','Client.exe','Monitor.exe','MonitorGUI.exe','Socket.exe']
        for key in kill_list:
            # print(key)
            if p.name() == key:
                cmd = 'taskkill /F /IM '+key
                try:
                    os.system(cmd)            
                except Exception as e:
                    print(str(e))
