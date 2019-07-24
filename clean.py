import psutil
import os


def killpid():
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
        except:
            continue
        # print('pid-%s,pname-%s' % (pid, p.name()))
        if p.name() == 'chrome.exe':
            cmd = 'taskkill /F /IM chrome.exe'
            os.system(cmd)
        if 'chromedriver.exe' in p.name() :
            cmd = 'taskkill /F /IM '+p.name()
            os.system(cmd)   
        # test   
        # if p.name() == 'Client.exe':
        #     cmd = 'taskkill /F /IM Client.exe'
        #     os.system(cmd)
        # if p.name() == 'Monitor.exe':
        #     cmd = 'taskkill /F /IM Monitor.exe'
        #     os.system(cmd)            
        # if p.name() == 'MonitorGUI.exe':
        #     cmd = 'taskkill /F /IM MonitorGUI.exe'
        #     os.system(cmd)                  
        # if 'CCleaner' in p.name():
        #     cmd = 'taskkill /F /IM ' + p.name()
        #     os.system(cmd) 
        # if 'Socket.exe' in p.name():
        #     cmd = 'taskkill /F /IM ' + p.name()
        #     os.system(cmd)  


if __name__ == '__main__':
    killpid()