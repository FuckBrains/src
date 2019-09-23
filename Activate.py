import json
import luminati
import random
from time import sleep
import db
import time_related
import os
import Changer_windows_info as changer
import ip_test
import importlib
import sys
sys.path.append('..')
import threadpool
import Chrome_driver
import tools
import datetime



pool = threadpool.ThreadPool(4)


def killpid():
    pids = psutil.pids()
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


def getactivatestatus():
    time_related.getactivatetime()



def multi_activate(submit):
    # print(submit)
    if submit['Cookie'] == '':
        print('This Convertion is of no cookie.........')
        return
    return_rand = random.randint(0,3)
    if return_rand == 0:
        print('unique  random,return....................')
        return        
    flag = time_related.getactivatetime(submit['Create_time'])
    if flag == 0:
        print('Convertion made of ',submit['Create_time'],'No need to activate')
        return
    elif flag == 1:
        activate_term = 'activate1'
    elif flag == 2:
        return_rand = random.randint(0,5)
        if return_rand == 0:
            print('unique  random,return....................')
            return        
        activate_term = 'activate2'
    elif flag == 3:
        return_rand = random.randint(0,3)
        if return_rand == 0:
            print('unique  random,return....................')
            return         
        activate_term = 'activate3'
    if submit[activate_term] != '':
        print('Convertion made of ',submit['Create_time'],'Already done the activate')
        return
    time_cheat = random.randint(0,10)
    print('Sleep for random time:',time_cheat*60,'-------------')
    # sleep(time_cheat*60)
    account = db.get_account()
    submit['ip_lpm'] = account['IP']
    ports_used = luminati.ports_get(submit['ip_lpm'])
    port_ = 24000
    while port_ in ports_used:
        port_rand = random.randint(0,1000)
        basic_port = 24000
        port_ = basic_port + port_rand
    submit['port_lpm'] = port_
    luminati.add_proxy(submit['port_lpm'],country=submit['Country'],proxy_config_name='zone2',ip_lpm=submit['ip_lpm'])
    module = 'Mission_'+str(submit['Mission_Id'])
    Module = import_Module(module)
    print(module)
    print('Start activate Mission:',submit['Alliance'],'account',submit['Account'],',',submit['Mission_Id'],',',submit['Create_time'])
    flag_activate = 0
    try:
        chrome_driver = Chrome_driver.get_chrome(submit)
        flag_activate = Module.activate(submit,chrome_driver)
    except Exception as e:
        print(str(e))
    try:
        chrome_driver.close()
        chrome_driver.quit()
    except:
        pass
    if flag_activate == 1:
        db.update_activate_status(submit) 
    luminati.delete_port([submit['port_lpm']])
    # global Falg_threads
    # Falg_threads += 1
    # print('Falg_threads:',Falg_threads)

def import_Module(module):
    module_name = importlib.import_module(module)
    return module_name

def main():
    print('checking system time')
    # time_related.update_time_system()
    print('Fix system time completed')
    while True:
        try:
            tools.killpid()
        except Exception as e:
            print(str(e))
            pass    
        plans = db.read_plans(4)
        print('Mission:')
        print(plans)
        submits = []
        for plan in plans:
            print(plan)
            submits = db.get_cookie(plan)
            Country = plan['Country']
            if len(submits) == 0:
                continue
            else:
                break     
        # time_delta = datetime.timedelta(hours=-24*3)
        for submit in submits:
            submit['Country'] = Country
            submit['Email'] = {}
            submit['Email']['Email_Id']= submit['Email_Id']
            # print(submit['Create_time'])
            flag = time_related.getactivatetime(submit['Create_time'])
            # print(flag)
            # cookies = json.loads(submit['Cookie'])
            # # print(cookies)
            # for cookie in cookies:
            #     print(cookie)
            # print(type(cookies))
            # print(len(cookies))
            # return
        if len(submits) == 0:
            print('No activate plan,sleep for 1hour')
            for i in range(60):
                print('%d minutes left...'%(60-i))
                sleep(60)                
            continue
        # print(submit)
        # submit['activate1'] = datetime.datetime.utcnow()
        # db.update_activate_status(submit)
        requests = threadpool.makeRequests(multi_activate, submits)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        # restart_time = 60
        # print('Mission completed.........')
        # print('Sleep',restart_time,'minutes')
        # for i in range(60):
        #     print('%d minutes left'%(restart_time-i))
        #     sleep(restart_time*60)

def test():
    return_rand = random.randint(0,3)
    print(return_rand)


if __name__ == '__main__':
    # paras=sys.argv
    # test    
    # paras = [0,1,2,3,4]
    # i = int(paras[1])    
    main()



