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

def get_one_data(sheet,Mission_Id):
    rows = sheet.nrows
    print(rows)
    # list_rows = random.sample(range(rows),rows)    
    for i in range(rows-1):
        if i==0:
            keys = sheet.row_values(i)
            continue
        values = sheet.row_values(i)
        submit = dict(zip(keys,values))
        print(submit)  
        key = 'Status_'+ str(Mission_Id)
        if submit[key] == '':
            submit['row'] = i
            return submit

def change_ip(submit):
    country = submit['Country']
    for i in range(3):
        try:
            zipcode = ip_test.ip_Test('',state = '',country=country )
            if zipcode != '' and zipcode != None:
                submit['zipcode'] = zipcode
                return submit
        except:
            pass
    changer.restart()


def write_status(path,workbook,submit):
    book2 = copy(workbook)
    sheet2 = book2.get_sheet(0) 
    col = int(str(submit['Mission_Id'])[-1])+11
    print(col)
    sheet2.write(submit['row'],col,submit['status'])
    book2.save(path)

def mission(plans):
    for plan in plans:
        try:
            reg_part(plan)
        except TimeoutError:
            print('timeout')            

# @timeout(600)
def reg_part(plan):
    path = r'..\res\Dadao.xlsx'
    sheet,workbook = get_excel(path)    
    submit = get_one_data(sheet,plan['Mission_Id'])
    submit['status'] = 'using'
    submit['Site'] = plan['url_link']
    submit['Mission_Id'] = plan['Mission_Id']
    print('reg_part')
    write_status(path,workbook,submit)    
    module = 'Mission_'+str(plan['Mission_Id'])
    Module = importlib.import_module(module)
    try:
        change_ip(submit)
        print('----------------====================')
        chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
        print('========')
        status = Module.web_submit(submit,chrome_driver=chrome_driver)
        submit['status'] = status
        if status == 2:
            writelog(chrome_driver,submit)
        write_status(path,workbook,submit)
        print(submit)
    except Exception as e:
        traceback.format_exc()
        print(str(e))
        try:
            print('==========++++')
            writelog(chrome_driver,submit)  
        except Exception as e:
            print(str(e))
            traceback.format_exc()
    try:
        chrome_driver.close()
        chrome_driver.quit()
    except:
        pass


def main():
    while True:
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



if __name__ == '__main__':
    main()