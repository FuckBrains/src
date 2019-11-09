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
import selenium_funcs
import Submit_handle
import random


def web_submit(submit,chrome_driver,debug=0):
    # test
    if debug == 1:
        site = 'https://adpgtrack.com/click/5cf8d637a0359455055330d6/156986/199595/subaccount'
        submit['Site'] = site
    # js = 'window.location.href="%s"'(submit['Site'])
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    chrome_driver.find_element_by_xpath('//*[@id="trigger-overlay"]').click()
    sleep(3)
    num_ = random.randint(0,100000)
    num_1 = random.randint(0,1)
    if num_1 == 0:
        name = submit['DECJ']['lastname']+str(num_)        
    else:
        name = submit['DECJ']['lastname']+str(num_)+submit['DECJ']['firstname']
    chrome_driver.find_element_by_xpath('//*[@id="usernameInput1"]').send_keys(name)
    sleep(2)
    email = submit['DECJ']['emailaddress']    
    chrome_driver.find_element_by_xpath('//*[@id="regForm1"]/div[2]/input').send_keys(email)
    sleep(2)
    pwd = Submit_handle.password_get()
    chrome_driver.find_element_by_xpath('//*[@id="regForm1"]/div[3]/input').send_keys(pwd)
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="regForm1"]/div[4]/div/button').click()
    sleep(30)
    chrome_driver.close()
    chrome_driver.quit()
    return 1






def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10056']
    excel = 'DECJ'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    # submit = {}
    submit['Country'] = 'DE'
    submit['Mission_Id'] = '10056'
    # phone = submit[excel]['homephone']
    # phone = Submit_handle.get_uk_phone1(phone)
    # print(phone)
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)



if __name__=='__main__':
    test()
