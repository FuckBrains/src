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
        site = 'https://go.byoffers.net/click?pid=170&offer_id=1268'
        submit['Site'] = site
    # js = 'window.location.href="%s"'(submit['Site'])
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    chrome_driver.switch_to_frame('rsIframe')
    chrome_driver.find_element_by_xpath('//*[@id="page1"]/button[3]').click()
    sleep(5000)


def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10002']
    excel = 'health'  
    # excel = 'Uspd'  
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    print(submit)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel]]  
    submit['Mission_Id'] = '10002'
    # phone = submit[excel]['homephone']
    # phone = Submit_handle.get_uk_phone1(phone)
    # print(phone)
    # chrome_driver = Chrome_driver.get_chrome(submit)
    # web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
