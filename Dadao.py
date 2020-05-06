from time import sleep
import xlrd
from xlutils.copy import copy
# from wrapt_timeout_decorator import *
import db
import tools
import importlib
import ip_test
import traceback
import Chrome_driver
import random
import Changer_windows_info as changer
import traceback
import os
import json
import thread_tokill
import sys
import threadpool
import threading
import datetime





write_flag = 0
pool = threadpool.ThreadPool(5)


def makedir_account(path):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)

def writelog(chrome_driver,submit):
        '''
        writelog and
        '''

        path = r'..\log'        
        makedir_account(path)        
        path_ = r'..\log\pics'        
        makedir_account(path_)
        path_ = os.path.join(path_,str(submit['Mission_Id']))
        makedir_account(path_)  
        starttime = datetime.datetime.utcnow() 
        time_now = str(starttime).split('.')[0].replace(' ','').replace(':','')          
        pic_name = time_now+'.png'
        pic = os.path.join(path_,pic_name)
        print(pic)
        try:
            chrome_driver.save_screenshot(pic)
            print('pic saved success')
        except Exception as e:
            print(str(e))
        with open(pic,'rb') as f:
            png = f.read()
        Mission_Id = submit['Mission_Id']
        traceback_ = traceback.format_exc()
        db.write_log_db(Mission_Id,traceback_,png)
        # write_flag = 0

def get_excel(path):
    path_excel = path
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    return sheet,workbook    

def get_one_data(sheet,Mission_Id,Country=''):
    rows = sheet.nrows
    print(rows)
    # list_rows = random.sample(range(rows),rows)    
    badname = []
    submit_ = {}
    for i in range(rows):
        print(i)
        if i==0:
            keys = sheet.row_values(i)
            continue
        values = sheet.row_values(i)
        submit = dict(zip(keys,values))
        # print(submit) 
        if Country != '': 
            if submit['Country'] != Country:
                continue
        key = 'Status_'+ str(Mission_Id)
        flag_alpha = True
        for key_ in submit:
            submit[key_] = str(submit[key_]).replace('\t','').replace(' ','')
        firstname = submit['firstname'].replace('\t','').replace(' ','')
        lastname = submit['lastname'].replace('\t','').replace(' ','') 
        # print(submit[key])
        # print(firstname)
        # print(lastname)        
        if submit[key] == '':
            if len(firstname) == 0:
                submit['row'] = i
                submit['badname'] = badname
                submit_ = submit
                break
            if len(lastname) == 0:
                submit['row'] = i
                submit['badname'] = badname
                submit_ = submit                
                break            
            for part in firstname:
                a = tools.is_alphabet(part)
                if a == False:
                    flag_alpha = a
                    print('not alpha:',part)
                    break
            for part in lastname:
                a = tools.is_alphabet(part)
                if a == False:
                    print('not alpha:',part)                    
                    flag_alpha = a
                    break
            if flag_alpha == True:
                submit['row'] = i
                submit['badname'] = badname
                submit['lastname'] = lastname
                submit['firstname'] = firstname   
                submit_ = submit              
                break
            else:
                badname.append(i)
    # print('submit find:',submit)
    return submit_

def change_ip(country):
    for i in range(5):
        try:
            ip_test.ip_Test('',state = '',country=country )
            return
            # if zipcode != '' and zipcode != None:
            #     submit['zipcode'] = zipcode
            #     return submit
        except:
            pass
    changer.restart()

def change_ip_dadao():
    import urllib.request
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({'socks5':'socks5://51.15.13.163:2380'}))
            # {'http':'http://192.168.30.131:24001'}))
    # url_test = 'http://lumtest.com/myip.json'
    # url_test = 'http://www.google.com'
    res = str(opener.open('http://lumtest.com/myip.json').read(),encoding = "utf-8")
    # res = json.loads(res)
    print(res)

def write_status(path,workbook,submit,content):
    book2 = copy(workbook)
    sheet2 = book2.get_sheet(0) 
    col = int(str(submit['Mission_Id'])[-3:])+12
    print(col)
    sheet2.write(submit['Dadao']['row'],col,content)
    book2.save(path)
    # write_flag = 0

def mission(plans):
    requests = threadpool.makeRequests(reg_part, plans)
    [pool.putRequest(req) for req in requests]
    pool.wait()       

def get_write_content(submit):
    submit_ = {}
    if 'password' in submit:
        submit_['password'] = submit['password']
    if 'zipcode' in submit:
        submit_['zipcode'] = submit['zipcode']
    if 'status' in submit:
        submit_['status'] = submit['status']
    content = json.dumps(submit)
    return content    

# @timeout(600)
def reg_part(plan):
    path = r'..\res\Dadao.xlsx'
    global write_flag
    while True:
        if write_flag != 0:
            sleep(3)
        else:
            write_flag = 1
            break      
    sheet,workbook = get_excel(path)    
    submit_ = get_one_data(sheet,plan['Mission_Id'])
    if submit_ == {}:
        print('no data found')
        write_flag = 0
        return
    submit = {}
    submit['Dadao'] = submit_
    submit['Site'] = plan['url_link']
    submit['Mission_Id'] = plan['Mission_Id']
    submit['count'] = plan['count']
    submit['Mission_dir'] = plan['Mission_dir']
    submit['Excels_dup'] = ['Dadao','']
    submit['Country'] = plan['Country']
    print('reg_part')
    write_status(path,workbook,submit,'0')
    write_flag = 0
    # module = 'Mission_'+str(plan['Mission_Id'])
    # Module = ''
    # try:
    #     Module = importlib.import_module(module)
    # except:
    #     pass
    try:
        Page_flags = db.get_page_flag(submit['Mission_Id'])  
        print(Page_flags)      
        if len(Page_flags) == 0:
            print('No Page_flags found in db')
            return
        else:
            chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
            submit['Page_flags'] = Page_flags
            print('Page_flags found,use Record modern')
        thread_tokill.web_submit(submit,chrome_driver,debug=0)
        writelog(chrome_driver,submit)
        # print(submit)
    except Exception as e:
        print(str(e))
        a = traceback.format_exc()
        print(a)
        try: 
            writelog(chrome_driver,submit)
            print('==========++++')
        except Exception as e:
            print(str(e))
            # traceback.format_exc()
    print('misission finished')
    # content = json.dumps(submit)
    status = db.get_plan_status(plan['ID'])    
    while True:
        if write_flag != 0:
            print('threading ',submit['count'],'Global ',write_flag)
            sleep(3)
        else:
            write_flag = 1
            break          
    sheet,workbook = get_excel(path) 
    if str(status) == '0':
        status = ''    
    write_status(path,workbook,submit,str(status))
    write_flag = 0
    print('write status finished')
    try:
        chrome_driver.close()
        chrome_driver.quit()
    except:
        pass
    for i in submit['Dadao']['badname']:
        submit['row'] = i
        while True:
            if write_flag != 0:
                sleep(3)
            else:
                write_flag = 1
                break          
        sheet,workbook = get_excel(path)     
        write_status(path,workbook,submit,'badname')          
        write_flag = 0        

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

def main(num):
    try:
        flag = check_version()
    except Exception as e:
        print(str(e))
        print('get db failed,restart........')
        changer.Restart()     
    if flag == False:
        change_update_file()
        command = '''start cmd /k "python Auto_update.pyc 1"{$name$:$qcy$}" "'''
        os.system(command)
        return        
    # while True:
    for i in range(1):

        account = db.get_account()
        plan_id = account['plan_id']
        # print('Plan_id:',plan_id,',connecting sql for plan info...')
        try:
            db.update_flag_use_all()
            plans = db.read_plans(plan_id)
            for k in range(len(plans)):
                plans[k]['count'] = k
            # print(len(plans_))
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
        if num == 0:
            try:
                tools.killpid()
            except Exception as e:
                print(str(e))
            change_ip(plans[0]['Country'])            

        mission(plans)
        print('All Missions finished..............')
        try:
            print('try killing pids')
            # tools.killpid()
            return
            print('kill pids finished')
        except Exception as e:
            print(str(e))
            pass          
        restart_time = random.randint(3,5)
        print('Mission completed.........')
        print('Sleep',restart_time,'minutes')
        # sleep(restart_time*60)
        changer.Restart()
        sleep(200)

def test():
    path = r'..\res\Dadao.xlsx'
    row = 100    
    for length in range(row):  
        sheet,workbook = get_excel(path)  
        row = sheet.nrows        
        submit = get_one_data(sheet,11000)
        return
        submit['Mission_Id'] = 11000    
        write_status(path,workbook,submit)
        print(submit['firstname'],submit['lastname'])
        for i in submit['firstname']:
            a = tools.is_alphabet(i)
            print(i,a)            
            if a == False:
                return
        for i in submit['lastname']:
            a = tools.is_alphabet(i)
            print(i,a)            
            if a == False:
                return            

if __name__ == '__main__':
    paras=sys.argv
    i = int(paras[1])
    main(i)