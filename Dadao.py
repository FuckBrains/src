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
        pic_name = str(submit['Mission_Id'])+'_'+str(random.randint(0,100000))+'.png'
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

def get_excel(path):
    path_excel = path
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    return sheet,workbook    

def get_one_data(sheet,Mission_Id,Country=''):
    rows = sheet.nrows
    # print(rows)
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
        print(submit) 
        if Country != '': 
            if submit['Country'] != Country:
                continue
        key = 'Status_'+ str(Mission_Id)
        flag_alpha = True
        for key_ in submit:
            submit[key_] = str(submit[key_]).replace('\t','').replace(' ','')
        firstname = submit['firstname'].replace('\t','').replace(' ','')
        lastname = submit['lastname'].replace('\t','').replace(' ','') 
        print(submit[key])
        print(firstname)
        print(lastname)        
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
    return submit_

def change_ip(submit):
    country = submit['Country']
    for i in range(3):
        try:
            ip_test.ip_Test('',state = '',country=country )
            return
            # if zipcode != '' and zipcode != None:
            #     submit['zipcode'] = zipcode
            #     return submit
        except:
            pass
    changer.restart()

def write_status(path,workbook,submit,content):
    book2 = copy(workbook)
    sheet2 = book2.get_sheet(0) 
    col = int(str(submit['Mission_Id'])[-1])+12
    print(col)
    sheet2.write(submit['row'],col,content)
    book2.save(path)

def mission(plans):
    for plan in plans:
        try:
            reg_part(plan)
        except Exception as e:
            a = traceback.format_exc()
            print(a)
            print('timeout')            

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
    sheet,workbook = get_excel(path)    
    submit = get_one_data(sheet,plan['Mission_Id'])
    submit['status'] = 'using'
    submit['Site'] = plan['url_link']
    submit['Mission_Id'] = plan['Mission_Id']
    print('reg_part')
    write_status(path,workbook,submit,'using')
    module = 'Mission_'+str(plan['Mission_Id'])
    Module = ''
    try:
        Module = importlib.import_module(module)
    except:
        pass
    try:
        change_ip(submit)
        print('----------------====================')
        chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
        print('========')
        if Module != '':
            submit = Module.web_submit(submit,chrome_driver=chrome_driver)
        else:
            thread_tokill.web_submit(submit,chrome_driver,debug=0)
        # if submit['status'] == 'No sign':
        writelog(chrome_driver,submit)
        # print(submit)
    except Exception as e:
        # traceback.format_exc()
        try: 
            writelog(chrome_driver,submit)
            print('==========++++')
        except Exception as e:
            print(str(e))
            # traceback.format_exc()
    # content = get_write_content(submit)
    content = json.dumps(submit)
    write_status(path,workbook,submit,content)
    try:
        chrome_driver.close()
        chrome_driver.quit()
    except:
        pass
    submit['status'] = 'badname'
    for i in submit['badname']:
        submit['row'] = i
        write_status(path,workbook,submit,'badname')          

def main():
    # while True:
    for i in range(1):
        try:
            tools.killpid()
        except Exception as e:
            print(str(e))
            pass
        account = db.get_account()
        plan_id = account['plan_id']
        # print('Plan_id:',plan_id,',connecting sql for plan info...')
        try:
            plans = db.read_plans(plan_id)
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
        mission(plans)
        print('All Missions finished..............')
        try:
            print('try killing pids')
            tools.killpid()
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
        submit['status'] = 'using'
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
    i = 0
    if i == 0:
        main()
    else:
        test()