import psutil
import os

def killpid():
    pids = psutil.pids()
    for pid in pids:
        # print(pids)
        try:
            p = psutil.Process(pid)
        except:
            continue
        kill_list = ['chrome.exe','chromedriver.exe','Client.exe','Monitor.exe','MonitorGUI.exe','Socket.exe','CCleaner','wps']
        for key in kill_list:
            # print(key)
            if key in p.name():
                cmd = 'taskkill /F /IM '+p.name()
                try:
                    os.system(cmd)            
                except Exception as e:
                    print(str(e))
if __name__ == '__main__':
    killpid()