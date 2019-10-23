import random
from time import sleep
import db
import Chrome_driver
import luminati
import imap_test
import importlib
from wrapt_timeout_decorator import *


@timeout(600)
def reg_part(Config):
    while True:
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
        flag = luminati.ip_test(submit['port_lpm'],state=submit['state_'] ,country='')
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
    module = 'Mission_'+str(submit['Mission_Id'])
    Module = importlib.import_module(module)
    flag = 0
    try:
        print('----------------====================')
        chrome_driver = Chrome_driver.get_chrome(submit)
        flag = Module.web_submit(submit,chrome_driver=chrome_driver)
        print(submit)
    except Exception as e:
        print(str(e))
    try:
        chrome_driver.close()
        chrome_driver.quit()
    except:
        pass
    if flag == 1:
        mission_check = {}
        try:
            mission_check = db.check_mission_status(submit)
        except:
            pass
        if len(mission_check) == 0:
            print('Mission: ',submit['Mission_Id'],'success,uploading db')
            db.write_one_info([str(submit['Mission_Id'])],submit)
    print('Mission_Id:',submit['Mission_Id'],'finished')

def multi_reg(Config):  
    # print(Config)
    return_rand = random.randint(0,5)
    if return_rand == 0:
        print('unique  random,return for Mission_Id:',Config)
    else:
        time_cheat = random.randint(0,10)
        print(Config)
        if Config['Alliance'] != 'Test':
            print('Sleep for random time:',time_cheat*60,'-------------')   
            if Config['Mission_Id'] != '20000':
                sleep(time_cheat*60)
        else:
            print('test...........')
        reg_part(Config)
    return  