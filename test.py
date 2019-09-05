import socket
import Alliance_login
import os
import json
import threading
import threadpool
import random
pool = threadpool.ThreadPool(5)
Falg_threads = 0
import Chrome_driver
from time import sleep
import psutil
import db

def read_ini():
    file = r'Offer_conf.ini'
    submits = []
    with open(file,'r') as f:
        jss = f.readlines()
        # print(jss)
        for js in jss:
            submit = json.loads(js)
            submits.append(submit)
            # print(submit)
    if len(submits) >= 1:
        return submits[-1]
    else:
        return []


def write_ini(content):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    file = r'Offer_conf.ini'
    content = json.dumps(content) 
    with open(file,'w') as f:
        # content += '\n'
        f.write(content)

def add_missiion(Mission_conf):
    Mission_conf[0]



def main():
    offer_conf = {
    '10000':'',
    '10001':'',
    '10002':'Auto'
}
    write_ini(offer_conf)
    offer_conf = read_ini()
    print(offer_conf)


def multi_test(submit):
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get('http://www.baidu.com')
    print('ppppppppp')
    sleep_time = random.randint(100,300)
    sleep(sleep_time)
    chrome_driver.quit()    
    global Falg_threads
    Falg_threads += 1
    print('Falg_threads:',Falg_threads)


def killpid():
    pids = psutil.pids()
    print(pids)
    for pid in pids:
        try:
            p = psutil.Process(pid)
        except:
            continue
        kill_list = ['chrome.exe','chromedriver.exe','Client.exe','Monitor.exe','MonitorGUI.exe','Socket.exe']
        for key in kill_list:
            if p.name() == key:
                cmd = 'taskkill /F /IM '+key
                try:
                    os.system(cmd)            
                except:
                    pass


def test():
    for i in range(5):
        # global Falg_threads
        Falg_threads=0
        submits = ['','','','']
        requests = threadpool.makeRequests(multi_test, submits)
        [pool.putRequest(req) for req in requests]
        print('1111111111111111')
        pool.wait()   
        flag_next = len(submits) 
        killpid() 
        # while True:
        #     if Falg_threads >= flag_next:
        #         break
        #     else:
        #         print('++++++++++++++++=================')
        #         print('Falg_threads:',Falg_threads)
        #         sleep(10)


def makedir_download(path=r'c:\emu_download'):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)



def clean_download():
    modules = os.listdir(r'c:\emu_download')
    # print(modules)
    path = os.path.join(os.getcwd(),r'c:\emu_download')
    modules_path = [os.path.join(path,file) for file in modules]
    print(modules_path)
    [os.remove(file) for file in modules_path]    
    return 


def test_rest():
    Mission_list = ['10005']
    Excel_name = ['','Email']
    Email_list = ['hotmail.com','aol.com','outlook.com','yahoo.com']
    rest = db.read_rest(Mission_list,Excel_name,Email_list)
    print(rest)


def test_coding():
    import Auto_update
    Auto_update.read_account()

def test_html():
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get('https://trk.hracmp.com/click?pid=190&offer_id=2492')
    sleep(3000)



def test_db():
    plans = db.read_plans(1)
    print(plans)


def test_ip():
    myname = socket.getfqdn(socket.gethostname(  ))
    print(myname)
    myaddr = socket.gethostbyname(myname)
    print(myaddr)

if __name__ == '__main__':
    test_ip()
