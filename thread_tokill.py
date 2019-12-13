import json
import random
import ip_test
import Changer_windows_info as changer
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
import threadpool
import threading
import qt
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import selenium_funcs
import Submit_handle
import time





pool = threadpool.ThreadPool(10)
timezone = ''
using_num = 0

def makedir_account(path):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)

def writelog(chrome_driver,submit,content=''):
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
        if content == '':
            content = traceback.format_exc()            
        db.write_log_db(Mission_Id,content,png)

        # file_ = r'..\log\log.txt'
        # content = str(datetime.datetime.now())
        # with open(file_,'a+') as f:
        #     content += '\n'
        #     f.write(content)          
        # traceback.print_exc(file=open(file_,'a+'))          
        # print(sys._getframe().f_lineno, 'traceback.print_exc():',traceback.print_exc())        
        # print(e.__traceback__.tb_frame.f_globals["__file__"])   # 发生异常所在的文件
        # print(e.__traceback__.tb_lineno)                        # 发生异常所在的行数    

def start(plans):
    print('Start func')
    if plans[0]['sleep_flag'] == 2:
        multi_reg(plans[0]) 
    else:
        requests = threadpool.makeRequests(multi_reg, plans)
        [pool.putRequest(req) for req in requests]
        pool.wait()     

def change_tz(windows_):
    global using_num
    while True:
        if using_num == 0:
            print('=========================')
            print('=========================')
            print('Change system timezone..............')            
            command = 'tzutil /s \"%s\"'%windows_
            os.system(command)
            using_num += 1
            return
        else:
            sleep(10)
            print('waiting tz')

def get_submit(Config):
    submit = {}
    while True:
        for item in submit:
            if 'BasicInfo_Id' in submit:
                db.update_flag_use(submit[item]['BasicInfo_Id'])   
                break        
            # print('getting data')
        try:
            print(Config)
            submit = db.get_luminati_submit(Config)           
            if submit == {}:
                content = 'No data found'
                qt.main(1,content)
                return None
            # print(submit)
            # return
            if Config['Alliance'] == 'Test':
                submit['state_'] = ''
            # print('Data for this mission:')
            # print(submit)
        except Exception as e:
            print(str(e))
            print('Get data wrong..................................')
            return None
        if submit['Excels_dup'][1] != '':
            print('testing email.........')
            flag = imap_test.Email_emu_getlink(submit['Email'])
            if flag == 0:
                # print('Bad email:',submit['Email']['Email_emu'])
                db.updata_email_status(submit['Email']['Email_Id'],0)
                continue
            elif flag == 1:
                # print("Good email")
                db.updata_email_status(submit['Email']['Email_Id'],1)
            else:
                # print('Loging email server failed,find another email')
                continue
        else:
            pass 
        print('refreshing ip.............') 
        if submit['sleep_flag'] != 2:
            # flag,proxy_info = luminati.ip_test(submit['port_lpm'],state=submit['state_'] ,country=submit['Country'])
            flag,proxy_info = luminati.ip_test(submit['port_lpm'],state='' ,country=submit['Country'])            
        else:
            for num_ip in range(6):
                try:
                    city = ip_test.ip_Test('','',country=submit['Country'])
                    if  city != 'Not found':
                        flag = 1
                        proxy_info = ''
                        break
                    if num_ip == 5:
                        print('Net wrong...!!!!!!')
                        changer.Restart()
                except:
                    changer.Restart()            

        # changing IP
        print(flag,'=========================')
        if flag == 1:
            break
        elif flag == -1:
            # print('bad port,change into new')
            luminati.delete_port_s(submit['port_lpm'])            
            port_new = luminati.get_port_random()
            db.update_port(submit['port_lpm'],port_new)
            Config['port_lpm'] = port_new
            # print(port_new)
            try:
                proxy_config_name_list = ['jia1','jia2'] 
                num_proxy = random.randint(0,1)
                luminati.add_proxy(port_new,country=submit['Country'],proxy_config_name=proxy_config_name_list[num_proxy],ip_lpm=submit['ip_lpm'])
            except Exception as e:
                print(str(e))
            continue
        else:
            continue
    return submit,proxy_info  

def data_handler(Config):
    print('data_handler')
    global timezone 
    global using_num    
    submit,proxy_info = get_submit(Config)
    if submit == None:
        return None
        # print('Reading config from sql server success')
    if submit['sleep_flag'] != 2: 
        submit['tz'] = db.get_cst_zone(proxy_info['geo']['tz'])
    # print("proxy_info['geo']['tz']:",proxy_info['geo']['tz'])
    # print(str(submit['Mission_Id']),'get timezone for ',submit['Country'],'is',submit['tz'])
    # print("timezone:",timezone)
    # print("using_num:",using_num) 
        print('submit[tz]:',submit['tz'])  
        if submit['tz'][0]['windows'] != timezone:
            change_tz(submit['tz'][0]['windows'])
            timezone = submit['tz'][0]['windows']
            print("timezone:",timezone)
            print("using_num:",using_num)
        else:
            using_num += 1 

    print("Mission started,using_num:",using_num)
    try:
        reg_part_(submit)
    except TimeoutError:
        print('timeout')
    using_num = using_num - 1  
    print("Mission finished,using_num:",using_num)
    print("timezone:",timezone) 
    flag = db.get_plan_status(submit['ID'])
    if flag != 0:
        mission_check = {}
        try:
            mission_check = db.check_mission_status(submit)
        except:
            pass
        if len(mission_check) == 0:
            submit['Status'] = flag
            print('Mission: ',submit['Mission_Id'],'success,uploading db')
            db.write_one_info([str(submit['Mission_Id'])],submit)
    for item in submit:
        print(item)
        if 'BasicInfo_Id' in submit[item]:
            db.update_flag_use(submit[item]['BasicInfo_Id'])
            break

    print('Mission_Id:',submit['Mission_Id'],'finished') 
    return 1       

# @timeout(600)
def reg_part_(submit):
    print('reg_part')
    global timezone 
    global using_num    
    submit['Record'] = 0
    Module = ''    
    if submit['Record'] == 0:
        try:
            module = 'Mission_'+str(submit['Mission_Id'])
            Module = importlib.import_module(module)
        except Exception as e:
            print(str(e))
    else:
        Module = ''    
    try:
        print('----------------====================')
        if submit['sleep_flag'] == 2:
            submit.pop('ip_lpm')
        chrome_driver = Chrome_driver.get_chrome(submit)
        print('========')
        if Module != '':
            print('11111111111111')
            print(Module)
            Module.web_submit(submit,chrome_driver=chrome_driver)
        else:
            print('Record modern')
            web_submit(submit,chrome_driver=chrome_driver)
        print(submit)
    except Exception as e:
        print(str(e))
        try:
            writelog(chrome_driver,submit)  
        except:
            pass
    try:
        chrome_driver.close()
        chrome_driver.quit()
    except:
        pass

def web_submit(submit,chrome_driver,debug=0):
    # predefine Mission
    # Excel_tag = 'Auto'    
    # num_html = 1
    # Mission_Id = 10046

    # if debug == 1:
    #     site = 'http://tracking.axad.com/aff_c?offer_id=181&aff_id=2138'
    #     submit['Site'] = site
    Page_flags = db.get_page_flag(submit['Mission_Id'])
    print(Page_flags)    
    print('============')
    print(submit['Site'])
    chrome_driver.get(submit['Site'])
    print('Load finish')
    # old_page = chrome_driver.find_element_by_tag_name('html')
    # print(old_page.id)
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    handle = chrome_driver.current_window_handle
    while True:
        '''
        turn to other page
        '''
        handles=chrome_driver.window_handles   
        for i in handles:
            if i != handle:        
                chrome_driver.switch_to.window(i)  
        '''
        detect page flag,if find ,continue,if not return
        '''
        page = page_detect(Page_flags,chrome_driver)
        if page == None:
            print('Looking for flag and Timeout or bad page')
            qt.main(1,content)            
            return
        elif page == '':
            content = 'New Page'
            writelog(chrome_driver,submit,content='')
            qt.main(1,content)
            return
        print('Find target_page:',page['Page'])
        '''
        save html
        '''
        save_html(chrome_driver,submit['Mission_Id'],page['Page'])
        '''
        get and sort page config
        '''
        config = db.get_page_config(submit['Mission_Id'],page['Page'])
        config.sort(key=takeStep)
        print(config)
        for item in submit:
            print(item)
            try:
                if 'BasicInfo_Id' in submit[item]:
                    key_excel = item
                    print('find excel name:',key_excel)
                    break
            except:
                pass
        '''
        find all xpaths for every step
        '''
        xpaths = []
        for config_ in config:
            print(config_)
            config_['General'] = json.loads(config_['General'])              
            xpaths.append(config_['General']['xpath']) 
        print(xpaths)
        '''
        check step status for every step
        '''
        step_detect(chrome_driver,xpaths) 
        print('All steps ready')
        '''
        stop window if every step is ready
        '''
        chrome_driver.execute_script("window.stop();")            
        wait = WebDriverWait(chrome_driver,1)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH,'aaaaaaaa')))
        except Exception as e:
            print(str(e))
        chrome_driver.maximize_window()                
        print('Stop loading')         
        # chrome_driver.get('https://www.baidu.com')
        # sleep(3000)
        # chrome_driver.execute_script("window.stop();")
        # chrome_driver.find_element_by_xpath(page['Flag_xpath']).click()
        # ActionChains(chrome_driver).key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()
        sleep(3)       

        '''
        do step by config
        '''
        for config_ in config:
            try:
                selenium_funcs.get_action(chrome_driver,config_,submit[key_excel])
                sleep(1)
            except Exception as e:
                a = traceback.format_exc()            
                print(a)
        '''
        check page flag status,if changed,continue
        '''
        flag_page_chane = page_change(chrome_driver,page)
        if flag_page_chane == 1:
            pass
        else:
            return
        if 'Almost' in page['Status']:
            db.update_plan_status(1,submit['ID'])
        if 'Finish' in page['Status']:
            db.update_plan_status(2,submit['ID'])
            return        

def takeStep(elem):
    return elem['Step']

def get_page_by_flag(Page_flags,chrome_driver):
    target_page = None
    for page in Page_flags:
        try:
            if page['Flag_xpath'] == '':
                chrome_driver.find_element_by_text(page['Flag_text'])
                print('find target page:',page['Page'],'with text')                                
                target_page = page
                break                                
            element = chrome_driver.find_element_by_xpath(page['Flag_xpath'])
            # print(page,'find text:',element.text)
            if EC.text_to_be_present_in_element(element,page['Flag_text']):
                print('find target page:',page['Page'],'with xpath and text')
                target_page = page
                break
            else:
                chrome_driver.find_element_by_text(page['Flag_text'])
                print('find target page:',page['Page'],'with text')                
                target_page = page
                break                
        except Exception as e:
            print(str(e))
    return target_page

def page_detect(Page_flags,chrome_driver):
    page = None
    for i in range(60):
        page = get_page_by_flag(Page_flags,chrome_driver)
        if page == None:
            print('Page Flag Not Found,',i+1)
            sleep(3)
        else:
            print('Page Flag Found')            
            break
        status = chrome_driver.execute_script("return document.readyState")
        print('document status:',status)
        wrong_pages = ['Webpage not available','This page isn’t working']
        flag_wrong_page = 0
        if status == 'complete':
            for wrong_page in wrong_pages:
                if wrong_page in chrome_driver.page_source :
                    print('wrong_page:',wrong_page)
                    flag_wrong_page = 1
                    break
            if flag_wrong_page == 0:
                page = ''
                break
            else:
                page = None
                break
    return page

def page_change(chrome_driver,page):
    print(page)
    flag = 0
    for i in range(360):        
        if EC.text_to_be_present_in_element((By.XPATH,page['Flag_xpath']),page['Flag_text']):
            sleep(1)
        else:
            flag = 1
            break
    if flag == 1:
        print('page changed')
        return 1
    else:
        print('timeout')
        return 0

def step_detect(chrome_driver,xpaths):
    for xpath in xpaths:
        WebDriverWait(chrome_driver,120).until(EC.visibility_of_element_located((By.XPATH,xpath)))
        print('xpath:',xpath,'ready')

def save_html(chrome_driver,Mission_Id,page):
    print('Title',chrome_driver.title)
    print('url',chrome_driver.current_url)    
    path_html = r'..\html'
    file = str(page)+'.html'
    path_folder = os.path.join(path_html,str(Mission_Id))
    Submit_handle.makedir_pic(path_folder)    
    path_file = os.path.join(path_folder,file)
    # html=chrome_driver.page_source
    html = chrome_driver.execute_script("return document.documentElement.outerHTML")    
    with open(path_file,mode="w",encoding="utf-8") as f:
        f.write(html) 

def multi_reg(Config):
    # print(Config)
    print('multi_reg')
    return_rand = random.randint(0,5)
    if return_rand == 0:
        print('unique  random,return for Mission_Id:',Config)
        if Config['sleep_flag'] != 2:
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
        flag = data_handler(Config)
        if flag == None:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')            
            print('Mission',Config['Mission_Id'],'is out of data............')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')            
    return  

def test():
    stopLoading()    

