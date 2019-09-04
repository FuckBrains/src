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
    file_Offer_config = r'ini\Offer_config.ini'    
    Offer_config = read_ini(file_Offer_config)  
    Email_list_new = []
    Email_list = Offer_config['Email_list']    
    Mission_Ids,Excels_dup = [Config['Mission_Id']],Config['Excel']
    # print(Excels_dup)
    submit = db.read_one_excel(Mission_Ids,Excels_dup,Email_list)
    # print(submit)
    submit['ip_lpm'] = Config['ip_lpm']
    submit['prot_lpm'] = Config['prot_lpm']
    if Excels_dup[0] == '':
        state = ''
    else:
        state = submit[Excels_dup[0]]['state']
    luminati.ip_test(submit['ip_lpm'],submit['prot_lpm'],state=state ,country='')     
    module = 'Mission_'+Config['Mission_Id']
    # print(module)
    Module = import_Module(module)
    submit['Site'] = Config['url_link']
    submit['Mission_dir'] = Config['Mission_dir']
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


def EMU_multi():
    makedir_download()
    # clean_download()
    # test
    Excel_names = db.get_excel_names()
    '''
    get all links without sorted
    '''
    file_Offer_link = r'..\res\Offer_link.ini'
    Offer_links = read_ini(file_Offer_link)
    # sort all links into lists
    Mission_conf_duplicated_all = sort_Mission_conf(Offer_links)
    file_Offer_config = r'ini\Offer_config.ini'
    Offer_config = read_ini(file_Offer_config)  
    Email_list_new = []
    Email_list = Offer_config['Email_list']
    for item in Email_list:
        if Email_list[item] == 1:
            Email_list_new.append(item)
    # go through all the links from lists
    for Mission_conf_duplicated in Mission_conf_duplicated_all:     
        # global Falg_threads
        # Falg_threads = 0
        Mission_Ids = []
        for index in Mission_conf_duplicated:
            if Mission_conf_duplicated[index]['Mission_Id'] not in Mission_Ids:
                Mission_Ids.append(Mission_conf_duplicated[index]['Mission_Id'])
        country = Mission_conf_duplicated[index]['Country']
        print(country)
        print(Mission_Ids)
        try:
            killpid()
        except:
            pass
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
            try:
                print('Mission_Ids,Excels_dup,Email_list:')
                print(Mission_Ids,Excels_dup,Email_list)
                submit1 = db.read_one_excel(Mission_Ids,Excels_dup,Email_list)
            except Exception as e:
                print(str(e))
                # changer.Restart()
                return
            print(submit1)
            print('Reading config from sql server success')
            if Excels_dup[1] != '':
                print('testing email.........')
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
            try:
                if Excels_dup[0] != '':
                    city = ip_test.ip_Test('',state = submit1[Excels_dup[0]]['state'],country=country )
                else:
                    city = ip_test.ip_Test('','',country=country )
                if  city != 'Not found':
                    break
                if num_ip == 5:
                    print('Net wrong...!!!!!!')
                    changer.Restart()
                    return
            except:
                changer.Restart()
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
        # flag_next = len(submits) 
        # while True:
        #     if Falg_threads >= flag_next:
        #         break
        #     else:
        #         print('++++++++++++++++=================')
        #         print('Falg_threads:',Falg_threads)
        #         sleep(10)        
        try:
            killpid()
        except:
            pass
    if len(Mission_conf_duplicated_all) == 0:
        return
    # time_delay = random.randint(Delay['up']*60,Delay['down']*60)
    # print('Sleeping',time_delay,'Minutes')
    # sleep(time_delay)
    file_Offer_config = r'ini\Offer_config.ini'
    Offer_config = read_ini(file_Offer_config) 
    up = Offer_config['Delay']['up']   
    down = Offer_config['Delay']['down']
    time_delay = random.randint(up*60,down*60)
    print('Finish all tasks,starting sleep:',time_delay)    
    sleep(time_delay)
    changer.Restart()

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
    plan_id = 1
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
