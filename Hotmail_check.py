import sys
sys.path.append("../..")

from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from datetime import date,datetime
import xlrd
from xlutils.copy import copy
from selenium import webdriver

import textcode as TC
# from xlutils.copy import copy
from time import sleep
# from name_get import name_get as ng
import re
import os
import random
# from modules_add.Cam4 import Cam4_reg as web_reg
import json
import time
import threadpool

pool = threadpool.ThreadPool(3)

def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()

def Hotmail_Check(submit,str_1,str_2):
    writelog(submit['email']+'login start:')
    # path='../driver'
    # executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument("--disable-infobars")
    # options.add_argument("--single-process")
    ua = submit['ua']
    options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒
    chrome_driver.get("https://outlook.live.com/owa/")
    i = 0
    while i <=3:
        try:
            chrome_driver.find_element_by_css_selector('body > section > div > div > div.landing-section.headerHero > a:nth-child(4)').click()
            writelog('Accessing hotmail singin page success')
            break
        except Exception as e:
            writelog('Accessing hotmail singin page failed for'+str(i)+'time',str(e))
            chrome_driver.get("https://outlook.live.com/owa/")
            sleep(5)
            i = i + 1  
    # print(chrome_driver.title)
    title = 'Sign in to your Microsoft account'
    i = 0
    while chrome_driver.title != title:
        chrome_driver.refresh()
        i += 1
        if i == 3:
            break
    if chrome_driver.title == "Sign in to your Microsoft account" :
        writelog('Get to hotmail singin page success')
    else:
        if chrome_driver.title == 'Outlook.com - Microsoft free personal email':
            try:
                chrome_driver.find_element_by_css_selector('body > section > div > div > div > div:nth-child(4) > a').click()
            except Exception as e:
                writelog('Network wrong,hotmail signin page  failed to get')
                chrome_driver.close()
                chrome_driver.quit()
                return 0  
        else:
            writelog('Network wrong,hotmail signin page  failed to get')
            chrome_driver.close()
            chrome_driver.quit()
            return 0  
    try:
        chrome_driver.find_element_by_name('loginfmt').send_keys(submit['email'])
        sleep(3)
        chrome_driver.find_element_by_id('idSIButton9').click()
    except Exception as e:
        # sleep(1000)
        num = random.randint(11111,99999)
        chrome_driver.save_screenshot(submit['email']+str(num)+'.png')        
        writelog('Network wrong,hotmail signin page  failed to get',str(e))
        chrome_driver.close()
        chrome_driver.quit() 
        return 0       
    # sleep(1000)

    i = 0
    while chrome_driver.title != title:
        chrome_driver.refresh()
        i += 1
        if i == 3:
            break
    if chrome_driver.title == "Sign in to your Microsoft account":
        writelog('Get to hotmail enter passwd page success')
    else:
        writelog('Network wrong,hotmail enter passwd page  failed to get')
        chrome_driver.close()
        chrome_driver.quit()
        return 0  

    try:
        chrome_driver.find_element_by_name('passwd').send_keys(submit['email_pwd'])
        sleep(3)
        chrome_driver.find_element_by_id('idSIButton9').click()
    except Exception as e:
        writelog('Network wrong,hotmail signin page  failed to get')
        chrome_driver.close()
        chrome_driver.quit()
        return 0 
    if 'Your account has been temporarily suspended' in chrome_driver.page_source:
        writelog('Account wrong,need phone code')
        chrome_driver.close()
        chrome_driver.quit()
        return -1         

    i = 0
    while submit['email'] not in chrome_driver.title:
        chrome_driver.refresh()
        i += 1
        if i == 3:
            break
    if 'https://outlook.live.com/mail/inbox' in chrome_driver.current_url:
        writelog(submit['email']+' login success')
    else:
        writelog('Network wrong,'+submit['email']+'login failed after entering email passwd')
        chrome_driver.close()
        chrome_driver.quit()
        return 0  

    cookies = chrome_driver.get_cookies()
    try:
        with open('cookies\cookies_email\\hotmail\\'+submit['email']+".txt",'w') as fp:
            json.dump(cookies, fp) 
    except Exception as e:
        writelog('Get cookies failed after login successed with error:',str(e))
    try:
        flag = web_reg.web_Submit(submit)
        if flag == 0:
            writelog('register failed')
            chrome_driver.close()
            chrome_driver.quit()
            return 1
        else:
            writelog('Register success with cam4')
    except Exception as e:
        writelog('Register failed with error:',str(e))
        chrome_driver.close()
        chrome_driver.quit()
        return 1
    try:
        # //*[@id="searchBoxId"]/div[2]/div/input
        chrome_driver.find_element_by_xpath('//*[@id="searchBoxId"]/div[2]/div/input').click()
        sleep(2)
        # //*[@id="searchBoxId"]/div[1]/div/input
        chrome_driver.find_element_by_xpath('//*[@id="searchBoxId"]/div[1]/div/input').send_keys('Cam4')
        sleep(3)
        chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/button/div').click()
        sleep(3)
    except Exception as e:
        writelog('Can not find searchBox',str(e))
    # sleep(1000)
    try:
        list1 = chrome_driver.find_elements_by_tag_name("mark")
        [a.click() for a in list1 if str_1 in str(a.get_attribute('innerHTML'))]
        chrome_driver.maximize_window()
        if chrome_driver.find_element_by_link_text(str_2):
            writelog('Yes we find Cam4 and we are clicking verify')
            chrome_driver.find_element_by_link_text(str_2).click()
            rantime = random.randint(3,5)
            sleep(rantime*60)
            #add logic,save cookies to floder cookies
            chrome_driver.get("http://www.cam4.com/female")
            sleep(10)
            j = 0
            while chrome_driver.page_source.find('This site can’t be reached')!=-1:
                chrome_driver.refresh()
                j += 1
                if j > 3:
                    break
            if chrome_driver.page_source.find('This site can’t be reached')==-1:                
                cookies = chrome_driver.get_cookies()
                print(cookies)
                with open('cookies\cookies_cam4\\'+submit['email']+".txt",'w') as fp:
                    json.dump(cookies, fp)                     
            chrome_driver.close()
            chrome_driver.quit()
            return 3        
    except Exception as e:
        writelog('Cam4 email not find',str(e))


def Hotmail_Recover(submit):
    # writelog(submit['email']+'login start:')
    # path='../driver'
    # executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument("--disable-infobars")
    # options.add_argument("--single-process")
    # ua = submit['ua']
    # options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒
    chrome_driver.get("https://outlook.live.com/owa/")
    i = 0
    while i <=3:
        try:
            chrome_driver.find_element_by_css_selector('body > section > div > div > div.landing-section.headerHero > a:nth-child(4)').click()
            writelog('Accessing hotmail singin page success')
            break
        except Exception as e:
            writelog('Accessing hotmail singin page failed for'+str(i)+'time',str(e))
            chrome_driver.get("https://outlook.live.com/owa/")
            sleep(5)
            i = i + 1  
    # print(chrome_driver.title)
    title = 'Sign in to your Microsoft account'
    i = 0
    while chrome_driver.title != title:
        chrome_driver.refresh()
        i += 1
        if i == 3:
            break
    chrome_driver.find_element_by_name('loginfmt').send_keys(submit['email'])
    chrome_driver.find_element_by_id('idSIButton9').click()
    sleep(2)
    chrome_driver.find_element_by_name('passwd').send_keys(submit['email_pwd'])
    sleep(3)
    chrome_driver.find_element_by_id('idSIButton9').click()
    if 'Your account has been locked' not in chrome_driver.page_source:
        return 1
    chrome_driver.find_element_by_id('StartAction').click()
    while True:
        try:
            s1 = Select(chrome_driver.find_elements_by_class_name('form-control')[0])  # 实例化Select  
            break
        except:
            sleep(1)
            pass
    try:
        s1.select_by_value('CN')  # 选择value="o2"的项  
    except:
        chrome_driver.close()
        chrome_driver.quit()
    while True:
        sleep(3)        
        phone,time_stand = TC.get_phone_single()
        chrome_driver.find_elements_by_class_name('form-control')[1].clear()
        chrome_driver.find_elements_by_class_name('form-control')[1].send_keys(phone)
        sleep(3) 
        chrome_driver.find_element_by_link_text('Send code').click()
        sleep(3)
        try:
            chrome_driver.find_elements_by_class_name('form-control')[2].send_keys('123')
        except:
            print(phone)
            TC.free_phone(phone)
            print('=====')
            continue
        while True:
            text = TC.get_text(phone,time_stand)
            if str(text) != '3001':
                chrome_driver.find_elements_by_class_name('form-control')[2].clear()
                chrome_driver.find_elements_by_class_name('form-control')[2].send_keys(text)
                TC.free_phone(phone)
                break 
            else:
                sleep(5) 
        break          
    chrome_driver.find_element_by_xpath('//*[@id="ProofAction"]').click()
    sleep(10)
    chrome_driver.close()
    chrome_driver.quit()
    return 1
    

def Hotmail_login(submit):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument("--disable-infobars")
    # options.add_argument("--single-process")
    # ua = submit['ua']
    # options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒
    chrome_driver.get("https://outlook.live.com/owa/")
    i = 0
    while i <=3:
        try:
            chrome_driver.find_element_by_css_selector('body > section > div > div > div.landing-section.headerHero > a:nth-child(4)').click()
            writelog('Accessing hotmail singin page success')
            break
        except Exception as e:
            writelog('Accessing hotmail singin page failed for'+str(i)+'time',str(e))
            chrome_driver.get("https://outlook.live.com/owa/")
            sleep(5)
            i = i + 1  
    # print(chrome_driver.title)
    title = 'Sign in to your Microsoft account'
    i = 0
    while chrome_driver.title != title:
        chrome_driver.refresh()
        i += 1
        if i == 3:
            break
    chrome_driver.find_element_by_name('loginfmt').send_keys(submit['email'])
    chrome_driver.find_element_by_id('idSIButton9').click()
    sleep(2)
    chrome_driver.find_element_by_name('passwd').send_keys(submit['email_pwd'])
    sleep(3)
    chrome_driver.find_element_by_id('idSIButton9').click()
    return chrome_driver


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




def multi_recover(submit):
    flag = 0
    try:
        flag=Hotmail_Recover(submit)
        prit()
    except Exception as e:
        writelog(str(e))






def multi_login(submit):
    flag = 0
    try:
        chromedriver=Hotmail_login(submit)
        prit()
    except Exception as e:
        writelog(str(e))
    a = input()
    chromedriver.close()
    chromedriver.quit()


def read_excel(path_excel):
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    rows = sheet.nrows 
    keys = sheet.row_values(0)    
    submits = []
    for i in range(rows):
        if  i == 0:
            pass
        if sheet.cell(i,0).value == '':
            values = sheet.row_values(i)
            submit = dict(zip(keys,values))
            submit['index'] = i
            submits.append(submit)
    return submits   


def recover(path_excel):
    # path_excel = 'Hotmail_recover.xlsx'    
    submits = read_excel(path_excel)
    # print(submits)
    print(len(submits))
    # return
    requests = threadpool.makeRequests(multi_recover, submits)
    [pool.putRequest(req) for req in requests]
    pool.wait() 


def Login(path_excel):
    # path_excel = 'Hotmail_recover.xlsx'    
    submits = read_excel(path_excel)
    # print(submits)
    print(len(submits))
    # return
    requests = threadpool.makeRequests(multi_login, submits)
    [pool.putRequest(req) for req in requests]
    pool.wait() 
    killpid()



if __name__=='__main__':
    path_excel = 'Hotmail_recover.xlsx'    
    Login(path_excel)
