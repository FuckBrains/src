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
        site = 'http://flusnlb.com/GSvV?sub1=sub1&sub2=sub2&sub3=sub3&sub4=sub4&sub5=sub5'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(5000)
    # page1
    chrome_driver.find_element_by_xpath('//*[@id="header_login"]/a[2]').click()
    sleep(10)
    chrome_driver.find_element_by_xpath('//*[@id="user_member_username"]').send_keys()
    sleep(3)
    chrome_driver.find_element_by_xpath('//*[@id="member_join_popup"]/div[3]/div/button').click()
    sleep(3)
    



def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_Id = '10041'
    Mission_list = [Mission_Id]
    excel = 'Email'    
    Excel_name = ['',excel]
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    submit['Mission_Id'] = Mission_Id
    print(submit)

    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Country'] = 'FR'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
