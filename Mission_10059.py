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
    chrome_driver.close()
    chrome_driver.quit()
    chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
    if debug == 1:
        site = 'http://flusnlb.com/O20V'
        submit['Site'] = site
    # js = 'window.location.href="%s"'(submit['Site'])
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    chrome_driver.find_element_by_xpath('//*[@id="reg-form"]/div[1]/div[2]/div[2]/span').click()
    sleep(1)
    # choose age
    age = random.randint(19,50)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="age-field"]'))
    s1.select_by_value(str(age))
    sleep(1)
    # next
    chrome_driver.find_element_by_xpath('//*[@id="reg-form"]/div[1]/div[2]/div[2]/span').click()
    # next
    chrome_driver.find_element_by_xpath('//*[@id="reg-form"]/div[1]/div[2]/div[2]').click()
    # Email
    sleep(2)
    email = submit['it_soi']['email']
    element = chrome_driver.find_element_by_xpath('//*[@id="email-field"]')
    element.click()
    element.send_keys(email)
    # next
    chrome_driver.find_element_by_xpath('//*[@id="reg-form"]/div[1]/div[2]/div[2]').click()
    sleep(1)
    element = chrome_driver.find_element_by_xpath('//*[@id="password-field"]')
    element.click()
    pwd = Submit_handle.password_get_Nostale()
    element.send_keys(pwd)
    sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="submit-btn"]').click()
    sleep(180)
    chrome_driver.close()
    chrome_driver.quit()
    return 1



def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10059']
    excel = 'it_soi'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Mission_Id'] = '10059'
    submit['Country'] = 'IT'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
