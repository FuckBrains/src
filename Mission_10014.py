from time import sleep
import random
import os
import time
import sys
import json
import re
from urllib import request, parse
import name_get
import Chrome_driver
import email_imap as imap
import db
import selenium_funcs
import emaillink



'''
DesperateBBWs(Done)
'''




def detect_email():
    url = r'https://www.cam4.com/signup/email?pageLocale=en'
    url2 = r'https://www.cam4.com/signup/username?pageLocale=en'


def check_email(submit):
    print(submit['Email_emu'])
    data = {'email': submit['Email_emu']}
    data = parse.urlencode(data).encode('gbk')
    req = request.Request(url, data=data)
    page = ''
    for i in range(5):
        try:
            page = request.urlopen(req,timeout=10.0).read()
        except:
            continue
        if str(page) != '':
            break
    print(page)
    if 'GOOD_EMAIL' not in str(page):
        if page == '':
            return -1 #netwrong
        else:
            return 1 #fail
    else:
        print(submit['Email_emu'],'is GOOD_EMAIL')
        return 0 #success




def web_submit(submit,debug=0):
    if debug == 1:
        site = 'http://gbb.maxcodema.xyz/c/11286/1?'
        submit['Site'] = site        
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    # name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    # chrome_driver.refresh()
    if 'desperatebbws.com/landing?' not in chrome_driver.current_url:
        chrome_driver.close()
        chrome_driver.quit()
        return
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Email']['Email_emu'])
    chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(submit['Email']['Email_emu_pwd'])
    sleep(2)
    # chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[3]/div/div').click()
    chrome_driver.find_element_by_class_name('btn-secondary').click()
    # chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[3]/div/div/a').click()
    sleep(10)
    # sleep(5000)
    if 'registered' not in chrome_driver.current_url:
        chrome_driver.close()
        chrome_driver.quit()
        return
    site = ''
    handle = chrome_driver.current_window_handle
    try:            
        site = email_confirm(submit)  
        print(site)      
    except Exception as e:
        print('email check failed',str(e))
    if site != '':
        newwindow='window.open("' + site + '");'
        chrome_driver.execute_script(newwindow)
        sleep(20)        
    else:
        flag = 1
        chrome_driver.close()
        chrome_driver.quit()
        return flag        
    handles=chrome_driver.window_handles   
    try:
        for i in handles:
            if i != handle:
                chrome_driver.switch_to.window(i)
                chrome_driver.refresh()                  
    except Exception as e:
        chrome_driver.close()
        chrome_driver.quit()    
        return flag    
    chrome_driver.close()
    chrome_driver.quit()
    return flag
        # submit['name'] = ng.gen_one_word_digit(lowercase=False)
        # status,submit['name'] = web_Submit(submit)


def email_confirm(submit):
    print('----------')
    for i in range(5):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']
            title = 'Please verify your e-mail address'
            pattern = r'.*?(https://desperatebbws.com/accounts/verify/email/e[\w]{1,100})'
            # pattern = r'.*?(https://opinionoutpost.com/Membership/Intake\?signuptoken=.*?\&resp=([0-9]{5,15}))'
            url_link = emaillink.get_email(name,pwd,title,pattern)
            if 'Bad' in url_link:
                print('Get duplicated email')
                url_link = emaillink.get_email(name,pwd,title,pattern,True)
            if 'http' in url_link :
                break
        except Exception as e:
            print(str(e))
            print('===')
            sleep(15)
            pass
    return url_link



if __name__=='__main__':
    submit = db.get_one_info()
    print(submit)
    web_submit(submit,1)
    # submit = {'Email': {'Email_Id': '70099ee9-aa34-11e9-964c-0003b7e49bfc', 'Email_emu': 'RitchieShieldsrf@aol.com', 'Email_emu_pwd': 'ITgUVB3F', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}
    # email_confirm(submit)
