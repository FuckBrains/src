import threading
import xlrd
from xlutils.copy import copy
import random
import os
import sys
sys.path.append("..")
import importlib
import threadpool
from time import sleep
import Changer_windows_info as changer
import imap_test
import Hotmail_check as hotmail
import psutil
import ip_test
from xlrd import xldate_as_tuple
from urllib import request, parse
import pymysql
import db
import re
import json
import luminati
import tools
import Chrome_driver

'''
'testeeeee'
'''

Falg_threads = 0
Mission_num = 0



pool = threadpool.ThreadPool(5)


                 
def multi_reg(Config):  
    # print(Config)
    global Falg_threads    
    return_rand = random.randint(0,5)
    if return_rand == 0:
        print('unique  random,return for Mission_Id:',Config)
    else:
        time_cheat = random.randint(0,5)
        print(Config)
        if Config['Alliance'] != 'Test':
            print('Sleep for random time:',time_cheat*60,'-------------')   
            sleep(time_cheat*60)
        else:
            print('test...........')
        while True:
            print('getting data')
            try:
                submit = db.get_luminati_submit(Config)
                print(submit)
                print('starting writing submit into db')
                if Config['Alliance'] == 'Test':
                    submit['state_'] = ''
                print('Data for this mission:')
                print(submit)
            except Exception as e:
                print(str(e))
                Falg_threads += 1
                print('Get data wrong..................................')
                print('Falg_threads',Falg_threads)
                print('Mission_num:',Mission_num)                
                # changer.Restart()
                return
            if submit['Excels_dup'][1] != '':
                print('testing email.........')
                flag = imap_test.Email_emu_getlink(submit['Email'])
                if flag == 0:
                    print('Bad email:',submit['Email']['Email_emu'])
                    db.updata_email_status(submit['Email']['Email_Id'],0)
                    continue
                else:
                    print("Good email")
                    db.updata_email_status(submit['Email']['Email_Id'],1)
            else:
                pass
            print(Config['Alliance'],'email test finished')
            flag = luminati.ip_test(submit['ip_lpm'],submit['port_lpm'],state=submit['state_'] ,country='')
            if flag == 1:
                break
            else:
                continue
            print('Reading config from sql server success')
        module = 'Mission_'+str(submit['Mission_Id'])
        Module = importlib.import_module(module)
        flag = 0
        try:
            print('----------------====================')
            chrome_driver = Chrome_driver.get_chrome(submit)
            flag = Module.web_submit(submit,chrome_driver=chrome_driver)
            print(submit)
        except Exception as e:
            print(str(e))
        try:
            chrome_driver.close()
            chrome_driver.quit()
        except:
            pass
        if flag == 1:
            mission_check = db.check_mission_status(submit)
            if len(mission_check) == 0:
                print('Mission: ',submit['Mission_Id'],'success,uploading db')
                db.write_one_info([str(submit['Mission_Id'])],submit)
        print('Mission_Id:',submit['Mission_Id'],'finished')
    Falg_threads += 1  
    print('Falg_threads',Falg_threads)
    print('Mission_num:',Mission_num)
    if Falg_threads == Mission_num:
        try:
            print('try killing pids')
            tools.killpid()
            print('kill pids finished')
        except Exception as e:
            print(str(e))
            pass  
    return  

    # print('Falg_threads:',Falg_threads)

def get_modules():
    modules = os.listdir('..\src\\')
    modules = [module.strip('.py') for module in modules] 
    modules_new = []
    for module in modules:
        if 'Mission' in module:
            # print(module)
            modules_new.append(module)  
    modules = ['src.'+ module for module in modules_new]             
    # print(modules)
    Module_list = []
    # print(modules)
    for module in modules:
        Module_list.append(importlib.import_module(module)) 
    return Module_list,modules

def import_Module(module):
    module_name = importlib.import_module(module)
    return module_name


def main(i):
    while True:
        try:
            tools.killpid()
        except Exception as e:
            print(str(e))
            pass    
        account = db.get_account()
        plan_id = account['plan_id']
        print('Plan_id:',plan_id,',connecting sql for plan info...')
        try:
            plans = db.read_plans(plan_id)
        except Exception as e:
            print(str(e))
            print('get db failed,restart........')
            changer.Restart()
        if len(plans) == 0:
            print('No plan for this computer!!!!!!')
            return
        print('Missions:')
        # print(plans)

        global Mission_num
        Mission_num = len(plans)
        print(Mission_num)
        requests = threadpool.makeRequests(multi_reg, plans)
        [pool.putRequest(req) for req in requests]
        pool.wait() 
        print('All Missions finished..............')
        if i == 1:
            restart_time = random.randint(3,5)
            print('Mission completed.........')
            print('Sleep',restart_time,'minutes')
            sleep(restart_time*60)
            changer.Restart()
            sleep(200)

def test():
    print(Delay)
    print(pool)
    print(Config)

if __name__ == '__main__':
    paras=sys.argv
    i = int(paras[1])
    main(i)
