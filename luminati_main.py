import threading
import random
import os
import sys
sys.path.append("..")
import importlib
import threadpool
from time import sleep
import Changer_windows_info as changer
import db
import tools
import thread_tokill as tk

'''
'testeeeee'
'''

pool = threadpool.ThreadPool(5)

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
            plans_ = db.read_plans(plan_id)
            print(len(plans_))
            plans = []
            for plan in plans_:
                for count in range(plan['Mission_time']):
                    plans.append(plan)
            print(plans)
            print(len(plans))
        except Exception as e:
            print(str(e))
            print('get db failed,restart........')
            changer.Restart()
        if len(plans) == 0:
            print('No plan for this computer!!!!!!')
            return
        # print(plans)
        requests = threadpool.makeRequests(tk.multi_reg, plans)
        [pool.putRequest(req) for req in requests]
        pool.wait() 
        print('All Missions finished..............')
        try:
            print('try killing pids')
            tools.killpid()
            print('kill pids finished')
        except Exception as e:
            print(str(e))
            pass          
        if i == 1:
            restart_time = random.randint(3,5)
            print('Mission completed.........')
            print('Sleep',restart_time,'minutes')
            # sleep(restart_time*60)
            changer.Restart()
            sleep(200)

def test():
    print(Delay)
    print(pool)
    print(Config)

if __name__ == '__main__':
    paras=sys.argv
    i = int(paras[1])
    # i = 1
    main(i)
