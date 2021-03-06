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
# import qt
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import selenium_funcs
import Submit_handle
import time
import time_related
import Dadao





pool = threadpool.ThreadPool(7)
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
        path_ = os.path.join(path_,str(submit['Mission_Id']))        
        makedir_account(path_)        
        start = time_related.Time_start()
        start = str(start)
        after = start.split('.')[0].replace(':','-')        
        pic_name = str(submit['Mission_Id'])+'_'+after+'.png'
        pic = os.path.join(path_,pic_name)
        print(pic)
        try:
            chrome_driver.save_screenshot(pic)
            print('pic saved success')
        except Exception as e:
            print(str(e))
        if content == '':
            content = traceback.format_exc()  
            print('traceback.format_exc():' ,content)  
            if content == '':
                content = 'NO traceback'        
        # if submit['Excels_dup'][0] == 'Dadao':
        #     status = db.get_plan_status(submit['ID'])
        #     path = submit['Dadao']['path']
        #     sheet,workbook = Dadao.get_excel(path)   
        #     content = 'Mission Status:'+str(status)+'\n'+'traceback:\n    '+content        
        #     Dadao.write_status(path,workbook,submit['Dadao'],content)            
        #     return            
        with open(pic,'rb') as f:
            png = f.read()
        Mission_Id = submit['Mission_Id']
        if 'badstep' in submit:
            content+='\n'+submit['badstep']
        db.write_log_db(Mission_Id,content,png)
        # file_ = r'..\log\log.txt'
        # content = str(datetime.datetime.now())
        # with open(file_,'a+') as f:
        #     content += '\n'
        #     f.write(content)          
        # traceback.print_exc(file=open(file_,'a+'))          
        # print(sys._getframe().f_lineno, 'traceback.print_exc():',traceback.print_exc())        
        # print(e.__traceback__.tb_frame.f_globals["__file__"])   # ???????????????????????????
        # print(e.__traceback__.tb_lineno)                        # ???????????????????????????    

def start(plans):
    print('Start func')
    print(len(plans),'plans found')
    if plans[0]['sleep_flag'] == 2:
        for num_ip in range(6):
            try:
                city = ip_test.ip_Test('','',country=plans[0]['Country'])
                if  city != 'Not found':
                    flag = 1
                    proxy_info = ''
                    break
                if num_ip == 5:
                    print('Net wrong...!!!!!!')
                    changer.Restart()
            except:
                changer.Restart()     
        for plan in plans:
            plan['city'] = city
            print('911 city:',city) 
    for i in range(len(plans)):
        plans[i]['count'] = i
    print(len(plans),'after set count')
    print(plans)
    print('=====================')
    print('=====================')
    print('=====================')
    print('=====================')
    requests = threadpool.makeRequests(multi_reg, plans)
    [pool.putRequest(req) for req in requests]
    pool.wait()     

def change_tz(windows_):
    # return
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
            # sleep(15)            
            break
            # print('waiting tz')

def read_same_config_num():
    Offer_configs = {}
    with open(r'ini\same_config.ini') as f:
        lines = f.readlines()
        alias = {}
        for line in lines:
            if ',' in line:
                config = line.split(',')                
                alias[str(config[0])] = str(config[1])
    # print(Offer_configs)
    return alias

def get_submit(Config):
    submit = {}
    while True:
        for item in submit:
            if 'BasicInfo_Id' in submit:
                db.update_flag_use(submit[item]['BasicInfo_Id'])   
                break        
            # print('getting data')
        try:
            print('Config',Config)
            submit = db.get_luminati_submit(Config)           
            if submit == {}:
                content = 'No data found'
                # qt.main(1,content)
                return None
            # print(submit)
            # return
            if Config['Alliance'] == 'Test':
                submit['state_'] = ''
            # print('Data for this mission:')
            # print(submit)
        except Exception as e:
            content = traceback.format_exc()  
            print('traceback.format_exc():' ,content)              
            print('Get data wrong..................................')
            return None
        if submit['Excels_dup'][1] != '':
            print('testing email.........')
            flag_email = 0
            try:
                flag_email = imap_test.Email_emu_getlink(submit['Email'])
            except:
                continue
            if flag_email == 0:
                # print('Bad email:',submit['Email']['Email_emu'])
                db.updata_email_status(submit['Email']['Email_Id'],0)
                continue
            elif flag_email == 1:
                # print("Good email")
                db.updata_email_status(submit['Email']['Email_Id'],1)
            else:
                # print('Loging email server failed,find another email')
                continue
        else:
            pass 
        flag = 0
        if submit['sleep_flag'] != 2 and submit['sleep_flag'] != 3:
            print('refreshing ip.............') 
            # flag,proxy_info = luminati.ip_test(submit['port_lpm'],state=submit['state_'] ,country=submit['Country'])
            flag,proxy_info = luminati.ip_test(submit['port_lpm'],state='' ,country=submit['Country'])            
            print('proxy_info:',proxy_info)
            if len(proxy_info)>=1:
                submit['ip_record'] = proxy_info['ip']
            else:
                submit['ip_record'] = ''                
        else:
            city = ''
            proxy_info = {}
            flag = 1  
            submit['ip_record'] = ''      
        # changing IP
        print(flag,'=========================')
        if flag == 1:
            break
        elif flag == -1:
            # print('bad port,change into new')
            for i in range(5):
                try:
                    flag_delete = luminati.delete_port_s(submit['port_lpm']) 
                    if flag_delete == 1:
                        break           
                    else:
                        continue
                except:
                   pass
            port_new = luminati.get_port_random()
            print('port_new:',port_new)
            db.update_port(submit['ID'],port_new)
            print('update port success')
            Config['port_lpm'] = port_new
            # print(port_new)
            try:
                # proxy_config_name_list = ['jia1','jia2'] 
                # num_proxy = random.randint(0,1)
                luminati.add_proxy(port_new,country=submit['Country'],proxy_config_name=submit['zone'],ip_lpm=submit['ip_lpm'],Mission_Id=submit['Mission_Id'])
            except Exception as e:
                a = traceback.format_exc()
                print(a)
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
    print('Proxy:',proxy_info)
    lum_list = [0,1,4]
    if submit['sleep_flag'] in lum_list: 
        submit['tz'] = db.get_cst_zone(proxy_info['geo']['tz'])
    # print("proxy_info['geo']['tz']:",proxy_info['geo']['tz'])
    # print(str(submit['Mission_Id']),'get timezone for ',submit['Country'],'is',submit['tz'])
    # print("timezone:",timezone)
    # print("using_num:",using_num) 
        print('submit[tz]:',submit['tz'])  
        if len(submit['tz']) == 0:
            submit['tz'] = [{'windows':'West Pacific Standard Time'}]
        if submit['tz'][0]['windows'] != timezone:
            change_tz(submit['tz'][0]['windows'])
            timezone = submit['tz'][0]['windows']
            print("timezone:",timezone)
            print("using_num:",using_num)
        else:
            using_num += 1 
    print("Mission started,using_num:",using_num)
    if str(submit['Mission_Id']) == '11001':
        try:
            reg_part_(submit)
        except TimeoutError:
            print('timeout')
    else:
        try:
            reg_part_cpl(submit)
        except TimeoutError:
            print('timeout')   
    if submit['Excels_dup'][0] == 'Dadao':
        return 1
    using_num = using_num - 1  
    print("Mission finished,using_num:",using_num)
    print("timezone:",timezone) 
    flag = db.get_plan_status(submit['ID'])
    if flag != 0:
        # mission_check = {}
        # try:
        #     mission_check = db.check_mission_status(submit)
        # except:
        #     pass
        # if len(mission_check) == 0:
        submit['Status'] = flag
        print('Mission: ',submit['Mission_Id'],'success,uploading db')
        db.write_one_info([str(submit['Mission_Id'])],submit)
    for item in submit:
        print(item)
        if type(submit[item]) == type({}):
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
    # submit['Record'] = 0
    Module = ''    
    # if str(submit['Record']) == '0':
    #     try:
    #         module = 'Mission_'+str(submit['Mission_Id'])
    #         Module = importlib.import_module(module)
    #     except Exception as e:
    #         print(str(e))
    # else:
    #     Module = ''  
    # print('Module is :',Module)  
    try:
        if submit['sleep_flag'] == 2 or submit['sleep_flag'] == 3:
            submit.pop('ip_lpm')
        print(submit)
        chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
        same_config = read_same_config_num()
        if str(submit['Mission_Id']) in same_config:
            Mission_Id = same_config[str(submit['Mission_Id'])].replace('\n','')
        else:
            Mission_Id = str(submit['Mission_Id'])
        Page_flags = db.get_page_flag(Mission_Id)
        if len(Page_flags) == 0:
            print('No Page_flags found in db,try import module from src')
            module = 'Mission_'+str(Mission_Id)
            Module = importlib.import_module(module)            
            chrome_driver = Module.web_submit(submit,chrome_driver=chrome_driver)
        else:
            submit['Page_flags'] = Page_flags
            print('Page_flags found,use Record modern')
            chrome_driver = web_submit(submit,chrome_driver=chrome_driver)
        print(submit)
        # if submit['Excels_dup'][0] == 'Dadao':
        #     writelog(chrome_driver,submit)
    except Exception as e:
        print(str(e))
        try:
            writelog(chrome_driver,submit)  
        except:
            pass
        return
    import Mission_11002
    print('Import Mission_11002')
    try:
        Mission_11002.test(chrome_driver)
    except:
        pass
    try:
        chrome_driver.close()
        chrome_driver.quit()
    except:
        pass

@timeout(900)
def reg_part_cpl(submit):
    print('reg_part')
    global timezone 
    global using_num    
    # submit['Record'] = 0
    Module = ''    
    try:
        Mission_Id = submit['Mission_dir'].split(',')[0][-5:]
        same_config = read_same_config_num()
        if str(submit['Mission_Id']) in same_config:
            Mission_Id = same_config[str(submit['Mission_Id'])].replace('\n','')
            submit['same_config'] = Mission_Id
        else:
            Mission_Id = str(submit['Mission_Id'])         
        if submit['sleep_flag'] == 2 or submit['sleep_flag'] == 3:
            submit.pop('ip_lpm')
        print(submit)
        Page_flags = db.get_page_flag(Mission_Id)        
        print('Page_flags:',Page_flags)
        if len(Page_flags) == 0:
            print('No Page_flags found in db,try import module from src')
            chrome_driver = Chrome_driver.get_chrome(submit)
            module = 'Mission_'+str(Mission_Id)
            Module = importlib.import_module(module)            
            chrome_driver = Module.web_submit(submit,chrome_driver=chrome_driver)
        else:
            pic = 0
            for page in Page_flags:
                if page['Page']=='1':
                    pic = page['Pic'] 
            if submit['sleep_flag'] == 5:
                print('Modern 5:finding cookie for this session')
                cookies = luminati.get_lpm_cookie(submit['port_lpm'],submit['Site'],submit['ua'])
                if len(cookies) == 0:
                    return 
                submit['cookies_lpm'] = cookies
                submit.pop('ip_lpm')
            if submit['zone'] == 'jia10':
                chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
            else:
                chrome_driver = Chrome_driver.get_chrome(submit,pic=0)                
            submit['Page_flags'] = Page_flags
            print('Page_flags found,use Record modern')
            chrome_driver = web_submit(submit,chrome_driver=chrome_driver)
        print(submit)
        # if submit['Excels_dup'][0] == 'Dadao':
        #     writelog(chrome_driver,submit)
    except Exception as e:
        print(str(e))
        try:
            writelog(chrome_driver,submit)  
        except:
            pass
    # chrome_driver.delete_all_cookies()
    close_list = [3,4]
    if submit['sleep_flag'] not in close_list:
        print('try to close chrome')
        try:
            chrome_driver.close()
            chrome_driver.quit()
        except:
            pass
    else:
        sleep(3000)

def web_submit(submit,chrome_driver,debug=0):
    # predefine Mission
    # Excel_tag = 'Auto'    
    # num_html = 1
    # Mission_Id = 10046
    # if debug == 1:
    #     site = 'http://tracking.axad.com/aff_c?offer_id=181&aff_id=2138'
    #     submit['Site'] = site
    if 'remote' not in submit:
        Page_flags = submit['Page_flags']
        Page_flags = [item for item in Page_flags if item['Country'] == submit['Country']]    
        print(Page_flags) 
        print('============')
        print(submit['Site'])
        if '/>' in submit['Site']:
        # html =html_1.replace('"','\\"').replace("'","\\'") 
            js = 'document.writeln("'+submit['Site']+'");'
            print(js)
            chrome_driver.execute_script(js)
        # return
        else:
            submit['Site'] = submit['Site'].replace('\\n','')
            chrome_driver.get(submit['Site'])
    # chrome_driver.refresh()
    if submit['sleep_flag'] == 5:
        chrome_driver.delete_all_cookies()
        for k,v in submit['cookies_lpm'].items():
            # ?????????????????????
            chrome_driver.add_cookie({"name":k,"value":v})
            # ?????????????????????
            # brows.add_cookie({"domain": ".tyrz.gd.gov.cn", "name": k, "value": v, "path": "/"})
        chrome_driver.get(submit['Site'])
        cookies = chrome_driver.get_cookies()
        print(type(cookies))
        cookie_str = json.dumps(cookies)  
        print(cookie_str)       
    sleep(5)
    print('Load finish')
    # old_page = chrome_driver.find_element_by_tag_name('html')
    # print(old_page.id)
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    flag_refresh = 0
    # for i in range(20):
    page_done = []
    while True:
        '''
        turn to other page
        '''

        '''
        detect page flag,if find ,continue,if not return
        '''
        handle = chrome_driver.current_window_handle
        submit['handle'] = handle
        if 'remote' not in submit:
            page = page_detect(Page_flags,chrome_driver)
            if page == None:
                content = 'Looking for flag and Timeout or bad page'
                print(content)
                # qt.main(1,content)            
                return chrome_driver
            elif page == '':
                content = 'New Page'
                # writelog(chrome_driver,submit,content)
                # qt.main(1,content)
                return chrome_driver
            print('Find target_page:',page['Page'])
            if page['Page'] in page_done:
                return chrome_driver
        else:
            page = submit['Page']
        '''
        save html
        '''
        # save_html(chrome_driver,submit['Mission_Id'],page['Page'])
        '''
        get and sort page config
        '''
        if flag_refresh == 0:     
            Mission_Id = submit['Mission_dir'].split(',')[0][-5:]  
            if 'same_config' in submit:
                Mission_Id = submit['same_config'] 
            configs = db.get_page_config(Mission_Id,page['Page'])
            configs.sort(key=takeStep)
            print(configs)
            '''
            find all xpaths for every step
            '''
            # xpaths = []
            for config_ in configs:
                print(config_)
                config_['General'] = json.loads(config_['General'])   
        #     if config_['Action'] not in ['Set_Status','Set_Sleep'] :
        #         xpaths.append(config_['General']['xpath']) 
        # print(xpaths)
        '''
        check step status for every step
        '''
        # if len(xpaths) !=0:
        #     iframe = config_['General']['iframe']
        # step_detect(chrome_driver,configs) 
        sleep(3)
        # print('All steps ready')
        '''
        stop window if every step is ready
        '''
        # if submit['Excels_dup'][0] != 'Dadao':
        #     chrome_driver.execute_script("window.stop();")            
        # else:
        # for i in range(180):
        #     status = chrome_driver.execute_script("return document.readyState")
        #     if status != 'complete':
        #         print('document status:',status)
        #         sleep(1)
        #     else:
        #         print('document status:',status)
        #         break            
        # wait = WebDriverWait(chrome_driver,1)
        # try:
        #     wait.until(EC.visibility_of_element_located((By.XPATH,'aaaaaaaa')))
        # except Exception as e:
        #     print(str(e))
        # chrome_driver.maximize_window()                
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
        # flag_refresh = 0
        for config_ in configs:
            if 'remote' not in submit:
                if int(config_['Step']) < int(submit['Step']):
                    continue
            try:
                step_detect(chrome_driver,[config_])
                sleep(1)
            except:
                pass
            try:
                if config_['Action'] == 'Set_Refresh':
                    if flag_refresh == 0:
                        chrome_driver.refresh()
                        print('Chrome refreshing......')
                        flag_refresh = 1
                        break                        
                    else:
                        page_done.append(page['Page'])
                        continue
                flag_ready = wait_for_ready(chrome_driver)
                if flag_ready != 1:
                    print('Timeout ,"window.stop();"')
                    chrome_driver.execute_script("window.stop();")                    
                iframe_change(chrome_driver,config_['General']['iframe'])
                submit = selenium_funcs.get_action(chrome_driver,config_,submit)
                page_done.append(page['Page'])
                flag_refresh = 0
                sleep(2)
            except Exception as e:
                page_done.append(page['Page'])
                print(str(e))
                try:
                    submit['badstep'] = json.dumps(config_)
                    writelog(chrome_driver,submit)  
                except:
                    pass                
                return chrome_driver
        if flag_refresh == 1:
            print('flag_refresh = ',flag_refresh)
            continue
        else:
            page_done.append(page['Page'])
        '''
        check page flag status,if changed,continue
        '''
        if 'Success' in page['Status']:
            db.update_plan_status(2,submit['ID'])
            return chrome_driver
        if 'Fail' in page['Status']:
            db.update_plan_status(3,submit['ID'])
            return chrome_driver         
        flag_page_change = page_change(chrome_driver,page)
        if flag_page_change == 1:
            pass
        else:
            return chrome_driver
      
def takeStep(elem):
    return elem['Step']

def get_page_by_flag(Page_flags,chrome_driver):
    target_page = None
    for page in Page_flags:
        try:
            if page['Iframe'] != '':
                try:
                    print("page['Iframe']:",page['Iframe'])
                    iframe_change(chrome_driver,page['Iframe'])
                    # chrome_driver.switch_to_frame(page['Iframe'])
                except Exception as e:
                    print(str(e))
                    continue
            if page['Flag_xpath'] == '':
                if page['Flag_text'] in chrome_driver.page_source:
                    # chrome_driver.find_element_by_link_text(page['Flag_text'])
                    print('find target page:',page['Page'],'with text',page['Flag_text'])                                
                    target_page = page
                    break
                else:
                    sleep(1)
            else:
                if 'bbb===' in page['Flag_text']:
                    page['Flag_text'] = page['Flag_text'].split('bbb===')[1]  
                if '@@@@' in page['Flag_text']:
                    text_short = page['Flag_text'].split('@@@@')[0]
                    text_all = page['Flag_text'].split('@@@@')[1]
                else:
                    text_short = page['Flag_text']
                    text_all = page['Flag_text']
                # if text_short in chrome_driver.page_source:                
                element = chrome_driver.find_element_by_xpath(page['Flag_xpath'])
                print(page,'find xpath for:',element.get_attribute('innerText').lower())
                if element.get_attribute('innerText').lower() == text_all.lower():
                # if EC.text_to_be_present_in_element(element,text_all):
                    print('find target page:',page['Page'],'with xpath and text')
                    target_page = page
                    break
                else:
                    print("element text not equal to what's in db:")
                    print(element.get_attribute('innerText').lower())
                    print(text_all.lower())
                    #     chrome_driver.find_element_by_link_text(text_all)
                    #     print('find target page:',page['Page'],'with text')                
                    #     target_page = page
                    #     break  
                # else:
                #     sleep(1)             
        except Exception as e:
            print(str(e))
    return target_page

def wait_for_ready(chrome_driver):
    flag = 0
    for i in range(120):
        status = chrome_driver.execute_script("return document.readyState")
        if status != 'complete':
            print('document status:',status)
            sleep(1)
        else:
            flag = 1
            print('document status:',status)
            break    
    return flag

def page_detect(Page_flags,chrome_driver):
    page = None
    for i in range(5):
        flag = wait_for_ready(chrome_driver)
        if flag != 1:
            print('Timeout ,"window.stop();"')
            chrome_driver.execute_script("window.stop();")
        # page = get_page_by_flag(Page_flags,chrome_driver)
        # if page == None:
        #     print('Page Flag Not Found,',i+1)
        #     sleep(10)
        # else:
        #     print('Page Flag Found')            
        #     break
        # if 'Attackers might be trying to steal your information from' in chrome_driver.page_source:
        #     return None        
        status = chrome_driver.execute_script("return document.readyState")
        print('document status:',status)
        wrong_pages = ['Webpage not available','This page isn???t working','ERR_TIMED_OUT','ERR_CONNECTION_RESET']
        flag_wrong_page = 0
        if status == 'complete':
            # sleep(10)a
            for wrong_page in wrong_pages:
                if wrong_page in chrome_driver.page_source :
                    print('wrong_page:',wrong_page)
                    flag_wrong_page = 1
                    break
            if flag_wrong_page != 0:
                if i <= 2:
                    print('i <=2',i)
                    # if 'Attackers might be trying to steal your information from' in chrome_driver.page_source:
                    #     return None
                    #     chrome_driver.find_element_by_xpath('//*[@id="details-button"]').click()
                    #     sleep(2)
                    #     chrome_driver.find_element_by_xpath('//*[@id="proceed-link"]').click()
                    # else:
                    chrome_driver.refresh()
                    print('after refreshing page')
                    continue
                page = None
                break                          
            page = get_page_by_flag(Page_flags,chrome_driver)
            if page == None:
                print('Page Flag Not Found,',i+1)
            else:
                print('Page Flag Found')  
                return page          
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
    print('Detecting page if changed or changing....')
    flag = 0
    if page['Flag_xpath'] == '':
        if page['Flag_text'] not in chrome_driver.page_source:
            print('page changed')
            return 1
    try:
        element = chrome_driver.find_element_by_xpath(page['Flag_xpath'])
    except:
        print('page changed')        
        return 1
    for i in range(60): 
        if '@@@@' in page['Flag_text']:
            text_short = page['Flag_text'].split('@@@@')[0] 
            text_all = page['Flag_text'].split('@@@@')[1]             
        else:
            text_short = page['Flag_text'] 
            text_all = page['Flag_text']             
        if text_short not in chrome_driver.page_source:
            flag = 1
            print("page['Flag_text'] not in chrome_driver.page_source,page changed!!!!!!!!!!!")
            break            
        else:            
            # print(page,'find text:',element.text)
            # if element.is_displayed():
            # if element.text == text_all:
            #     print("%s still in chrome_driver.page_source,page not changed"%text_all)            
            #     sleep(2)
            # else:
            #     print("page['Flag_text'] not visibile in page,page changed!!!!!!!!!!!")                
            #     break
            try:
                if element.text == text:
                # if EC.text_to_be_present_in_element(element,text):
                    print("%s still in chrome_driver.page_source,page not changed"%text)            
                    sleep(2)
                else:
                    flag = 1
                    print("page['Flag_text'] not visibile in page,page changed!!!!!!!!!!!")                
                    break
            except Exception as e:
                flag = 1
                print("element not attached in page,page changed!!!!!!!!!!!")                
                break                
            # else:
            #     print("page['Flag_text'] not displayed in page,page changed!!!!!!!!!!!")                
            #     break


        # try:    
        #     chrome_driver.find_element_by_xpath(page['Flag_xpath'])   
        #     # print(element.text)
        # except:
        #     flag = 1
        #     break
        # if EC.text_to_be_present_in_element((By.XPATH,page['Flag_xpath']),page['Flag_text']):
        #     sleep(1)
        # else:
        #     flag = 1
        #     break
    if flag == 1:
        print('page changed')
        return 1
    else:
        print('timeout')
        return 0

def step_detect(chrome_driver,configs):
    # xpaths = []
    configs_detect = []
    for config in configs:
        if config['Action'] in ['Click','Select','Input','Slide','Set_Sleep']:
            if 'detect' not in config['General']:
                configs_detect.append(config)
            else:
                print("config['General']['detect']:",config['General']['detect'])
                if config['General']['detect'] == 'True':
                    configs_detect.append(config)
    # selenium_funcs.scroll_and_find_up(chrome_driver,xpaths[-1])
    for config in configs_detect:
        print('Detecting config:',config)
        iframe_change(chrome_driver,config['General']['iframe'])
        WebDriverWait(chrome_driver,50).until(EC.visibility_of_element_located((By.XPATH,config['General']['child_content'])))
        print('Step',config['Step'],' ready')

def iframe_change(chrome_driver,iframes):
    '''
    tag:-1   ----->>switch to default
    tag:2    ----->>switch to iframe 2
    ''       ----->>do nothing
    'iframe1,iframe2,iframe3'      ----->>switch to iframe3 from iframe2 from iframe1 from default
    '''


    if ':' in iframes:
        chrome_driver.switch_to.default_content()         
        num_iframe = int(iframes.split(':')[1])
        if num_iframe == -1:
            return
        else:
            iframe = chrome_driver.find_elements_by_tag_name('iframe')[num_iframe]
            chrome_driver.switch_to_frame(iframe)
            return
    if iframes == '':
        return
    else:
        iframes = iframes.split(',')
    chrome_driver.switch_to.default_content() 
    for iframe in iframes:
        if iframe != '':
            chrome_driver.switch_to_frame(iframe)

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
    # return_rand = random.randint(0,5)
    # if return_rand == 0:
    #     print('unique  random,return for Mission_Id:',Config)
    #     if Config['sleep_flag'] != 2:
    #         time_return = random.randint(0,600)
    #         # sleep(time_return)
    # else:
    time_cheat = random.randint(0,60)
    if Config['count']<5:
        sleep(Config['count']*5)
    else:
        sleep(Config['count']*30)
    # print(Config)
    if Config['Alliance'] != 'Test':
        if Config['Mission_Id'] != '20000':
            if Config['sleep_flag'] == 1:
                print('Sleep for random time:',time_cheat*60,'-------------')
                sleep(time_cheat*60)
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

