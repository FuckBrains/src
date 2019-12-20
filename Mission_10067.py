from selenium import webdriver
from selenium.webdriver import ActionChains
import json
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
import selenium_funcs
import Submit_handle


'''
GETAROUND
Auto
'''



def web_submit(submit,chrome_driver,debug=0):
    # test
    # https://www.cam4.com/
    chrome_driver.get('https://www.google.com')
    sleep(1)
    print('stop')
    # while True:
    #     url = chrome_driver.current_url 
    #     print(url)
    #     if 'account.blizzard.com' in url :
    #         chrome_driver.execute_script("window.stop();") 
    #         print('stop')
    #         break
    #     else:
    #         sleep(0.5)
    chrome_driver.delete_all_cookies()
    with open('1.txt','r') as f:
        cookie_str = f.readlines()

    cookies = json.loads(cookie_str[0])
    # cookies = json.loads(submit['Cookie'])
    for cookie in cookies:
        # if 'expiry' in cookie:
        #     cookie['expiry'] = int(cookie['expiry']) 
        chrome_driver.add_cookie(cookie)  
    print('After add cookie') 
    cookies = chrome_driver.get_cookies()    
    print('cookies',cookies)    
    chrome_driver.get('https://account.blizzard.com/')     
    # chrome_driver.refresh()
    sleep(3000)


def test1():
    with open('1.txt','r') as f:
        cookie_str = f.readlines() 
    print(cookie_str[0])
    return cookie_str[0]    

# {"scroll": "False", "try": "False", "xpath": "//*[@id=\"signup\"]", "hidden_xpath": "", "tagname": "", "iframe": ""}

def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    # Mission_list = ['10049']
    # excel = 'health'    
    # Excel_name = [excel,'']
    # Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    # submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit = {}
    submit['Country'] = 'US'
    submit['Mission_Id'] = '10067'
    # phone = submit[excel]['homephone']
    # phone = Submit_handle.get_uk_phone1(phone)
    # print(phone)
    account = db.get_cehuoaccount(submit)
    print(account)
    submit['Cookie'] = account['cookie']
    submit['ua'] = account['ua']
    print(submit['Cookie'])
    cookie_str = test1()
    print(cookie_str)
    cookies = json.loads(submit['Cookie'])
    # for cookie in cookies:
    #     for key in cookie:
    #         print(key,cookie[key])
    #         print(type(key),type(cookie[key])) 
    # submit['Record'] = 1

    # chrome_driver = Chrome_driver.get_chrome(submit)
    # web_submit(submit,chrome_driver)




if __name__=='__main__':
    test()