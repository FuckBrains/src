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
    chrome_driver.get('http://da.off3riz.com/aff_c?offer_id=19&aff_id=1564')
    father_elem = chrome_driver.find_element_by_class_name('step1')
    elem = father_elem.find_element_by_xpath('//*[@id="step"]/div/button')
    # {"scroll": "False", "try": "False", "father_type": "Class", "father_content": "step1", "child_type": "Xpath", "child_content": "//*[@id=\"step\"]/div/button[1]", "iframe": "", "detect": "False"}
    elem.click()
    sleep(3)
    father_elem = chrome_driver.find_element_by_class_name('step2')
    elem = father_elem.find_element_by_class_name('yes')
    elem.click()
    sleep(3)
    father_elem = chrome_driver.find_element_by_class_name('step3')
    elem = father_elem.find_element_by_class_name('yes')
    elem.click()
    sleep(3)
    father_elem = chrome_driver.find_element_by_class_name('step4')
    elem = father_elem.find_element_by_class_name('yes')
    elem.click()
    sleep(3)

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
    Mission_list = ['10049']
    excel = 'health'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    submit['Mission_Id'] = 10049
    submit['Country'] = 'FR'
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    # submit = {}
    # submit['Country'] = 'FR'
    # submit['Mission_Id'] = '10077'
    # phone = submit[excel]['homephone']
    # phone = Submit_handle.get_uk_phone1(phone)
    # print(phone)
    # account = db.get_cehuoaccount(submit)
    # print(account)
    # submit['Cookie'] = account['cookie']
    # submit['ua'] = account['ua']
    # print(submit['Cookie'])
    # cookie_str = test1()
    # print(cookie_str)
    # cookies = json.loads(submit['Cookie'])
    # for cookie in cookies:
    #     for key in cookie:
    #         print(key,cookie[key])
    #         print(type(key),type(cookie[key])) 
    # submit['Record'] = 1

    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver)




if __name__=='__main__':
    test()