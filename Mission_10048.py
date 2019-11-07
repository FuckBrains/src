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
        site = 'http://flusnlb.com/TUGV'
        submit['Site'] = site
    # js = 'window.location.href="%s"'(submit['Site'])
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()    
    sleep(3)
    elements = ['//*[@id="pp_img_0"]','//*[@id="pp_img_1"]','//*[@id="pp_img_2"]','//*[@id="pp_img_3"]','//*[@id="pp_img_4"]','//*[@id="pp_img_5"]']
    num = random.randint(0,5)
    chrome_driver.find_element_by_xpath(elements[num]).click()
    sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="prepage_box"]/p[2]/button').click()
    sleep(1)
    gender = ['//*[@id="mfw_fieldset_inputData"]/p[5]/div[1]','//*[@id="mfw_fieldset_inputData"]/p[5]/div[2]']
    num = random.randint(0,1)
    chrome_driver.find_element_by_xpath(gender[num]).click()
    sleep(1)
    firstname = submit['DECJ']['firstname']
    chrome_driver.find_element_by_xpath('//*[@id="mfw_fieldset_inputData"]/p[6]/input').send_keys(firstname)
    sleep(1)
    lastname = submit['DECJ']['lastname']
    chrome_driver.find_element_by_xpath('//*[@id="mfw_fieldset_inputData"]/p[7]/input').send_keys(lastname)
    sleep(1)
    email = submit['DECJ']['emailaddress']
    chrome_driver.find_element_by_xpath('//*[@id="mfw_fieldset_inputData"]/p[8]/span/input').send_keys(email)
    sleep(1)    
    chrome_driver.find_element_by_xpath('//*[@id="mfw_fieldset_agbs"]/p/div/label').click()
    sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="btn_middle"]').click()
    sleep_rand = random.randint(60,180)
    sleep(sleep_rand)
    return 1

def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10048']
    excel = 'DECJ'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    # submit = {}
    submit['Country'] = 'DE'
    submit['Mission_Id'] = '10048'
    # phone = submit[excel]['homephone']
    # phone = Submit_handle.get_uk_phone1(phone)
    # print(phone)
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)

if __name__=='__main__':
    test()
