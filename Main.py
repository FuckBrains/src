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

'''
'testeeeee'
'''



Delay, Config, Mission_conf, Email_list  = Cam4_allin.Config_read()
pool = threadpool.ThreadPool(Delay['threads'])


def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()


def read_excel():
    path_excel = r'..\res\Config.xlsx'
    workbooks = xlrd.open_workbook(path_excel)
    sheet = workbooks.sheet_by_index(0)
    rows = sheet.nrows
    keys = sheet.row_values(0)
    # print(keys)
    submit = {}
    submit['Index'] = -1
    for i in range(rows):
        if sheet.cell(i,0).value == '':
            values = sheet.row_values(i)
            submit = dict(zip(keys,values))
            submit['Index'] = i
            break
    # print(submit)
    if len(submit) == 1:
        return submit
    if submit['Zip'] == '':
        return submit
    submit['Home_phone'] = str(int(submit['Home_phone'])).replace('-','')
    submit['Zip'] = str(int(submit['Zip']))
    if len(submit['Zip']) == 4:
        submit['Zip'] = '0' + submit['Zip']
    submit['Height_FT'] = str(random.randint(4,7))
    submit['Height_Inch'] = '0'+str(random.randint(7,9))
    submit['Weight'] = str(int(random.randint(100,300)))
    if submit['Date_of_birth'] != '':
        date = xldate_as_tuple(submit['Date_of_birth'],0)
        # print(date)
    else:
        date = [str(random.randint(1960,1980))] 
    for item in date:
        if len(str(item)) == 2:
            if int(item) >= 50:
                submit['Year'] = '19' + str(item)    
        if len(str(item)) == 4:
            submit['Year'] = str(item)
    submit['Month'] = str(random.randint(1,12))
    submit['Day'] = str(random.randint(1,25))            
    return submit


def write_excel(submit,keyword = 'Done'):
    path_excel = r'..\res\Config.xlsx'
    workbooks = xlrd.open_workbook(path_excel)
    sheet = workbooks.sheet_by_index(0)
    book2 = copy(workbooks)
    sheet2 = book2.get_sheet(0)
    sheet2.write(submit['Index'],0,keyword)
    book2.save(path_excel)


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


def check_email(submit):
    print(submit['Email_emu'])
    data = {'email': submit['Email_emu']}
    data = parse.urlencode(data).encode('gbk')
    req = request.Request(url, data=data)
    page = ''
    for i in range(5):
        try:
            page = request.urlopen(req,timeout=10.0).read()
        except:
            continue
        if str(page) != '':
            break
    print(page)
    if 'GOOD_EMAIL' not in str(page):
        if page == '':
            return -1 #netwrong
        else:
            return 1 #fail
    else:
        print(submit['Email_emu'],'is GOOD_EMAIL')
        return 0 #success

def EMU_multi():
    # test
    Mission_list = [] 
    for item in Mission_conf:
        if Mission_conf[item] != '':
            Mission_list.append(int(item))
    if len(Mission_list) == 0:
        print('No Mission,check Cam4_allin')
        return
    changer.OpenCCleaner()
    sleep(30)         
    Email_list_new = []
    for item in Email_list:
        if Email_list[item] == 1:
            Email_list_new.append(item)
    while True:
        killpid()
        Module_list,modules = get_modules()
        Country = Config['IP_country']
        print(Email_list)
        submit1 = db.read_one_info(Country,Mission_list,Email_list_new)  
        print(submit1)
        db.write_one_info(Mission_list,submit1)
        flag = imap_test.Email_emu_getlink(submit)
        if flag == 0:
            print('Bad email:',submit1['Email_emu'])
            db.updata_email_status(submit['Email_Id'],0)
            continue
        else:
            db.updata_email_status(submit['Email_Id'],1)
        ip_test.ip_Test('',submit['State'])
        submits = []
        submit = {}
        for j in range(len(modules)):
            submit = submit1.copy()
            submit['Num']=str(j+10000)
            submits.append(submit)
            submit = {}
        print(submits)
        requests = threadpool.makeRequests(multi_reg, submits)
        [pool.putRequest(req) for req in requests]
        pool.wait() 
        # write_excel(submits[0])
        time_delay = random.randint(Delay['up']*60,Delay['down']*60)
        sleep(time_delay)
        changer.Restart()


def Hotmail_Login():
    path_excel = r'..\res\Hotmail_Login.xlsx'
    hotmail.Login(path_excel)


def Hotmail_Recovery():
    path_excel = r'..\res\Hotmail_Recover.xlsx'
    hotmail.recover(path_excel)


def test():
    submit = read_excel()
    write_excel(submit)

if __name__ == '__main__':
    paras=sys.argv
    # test    
    paras = [0,1]
    i = int(paras[1])
    if i == 1:
        # test()
        EMU_multi()
    elif i == 2:
        Hotmail_Login()
    elif i == 3:
        Hotmail_Recovery()

    
    # get_modules()
    # read_excel()
