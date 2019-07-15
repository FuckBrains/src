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






def web_submit(submit):
    print(submit)
    # test
    # site = 'https://finaff.go2affise.com/click?pid=3464&offer_id=9436'
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
            chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Email_emu'])
        except:
            pass
        break
    try:
        chrome_driver.find_element_by_xpath('//*[@id="email_verification"]').send_keys(submit['Email_emu'])
    except:
        pass

    chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(submit['Email_emu_pwd'])

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
        site = email_confirm(submit)  
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
            # print(site)
            site = str(base64.b64decode(site))   
            site_a = site.find('http://email.starstable.com/wf/click?upn=')         
            site_b = site.find('"',site_a)
            site = site[site_a:site_b]
            print(site)
            return site            
    return site






if __name__=='__main__':
    submit={}
    submit['Ua'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    submit['Firstname'] = 'KIRSTEN'
    submit['Lastname'] = 'WOLD'
    submit['City'] = 'SPOKANE'
    submit['State'] = 'WA'
    submit['Homephone'] = '5093270780'
    submit['Email'] = 'kdwold@live.com'
    submit['Address'] = '2509 W. SHARP AVE.'   
    submit['zipcode'] = '79108'
    submit['month'] = '4'
    submit['day'] = '12'
    submit['year'] = '1964'
    submit['Height_FT'] = '5'
    submit['Height_Inch'] = '11'
    submit['Weight'] = '175'
    submit['Email_emu'] = 'IsidoreChadbUuCg@yahoo.com'
    submit['Email_emu_pwd'] = 'pmV7T6oMy'
    # test_num()
    # web_Submit(submit)
    site=email_confirm(submit)
    print(site)
