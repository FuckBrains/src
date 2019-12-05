import psutil
import os

def killpid(kill_list=[]):
    pids = psutil.pids()
    for pid in pids:
        # print(pids)
        try:
            p = psutil.Process(pid)
        except:
            continue
        if kill_list == []:
            kill_list = ['chrome.exe','chromedriver','Client.exe','Monitor.exe','MonitorGUI.exe','Socket.exe','CCleaner','wps','Annoucement']
            # kill_list = ['chrome.exe','chromedriver']        
        for key in kill_list:
            # print(key)
            if key in p.name():
                cmd = 'taskkill /F /IM '+p.name()
                try:
                    os.system(cmd)            
                except Exception as e:
                    print(str(e))


def get_pid(key=''):
    pids = psutil.pids()
    p_all = []
    for pid in pids:
        # print(pids)
        try:
            p = psutil.Process(pid)
        except Exception as e:
            print(str(e))
            continue
        if key in p.name():
            # print(p)
            p_all.append(p)
    return p_all

def findpid(key):
    p_all = get_pid(key)
    # print('first:',p_all)
    # command = '''start cmd /k "python test.py "{$name$:$qcy$}" && exit"'''
    # os.system(command)
    p_all = get_pid(key)
    print('then:',p_all)




if __name__ == '__main__':
    # key = 'cmd'
    # findpid(key)
    killpid()