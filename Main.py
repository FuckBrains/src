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
import json

'''
'testeeeee'
'''

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
    # Module_list,modules = get_modules()
    # print(Module_list)
    # print('============')
    # print(type(submit['Config']['Mission_Id']))
    # print(submit['Config']['Mission_Id'])
    module = 'Mission_'+submit['Config']['Mission_Id']
    print(module)
    Module = import_Module(module)
    submit['Site'] = submit['Config']['url_link']
    try:
        Module.web_submit(submit)
    except:
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

def import_Module(module):
    module_name = importlib.import_module(module)
    return module_name

def sort_Mission_conf(Mission_conf_list):
    '''
    Mission_conf_list = {"0": {"Alliance": "Finaff", "Offer": "Royal Cams(Done)", "url_link": "http"}, "1": {"Alliance": "Finaff", "Offer": "Royal Cams(Done)", "url_link": "http"}}
    Mission_conf_duplicated_one ={'0':{"Alliance": "Finaff", "Offer": "Royal Cams(Done)", "url_link": "http"},...}
    1 <= num <= len(Mission_conf_list['1000x'])
    '''
    # file_Offer_config = r'ini\Offer_config.ini'
    # Offer_config = read_ini(file_Offer_config)
    # keys = []
    # for item in Offer_config:
    #     keys.append(item)
    # for index in Mission_conf_list:
    #     if Mission_conf_list[index]['Offer'] in keys:

    Mission_conf_duplicated_all = []
    while True:
        Mission_conf_one = {}
        items = []
        for dicts in Mission_conf_duplicated_all:
            for index_item in dicts:
                items.append(index_item)
        for item in Mission_conf_list:
            if item in items:
                continue
            if len(Mission_conf_one) == 0:
                Mission_conf_one[item] = Mission_conf_list[item]
                continue
            Alliances = []
            country = ''
            Mission_Id = []
            Excel = ''
            for index in Mission_conf_one:
                Alliances.append(Mission_conf_one[index]['Alliance'])
                Mission_Id.append(Mission_conf_one[index]['Mission_Id']) 
                if Mission_conf_one[index]['Excel'][0] != '':
                    Excel = Mission_conf_one[index]['Excel'][0]
            Country = Mission_conf_one[index]['Country']
            if Mission_conf_list[item]['Alliance'] in Alliances:
                continue
            if Mission_conf_list[item]['Country'] != Country:
                continue
            if Excel !='':
                if Mission_conf_list[item]['Excel'][0] != Excel:
                    continue
            if Mission_conf_list[item]['Mission_Id'] in Mission_Id :
                continue
            Mission_conf_one[item] = Mission_conf_list[item]
        if len(Mission_conf_one) == 0:
            break
        Mission_conf_duplicated_all.append(Mission_conf_one)
    return Mission_conf_duplicated_all


def change__delay_config():
    file_Offer_config = r'ini\Offer_config.ini'
    Offer_config = read_ini(file_Offer_config)
    Offer_config['Delay'] = {}
    Offer_config['Delay']['up'] = 3
    Offer_config['Delay']['down'] = 5
    Offer_config['Delay']['threads']= 5
    Offer_config['Email_list'] = {}
    Offer_config['Email_list']['hotmail.com'] = 1
    Offer_config['Email_list']['outlook.com'] = 1
    Offer_config['Email_list']['yahoo.com'] = 1
    Offer_config['Email_list']['aol.com'] = 1
    write_ini(file_Offer_config,Offer_config)
    

def EMU_multi():
    # test
    Excel_names = db.get_excel_names()
    '''
    get all links without sorted
    '''
    file_Offer_link = r'ini\Offer_link.ini'
    Offer_links = read_ini(file_Offer_link)
    # sort all links into lists
    # print(Offer_links)
    Mission_conf_duplicated_all = sort_Mission_conf(Offer_links)
    # print(Mission_conf_duplicated_all)
    file_Offer_config = r'ini\Offer_config.ini'
    Offer_config = read_ini(file_Offer_config)  
    # print(Offer_config)
    Email_list_new = []
    Email_list = Offer_config['Email_list']
    for item in Email_list:
        if Email_list[item] == 1:
            Email_list_new.append(item)
    # go through all the links from lists
    for Mission_conf_duplicated in Mission_conf_duplicated_all:     
        # print(Mission_conf_duplicated)
        # print(Mission_conf_duplicated)
        Mission_Ids = []
        for index in Mission_conf_duplicated:
            if Mission_conf_duplicated[index]['Mission_Id'] not in Mission_Ids:
                Mission_Ids.append(Mission_conf_duplicated[index]['Mission_Id'])
        country = Mission_conf_duplicated[index]['Country']
        print(country)
        print(Mission_Ids)
        killpid()
        # print(modules)
        # print('Reading config from sql server...')
        Excels_dup = ['','']
        for index in Mission_conf_duplicated:
            Excel = Mission_conf_duplicated[index]['Excel'] 
            if Excel[0] != '':
                Excels_dup[0] = Excel[0]
            if Excel[1] != '':
                Excels_dup[1] = Excel[1]
        while True:
            submit1 = db.read_one_excel(Mission_Ids,Excels_dup,Email_list)
            print(submit1)
            print('Reading config from sql server success')
            if Excels_dup[1] != '':
                flag = imap_test.Email_emu_getlink(submit1['Email'])
                if flag == 0:
                    print('Bad email:',submit1['Email']['Email_emu'])
                    db.updata_email_status(submit1['Email']['Email_Id'],0)
                    continue
                else:
                    print("Good email")
                    db.updata_email_status(submit1['Email']['Email_Id'],1)
                    break
            else:
                break
        # changing IP
        for num_ip in range(6):
            if Excels_dup[0] != '':
                city = ip_test.ip_Test('',state = submit1[Excels_dup[0]]['state'],country=country )
            if  city != 'Not found':
                break
            if num_ip == 5:
                print('Net wrong...!!!!!!')
                return
        submits = []
        submit = {}
        for item in Mission_conf_duplicated:
            submit = submit1.copy()
            submit['Config'] = Mission_conf_duplicated[item]
            submits.append(submit)
            submit = {}
        db.write_one_info(Mission_Ids,submit1)
        requests = threadpool.makeRequests(multi_reg, submits)
        [pool.putRequest(req) for req in requests]
        pool.wait() 
        killpid()
    # return
    # time_delay = random.randint(Delay['up']*60,Delay['down']*60)
    # print('Sleeping',time_delay,'Minutes')
    # sleep(time_delay)
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
