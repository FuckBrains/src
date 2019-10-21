
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
CindyMatches (Done)
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




def web_submit(submit,chrome_driver,debug=0):
    if debug == 1:
        site = 'https://tracking.plscmp.com/click?pid=1123&offer_id=23587'
        submit['Site'] = site        
    chrome_driver.get(submit['Site'])
    name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    # sleep(2000)
    # if 'cindyrnatches.com/landing?' not in chrome_driver.current_url:
    #     print('url wrong:',chrome_driver.current_url)
    #     chrome_driver.close()
    #     chrome_driver.quit()
    #     return
    sleep(5)
    chrome_driver.find_element_by_id('email').send_keys(submit['Email']['Email_emu'])
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div/div[3]/div[1]/button').click()
    # chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(submit['Email']['Email_emu_pwd'])
    sleep(2)
    # ok
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[1]/div[2]/div/div/a').click()
    # next
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[2]/div[2]/div/a').click()
    # chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[3]/div/div').click()
    chrome_driver.find_element_by_class_name('form-submit').click()
    # chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[3]/div/div/a').click()
    sleep(10)
    # sleep(5000)
    if 'registered' not in chrome_driver.current_url:
        chrome_driver.close()
        chrome_driver.quit()
        return 0
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
    for i in range(10):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']
            title = 'Please verify your e-mail address'
            pattern = r'.*?(https://cindyrnatches.com/accounts/verify/email/[\w]{1,100})'
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

def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_Id = '10012'
    Mission_list = [Mission_Id]
    excel = 'Email'    
    Excel_name = ['',excel]
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # submit['Mission_Id'] = Mission_Id
    print(submit)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    # submit['Country'] = 'FR'
    submit['Alliance'] = 'offeriz'
    submit['Account'] = 1
    submit['Mission_Id'] = Mission_Id
    submit['ua']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)
    # submit['Email']['Email_emu'] = 'ThynnFoordbP@yahoo.com'
    # submit['Email']['Email_emu_pwd'] = 'tb3yy7c1k'
    # email_confirm(submit,debug=1)

if __name__=='__main__':
    test()
