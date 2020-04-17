import random
import os
import sys
sys.path.append("..")
from time import sleep
import Changer_windows_info as changer
import db
import tools
import thread_tokill as tk


'''
'testeeeee'
'''



'''
flag:
    0 : Init status
    1 : Mission failed,but data should be uploaded
    2 : Mission finished success,data upload to db    
    --use plan['ID'] as key
'''




# def get_modules():
#     modules = os.listdir('..\src\\')
#     modules = [module.strip('.py') for module in modules] 
#     modules = [module.strip('.py') for module in modules] 
#     modules_new = []
#     for module in modules:
#         if 'Mission' in module:
#             # print(module)
#             modules_new.append(module)  
#     modules = ['src.'+ module for module in modules_new]             
#     # print(modules)
#     Module_list = []
#     # print(modules)
#     for module in modules:
#         Module_list.append(importlib.import_module(module)) 
#     return Module_list,modules

# def import_Module(module):
#     module_name = importlib.import_module(module)
#     return module_name

def check_version():
    num_db = db.get_current_version()
    num_db = str.join('.',num_db)
    file = r'ini\\VERSION.ini'
    with open(file) as f:
        num_native = f.readline()
    print('db version:%s'%num_db)
    print('native version:%s'%num_native)
    flag = False
    if num_native == num_db:
        flag = True
    # print(flag)
    return flag

def change_update_file():
    files = os.listdir('.')
    print(files)
    if 'Auto_update2.pyc' in files:
        # print(modules)
        file = os.path.join(os.getcwd(),'Auto_update.pyc')
        file2 = os.path.join(os.getcwd(),'Auto_update2.pyc')
        os.remove(file)
        os.rename(file2,file)

def main(i):
    # while True:
    flag = check_version()
    if flag == False:
        change_update_file()
        command = '''start cmd /k "python Auto_update.pyc 1"{$name$:$qcy$}" "'''
        os.system(command)
        return
    for j in range(1):
        try:
            if i != 3:
                tools.killpid()
            print(']]]]')
        except Exception as e:
            print(str(e))
            pass
        account = db.get_account()
        plan_id = account['plan_id']
        # print('Plan_id:',plan_id,',connecting sql for plan info...')
        try:
            db.update_flag_use_all()
            plans_ = db.read_plans(plan_id)
            print(len(plans_))
            plans = []
            for plan in plans_:
                # init sleep_flag and Status
                plan['sleep_flag'] = i
                db.update_plan_status(0,plan['ID'])                
                for count in range(plan['Mission_time']):
                    plans.append(plan)
            # print(plans)
            # print(len(plans))
        except Exception as e:
            print(str(e))
            print('get db failed,restart........')
            changer.Restart()                     
        if len(plans) == 0:
            print('No plan for this computer!!!!!!')
            return
        # print(plans)
        tk.start(plans)
        print('All Missions finished..............')
        try:
            print('try killing pids')
            if i != 3:            
                tools.killpid()
            else:
                return
            print('kill pids finished')
        except Exception as e:
            print(str(e))
            pass          
        restart_time = random.randint(1,5)
        print('Mission completed.........')
        print('Sleep',restart_time*60,'minutes')
        # sleep(restart_time*60)
        if i == 4:
            return
        changer.Restart()
        sleep(200)

def test():
    check_version()

if __name__ == '__main__':
    paras=sys.argv
    i = int(paras[1])
    main(i)
    # test()