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

'''
'testeeeee'
'''

# Falg_threads = 0



pool = threadpool.ThreadPool(5)


                 
def multi_reg(Config):
    time_cheat = random.randint(0,5)
    print(Config)
    if Config['Alliance'] != 'Test':
        print('Sleep for random time:',time_cheat*60,'-------------')    
        # sleep(time_cheat*60)
    else:
        print('test...........')
    while True:
        try:
            submit = db.get_luminati_submit(Config)
            if Config['Alliance'] == 'Test':
                submit['state_'] = ''            
            db.write_one_info([str(submit['Mission_Id'])],submit)
            print('Data for this mission:')
            print(submit)
        except Exception as e:
            print(str(e))
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
                # break
        else:
            pass
            # break              
        flag = luminati.ip_test(submit['ip_lpm'],submit['prot_lpm'],state=submit['state_'] ,country='')
        if flag == 1:
            break
        else:
            continue
        print('Reading config from sql server success')
    module = 'Mission_'+submit['Mission_Id']
    Module = importlib.import_module(module)
    try:
        Module.web_submit(submit)
        print(submit)
    except Exception as e:
        print(str(e))
    print('Mission_Id:',submit['Mission_Id'],'finished')
    # global Falg_threads
    # Falg_threads += 1
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
        plans = db.read_plans(plan_id)
        if len(plans) == 0:
            print('No plan for this computer!!!!!!')
            return
        print('Missions:')
        print(plans)
        requests = threadpool.makeRequests(multi_reg, plans)
        [pool.putRequest(req) for req in requests]
        pool.wait() 
        print('All Missions finished..............')
        if i == 1:
            restart_time = random.randint(3,5)
            print('Mission completed.........')
            # print('Sleep',restart_time,'minutes')
            # sleep(restart_time*60)
            changer.Restart()
            sleep(200)


def test():
    # submit = read_excel()
    # write_excel(submit)
    print(Delay)
    print(pool)
    print(Config)


if __name__ == '__main__':
    paras=sys.argv
    # test    
    # paras = [0,1,2,3,4]
    i = int(paras[1])
    # print(i)
    # i=0
    main(i)

    # if i == 1:
    #     # test()
    #     main()
    # elif i == 2:
    #     Hotmail_Login()
    # elif i == 3:
    #     Hotmail_Recovery()
    # elif i == 4:
    #     test()

    
    # get_modules()
    # read_excel()
