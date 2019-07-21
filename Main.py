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
import Cam4_allin
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

'''
'testeeeee'
'''



def get_all_config():
    Delay, Config, Mission_conf, Email_list  = Cam4_allin.Config_read()
    # Delay, Config, Mission_conf, Email_list = 1,1,1,1
    return Delay, Config, Mission_conf, Email_list 
    
Delay, Config, Mission_conf, Email_list = get_all_config()
pool = threadpool.ThreadPool(Delay['threads'])

def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()

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
        if p.name() == 'Client.exe':
            cmd = 'taskkill /F /IM Client.exe'
            os.system(cmd)
        if p.name() == 'Monitor.exe':
            cmd = 'taskkill /F /IM Monitor.exe'
            os.system(cmd)            
        if p.name() == 'MonitorGUI.exe':
            cmd = 'taskkill /F /IM MonitorGUI.exe'
            os.system(cmd)                  
        if 'CCleaner' in p.name():
            cmd = 'taskkill /F /IM ' + p.name()
            os.system(cmd) 
        if 'Socket.exe' in p.name():
            cmd = 'taskkill /F /IM ' + p.name()
            os.system(cmd)                         
  
def multi_reg(submit):
    # print('Starting Mission',submit['Num'])
    Module_list,modules = get_modules()
    # print(Module_list)
    for i in range(1):
        for j in range(len(modules)):
            if str(submit['Num']) in modules[j]:
                if 'http' in Mission_conf[str(submit['Num'])]:
                    submit['Site'] = Mission_conf[str(submit['Num'])]
                    try:
                        print(submit['Num'],'Starting')
                        # print(Module_list[j])
                        Module_list[j].web_submit(submit)
                    except Exception as e:
                        print(str(e))
                    print('Mission',submit['Num'],'end')
                    return
            else:
                # print('Mission not found')
                pass

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

def EMU_multi():
    # test
    print('Reading configs from Cam4_allin...')
    Mission_list = [] 
    for item in Mission_conf:
        if Mission_conf[item] != '':
            Mission_list.append(int(item))
    if len(Mission_list) == 0:
        print('No Mission,check Cam4_allin')
        return
    print('Configed Missions:',Mission_list)
    # changer.OpenCCleaner()
    # sleep(30)         
    Email_list_new = []
    for item in Email_list:
        if Email_list[item] == 1:
            Email_list_new.append(item)
    # print('Configed emails:',Email_list_new)
    while True:
        killpid()
        Module_list,modules = get_modules()
        # print(modules)
        nums = []
        for module in modules:
            num_module = re.findall(r'\d+',module) 
            nums+=num_module
        # print(nums)
        Country = Config['IP_country']
        # print(Email_list)
        Excel_names = db.get_excel_names()
        print('Reading config from sql server...')
        submit1=db.read_one_info(Country,Mission_list,Email_list,Excel_names)
        print('Reading config from sql server success')
        try:
            print('Testing email',submit1['Email']['Email_emu'])
        except:
            print('Email not found,check email status in sql and Email_list in Cam4_allin')
            return
        flag = imap_test.Email_emu_getlink(submit1['Email'])
        if flag == 0:
            print('Bad email:',submit1['Email']['Email_emu'])
            db.updata_email_status(submit1['Email']['Email_Id'],0)
            continue
        else:
            print("Good email")
            db.updata_email_status(submit1['Email']['Email_Id'],1)
        ip_test.ip_Test('',submit1['Usloan']['state'])
        submits = []
        submit = {}
        for num in nums:
            submit = submit1.copy()
            submit['Num']=num
            submits.append(submit)
            submit = {}
        db.write_one_info(Mission_list,submit1)
        requests = threadpool.makeRequests(multi_reg, submits)
        [pool.putRequest(req) for req in requests]
        pool.wait() 
        # write_excel(submits[0])
        time_delay = random.randint(Delay['up']*60,Delay['down']*60)
        print('Sleeping',time_delay,'Minutes')
        sleep(time_delay)
        changer.Restart()

def Hotmail_Login():
    path_excel = r'..\res\Hotmail_Login.xlsx'
    hotmail.Login(path_excel)

def Hotmail_Recovery():
    path_excel = r'..\res\Hotmail_Recover.xlsx'
    hotmail.recover(path_excel)

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
        EMU_multi()
    elif i == 2:
        Hotmail_Login()
    elif i == 3:
        Hotmail_Recovery()
    elif i == 4:
        test()

    
    # get_modules()
    # read_excel()
