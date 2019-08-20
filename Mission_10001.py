import base64
from selenium import webdriver
from time import sleep
# import xlrd
import random
import os
import time
import sys
sys.path.append("..")
# import email_imap as imap
# import json
import re
# from urllib import request, parse
from selenium.webdriver.support.ui import Select
# import base64
import Chrome_driver
import email_imap as imap
import name_get
import db


'''
STAR_STABLE
GB
Email
'''



def web_submit(submit):
    print(submit)
    # # test
    # site = 'http://im.datingwithlili.com/im/click.php?c=19&key=9ujpwgfe3d8bkaai63ncck9u'
    # submit['Site'] = site
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])   
    name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    # sleep(10000)
    sleep(10)
    # num = random.randint(0,30)
    # s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="first_name"]'))
    # s1.select_by_index(str(num))   
    # num = random.randint(0,30) 
    # s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="surname1"]'))
    # s1.select_by_index(str(num))     
    # num = random.randint(0,30) 
    # s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="surname2"]'))
    # s1.select_by_index(str(num))  
       
    # num = random.randint(0,30) 
    # s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="horse1"]'))
    # s1.select_by_index(str(num))     

    # num = random.randint(0,30) 
    # s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="horse2"]'))
    # s1.select_by_index(str(num))     
    while True:
        try:
            chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Email']['Email_emu'])
        except:
            pass
        break
    try:
        chrome_driver.find_element_by_xpath('//*[@id="email_verification"]').send_keys(submit['Email']['Email_emu'])
    except:
        pass
    chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(submit['Email']['Email_emu_pwd'])
    num = random.randint(1980,2004) 
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="year"]'))
    s1.select_by_value(str(num)) 

    num = random.randint(1,12) 
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="month"]'))
    s1.select_by_value(str(num)) 


    num = random.randint(1,12) 
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="day"]'))
    s1.select_by_value(str(num))

    chrome_driver.find_element_by_xpath('//*[@id="terms"]').click()
    chrome_driver.find_element_by_xpath('//*[@id="email_promotion"]').click()
    chrome_driver.find_element_by_xpath('//*[@id="email_newsletter"]').click()

    chrome_driver.find_element_by_xpath('//*[@id="btn_submit"]').click()
    site = ''
    handle = chrome_driver.current_window_handle
    flag = 0
    try:            
        site = email_confirm(submit['Email'])  
        print(site)      
    except Exception as e:
        print(str(e))
    if site != '':
        newwindow='window.open("' + site + '");'
        chrome_driver.execute_script(newwindow)
    else:
        flag = 1
        chrome_driver.close()
        chrome_driver.quit()
        return flag        
    handles=chrome_driver.window_handles   
    sleep(2000)
    for i in handles:
        if i != handle:
            chrome_driver.switch_to.window(i)
            chrome_driver.refresh() 
            sleep(30)     
            chrome_driver.close()
            chrome_driver.quit()
            return flag             




 

def email_confirm(submit):
    site = ''
    for i in range(4):
        msg_content = imap.email_getlink(submit,'starstable')
        # print(len(msg_content))
        if 'starstable' not in msg_content :
            print('Target Email Not Found !')
            sleep(15)
        else:
            # print(msg_content)
            c = msg_content.find('Content-Transfer-Encoding: base64')
            a = msg_content.find('Content-Transfer-Encoding: base64',c+10)
            b = msg_content.find('--====',a)
            site = msg_content[a+35:b-50].replace('\r','').replace('\n','')
            # print(len(site))
            site += "=" * ((4 - len(site) % 4) % 4)
            for i in range(4):
                # print(site)
                try:
                    site = str(base64.b64decode(site[:-1-i]))   
                    break
                except:
                    pass
            site_a = site.find('http://email.starstable.com/wf/click?upn=')         
            site_b = site.find('"',site_a)
            site = site[site_a:site_b]
            print(site)
            return site            
    return site






if __name__=='__main__':
    submit = db.get_one_info()
    web_submit(submit)
