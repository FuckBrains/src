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
        site = 'http://da.off3riz.com/aff_c?offer_id=666&aff_id=1230'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    print('Loading finished')
    sleep(3)
    # 18
    buttons = chrome_driver.find_elements_by_id('buttons')
    for button in buttons:
        button_yes = button.find_elements_by_tag_name('a')[0]
        print(button_yes.get_attribute('innerHTML'))
        try:
            button_yes.click()
            sleep(2)
        except Exception as e:
            print(e)
    # name
    sleep(3)
    name = name_get.gen_one_word_digit(lowercase=False,digitmax=100000)
    chrome_driver.find_element_by_xpath('//*[@id="registration"]/div[2]/input[1]').send_keys(name)
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="emailPG"]').send_keys(submit['fr_soi']['email'])
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="pg_submit"]').click()
    sleep_rand = random.randint(60,180)
    sleep(sleep_rand)
    return 1



def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    # Mission_list = ['10044']
    # excel = 'fr_soi'    
    # Excel_name = [excel,'']
    # Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    # submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit = {}
    submit['Mission_Id'] = '10047'
    submit['Country'] = 'FR'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)

def test1():
    num = random.randint(0,1)
    print(num)

if __name__=='__main__':
    test()
