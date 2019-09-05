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

'''
'testeeeee'
'''

# Falg_threads = 0

def read_ini(file):
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

def write_ini(file,content):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    content = json.dumps(content) 
    with open(file,'w') as f:
        # content += '\n'
        f.write(content)


pool = threadpool.ThreadPool(5)

# def writelog(runinfo,e=''):
#     file=open(os.getcwd()+"\log.txt",'a+')
#     file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
#     file.close()

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


                    
def multi_reg(Config):
    # print(Config)
    # return
    # print('Starting Mission',submit['Num'])
    # Module_list,modules = get_modules()
    # print(Module_list)
    # print('============')
    # print(type(submit['Config']['Mission_Id']))
    # print(submit['Config']['Mission_Id'])
    time_cheat = random.randint(0,5)
    print('Sleep for',time_cheat*60,'-------------')    
    sleep(time_cheat*60)
    while True:
        try:
            submit = db.get_luminati_submit(Config)
            print('Data for this mission:')
            print(submit)
        except Exception as e:
            print(str(e))
            # changer.Restart()
            return
        print('Reading config from sql server success')
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
                break
        else:
            break              
    module = 'Mission_'+submit['Mission_Id']
    Module = importlib.import_module(module)    
    db.write_one_info([submit['Mission_Id']],submit)
    luminati.ip_test(submit['ip_lpm'],submit['prot_lpm'],state=submit['state_'] ,country='')               
    try:
        Module.web_submit(submit)
        print(submit)
    except Exception as e:
        print(str(e))
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

def clean_download(path=r'c:\emu_download'):
    modules = os.listdir(path)
    # print(modules)
    path = os.path.join(os.getcwd(),r'c:\emu_download')
    modules_path = [os.path.join(path,file) for file in modules]
    print(modules_path)
    [os.remove(file) for file in modules_path]    
    return 

def makedir_file(path=r'c:\emu_download'):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)
        print('Making dir:',path,'success')


def create_emu_chrome(offerlist):
    offer_file = {}
    for i in range(len(offerlist)):
        offer_file[offerlist[i]] = offerlist.count(offerlist[i])
    print(offer_file)

def emu_chrome_count():
    emu_chromes = os.listdir(r'..\emu_chromes')
    print(emu_chromes)
    emu_chromes_count = {}
    for i in range(len(emu_chromes)):
        mission = emu_chromes[i].split(',')[0]
        if mission not in emu_chromes_count:
            emu_chromes_count[mission] = 1
        else:
            emu_chromes_count[mission] += 1
    print('emu_chromes_count:',emu_chromes_count)


def main():
    account = db.get_account()
    plan_id = account['plan_id']
    plans = db.read_plans(plan_id)
    print(plans)

    requests = threadpool.makeRequests(multi_reg, plans)
    [pool.putRequest(req) for req in requests]
    pool.wait() 
    # print(len(Configs))
    # print(Configs)


def test():
    # submit = read_excel()
    # write_excel(submit)
    print(Delay)
    print(pool)
    print(Config)


if __name__ == '__main__':
    paras=sys.argv
    # test    
    paras = [0,1,2,3,4]
    i = int(paras[1])
    if i == 1:
        # test()
        main()
    elif i == 2:
        Hotmail_Login()
    elif i == 3:
        Hotmail_Recovery()
    elif i == 4:
        test()

    
    # get_modules()
    # read_excel()
