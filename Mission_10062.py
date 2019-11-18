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
        site = 'http://zh.moneymethods.net/click.php?c=26&key=ga25g4e1rzhn442dwbuze685'
        submit['Site'] = site
    # js = 'window.location.href="%s"'(submit['Site'])
    chrome_driver.get(submit['Site'])
    sleep(3)

    # gender
    chrome_driver.find_element_by_xpath('//*[@id="form"]/div[1]/label[1]/span').click()
    sleep(2)

    # age
    element = '//*[@id="age"]'
    age = random.randint(25,50)
    s1 = Select(chrome_driver.find_element_by_xpath(element))
    s1.select_by_value(str(age))    
    sleep(2)

    # email
    try:
        email = submit['pl_soi']['email']
        chrome_driver.find_element_by_xpath('//*[@id="form"]/div[3]/div/div/input').send_keys(email)    
    except:
        return 1
    # confirm
    chrome_driver.find_element_by_xpath('//*[@id="form"]/div[3]/div/button[2]/span').click()
    sleep(2)    

    # pwd
    pwd = Submit_handle.get_pwd_real()
    chrome_driver.find_element_by_xpath('//*[@id="form"]/div[4]/div/div[1]/input').send_keys(pwd)
    # button
    chrome_driver.find_element_by_xpath('//*[@id="form"]/div[4]/div/button[2]').click()
    num = random.randint(60,180)
    sleep(num)
    return 1

def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10062']
    excel = 'pl_soi'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Mission_Id'] = '10062'
    submit['Country'] = 'PL'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
