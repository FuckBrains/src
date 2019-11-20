import random
from time import sleep
import db
import Chrome_driver
import luminati
import imap_test
import importlib
from wrapt_timeout_decorator import *
import traceback
import sys
import datetime
import os
import globalvar as gl


timezone = ''
using_num = 0

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

        # file_ = r'..\log\log.txt'
        # content = str(datetime.datetime.now())
        # with open(file_,'a+') as f:
        #     content += '\n'
        #     f.write(content)          
        # traceback.print_exc(file=open(file_,'a+'))          
        # print(sys._getframe().f_lineno, 'traceback.print_exc():',traceback.print_exc())        
        # print(e.__traceback__.tb_frame.f_globals["__file__"])   # 发生异常所在的文件
        # print(e.__traceback__.tb_lineno)                        # 发生异常所在的行数    


def change_tz(windows_):
    global using_num
    while True:
        if using_num == 0:
            command = 'tzutil /s \"%s\"'%windows_
            os.system(command)
            using_num += 1
            return
        else:
            sleep(10)


def data_handler(Config):
    submit = {}
    while True:
        if 'BasicInfo_Id' in submit:
            db.update_flag_use(submit['BasicInfo_Id'])           
        print('getting data')
        try:
            submit = db.get_luminati_submit(Config)
            print(submit)
            # return
            if Config['Alliance'] == 'Test':
                submit['state_'] = ''
            # print('Data for this mission:')
            # print(submit)
        except Exception as e:
            print(str(e))
            print('Get data wrong..................................')
            return
        if submit['Excels_dup'][1] != '':
            print('testing email.........')
            flag = imap_test.Email_emu_getlink(submit['Email'])
            if flag == 0:
                print('Bad email:',submit['Email']['Email_emu'])
                db.updata_email_status(submit['Email']['Email_Id'],0)
                continue
            elif flag == 1:
                print("Good email")
                db.updata_email_status(submit['Email']['Email_Id'],1)
            else:
                print('Loging email server failed,find another email')
                continue
        else:
            pass 
        print('refreshing ip.............')      
        flag,proxy_info = luminati.ip_test(submit['port_lpm'],state=submit['state_'] ,country=submit['Country'])
        print(flag,'=========================')
        if flag == 1:
            break
        elif flag == -1:
            print('bad port,change into new')
            luminati.delete_port_s(submit['port_lpm'])            
            port_new = luminati.get_port_random()
            db.update_port(submit['port_lpm'],port_new)
            Config['port_lpm'] = port_new
            print(port_new)
            try:
                luminati.add_proxy(port_new,country=submit['Country'],proxy_config_name='jia1',ip_lpm=submit['ip_lpm'])
            except Exception as e:
                print(str(e))
            continue
        else:
            continue
        print('Reading config from sql server success')
    submit['tz'] = db.get_cst_zone(proxy_info['geo']['tz'])
    print("proxy_info['geo']['tz']:",proxy_info['geo']['tz'])
    print(str(submit['Mission_Id']),'get timezone for ',submit['Country'],'is',submit['tz'])
    global timezone 
    global using_num
    print("timezone:",timezone)
    print("using_num:",using_num)    
    if submit['tz'][0]['windows'] != timezone:
        change_tz(submit['tz'][0]['windows'])
        timezone = submit['tz'][0]['windows']
        print("timezone:",timezone)
        print("using_num:",using_num)
    else:
        using_num += 1 
    print("Mission started,using_num:",using_num)            
    try:
        reg_part(submit)
    except TimeoutError:
        print('timeout')
    using_num = using_num - 1  
    print("Mission finished,using_num:",using_num)    
    print("timezone:",timezone)    
    flag = gl.get_value(submit['ID'])
    print('Status in thread_tokill:',flag)
    print("submit['ID']",submit['ID'])
    if flag != 2:
        mission_check = {}
        try:
            mission_check = db.check_mission_status(submit)
        except:
            pass
        if len(mission_check) == 0:
            print('Mission: ',submit['Mission_Id'],'success,uploading db')
            db.write_one_info([str(submit['Mission_Id'])],submit)
    if 'BasicInfo_Id' in submit:
        db.update_flag_use(submit['BasicInfo_Id'])
    print('Mission_Id:',submit['Mission_Id'],'finished')        



@timeout(3)
def reg_part(submit):
    global timezone 
    global using_num    

    module = 'Mission_'+str(submit['Mission_Id'])
    Module = importlib.import_module(module)
    try:
        print('----------------====================')
        chrome_driver = Chrome_driver.get_chrome(submit)
        Module.web_submit(submit,chrome_driver=chrome_driver)
        print(submit)
    except Exception as e:
        writelog(chrome_driver,submit)  
    try:
        chrome_driver.close()
        chrome_driver.quit()
    except:
        pass



def multi_reg(Config):  
    # print(Config)
    return_rand = random.randint(0,5)
    if return_rand == 0:
        print('unique  random,return for Mission_Id:',Config)
        time_return = random.randint(0,600)
        sleep(time_return)
    else:
        time_cheat = random.randint(0,600)
        # print(Config)
        if Config['Alliance'] != 'Test':
            if Config['Mission_Id'] != '20000':
                if Config['sleep_flag'] == 1:
                    print('Sleep for random time:',time_cheat,'-------------')                       
                    sleep(time_cheat)
        else:
            print('test...........')
        data_handler(Config)
    return  