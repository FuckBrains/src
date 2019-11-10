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
        site = 'https://track.amcmpn.com/click?pid=665&offer_id=23095'
        submit['Site'] = site
    # js = 'window.location.href="%s"'(submit['Site'])
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    num_ = random.randint(0,100000)
    num_1 = random.randint(0,1)
    if num_1 == 0:
        name = submit['DECJ']['lastname']+str(num_)        
    else:
        name = submit['DECJ']['lastname']+str(num_)+submit['DECJ']['firstname']
    chrome_driver.find_element_by_xpath('//*[@id="user_add_form"]/div/div/div[2]/input').send_keys(name)
    sleep(1)
    email = submit['DECJ']['emailaddress']
    chrome_driver.find_element_by_xpath('//*[@id="inputEmail"]').send_keys(email)
    sleep(1)
    phone = submit['DECJ']['phone'].split('.')[0]
    for key in int(phone):
        chrome_driver.find_element_by_xpath('//*[@id="phone"]').send_keys(key)
    sleep(1)
    chrome_driver.find_element_by_css_selector('#user_add_form > div > div > div:nth-child(41) > div > label > p').click()
    sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="user_add_form"]/div/div/div[15]/div/label/p').click()
    sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="user_add_form"]/div/div/button').click()
    sleep(60)
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
