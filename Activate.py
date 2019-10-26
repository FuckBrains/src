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



pool = threadpool.ThreadPool(6)


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

def detect_status(submit):
    if submit['Cookie'] == '':
        # print('This Convertion is of no cookie.........')
        return {}
    flag = time_related.getactivatetime(submit['Create_time'])
    if flag == 0:
        # print('Convertion made of ',submit['Create_time'],'No need to activate')
        return {}
    elif flag == 1:
        activate_term = 'activate1'
        submit['activate_term'] = 'activate1'
        # print('activate1==============')
    elif flag == 2:
        return_rand = random.randint(0,5)
        if return_rand == 0:
            activate_term = 'activate1'
            submit[activate_term] = 'No activate'
            # db.update_activate_status(submit)
            # print('between activate1 and activate2....................')
            return {}       
        activate_term = 'activate2'
        submit['activate_term'] = 'activate2'
        # print('activate2===========')
    elif flag == 3:
        return_rand = random.randint(0,5)
        if return_rand == 0:
            activate_term = 'activate2'
            submit[activate_term] = 'No activate'
            # db.update_activate_status(submit)            
            # print('between activate2 and activate3....................')
            return {}        
        activate_term = 'activate3'
        submit['activate_term'] = 'activate3'
        # print('activate3............')
    return_rand_ = random.randint(0,5)
    submit['activate_term'] = activate_term
    if return_rand_ == 0:
        activate_term = 'activate2'
        submit[activate_term] = 'No activate'
        # db.update_activate_status(submit)            
        # print('between activate2 and activate3....................')        
        # print('unique  random,return....................')
        return {}
    # print('dddddddddddddddddd')
    return submit




def multi_activate(submit):
    # print(submit)
    time_cheat = random.randint(0,10)
    print('Sleep for random time:',time_cheat*60,'-------------')
    sleep(time_cheat*60)
    account = db.get_account()
    submit['ip_lpm'] = account['IP']
    submit['port_lpm'] = luminati.get_port_random()
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
        # for item in submit:
        #     if ''
        submit[submit['activate_term']] = str(datetime.datetime.now())
        db.update_activate_status(submit) 
    luminati.delete_port([submit['port_lpm']])
    # global Falg_threads
    # Falg_threads += 1
    # print('Falg_threads:',Falg_threads)
def import_Module(module):
    module_name = importlib.import_module(module)
    return module_name

def get_unique_plans(plans):
    plans = [plan for plan in plans if plan['Activate_status'] == 1]
    plans_unique = []
    for plan in plans:
        flag = 0
        for plan_unique in plans_unique:
            if plan['Alliance'] == plan_unique['Alliance']:
                if plan['Account'] == plan_unique['Account']:
                    if plan['Mission_Id'] == plan_unique['Mission_Id']:
                        print('Same Mission')
                        flag = 1
                        break
        if flag == 0:
            plans_unique.append(plan)
    return plans_unique

def main(j):
    print('checking system time')
    # time_related.update_time_system()
    print('Fix system time completed')
    while True:
        try:
            tools.killpid()
        except Exception as e:
            print(str(e))
            pass    
        plans = db.read_plans(j)
        print('total',len(plans),'plans')
        submits_combine = []
        plans = get_unique_plans(plans)
        print('total',len(plans),'unique plans')
        for plan in plans:
            print(plan)
            submits = db.get_cookie(plan)
            # print(submits)
            print('Plan_Id',plan['Plan_Id'],len(submits),'with cookie')
            submits_ = []
            Country = plan['Country']
            for submit in submits:
                # print(submit)
                submit['Country'] = Country
                submit['Email'] = {}
                submit['Email']['Email_Id']= submit['Email_Id']
                submit = detect_status(submit)
                if len(submit) != 0:
                    # db.update_activate_status(submit)
                    # return
                    submits_.append(submit)
                    submits_combine.append(submit)
            print(len(submits_),'to activate')
            print('Total',len(submits_combine),'To activate')
            # return                    
            # if len(submits_) == 0:
            #     print('with nothing to activate')
            #     continue
        print('===============================')
        print(len(submits_combine))
        if len(submits_combine) == 0:
            print('No activate plan,sleep for 1hour')
            for i in range(60):
                print('%d minutes left...'%(60-i))
                sleep(60)                
            continue
        # print(submit)
        # submit['activate1'] = datetime.datetime.utcnow()
        # db.update_activate_status(submit)
        random.shuffle(submits_combine)
        requests = threadpool.makeRequests(multi_activate, submits_combine)
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
    paras=sys.argv
    # test    
    # paras = [0,1,2,3,4]
    # print(paras)
    # i = int(paras[1])
    # i=2
    # print(i)  
    main(9)



