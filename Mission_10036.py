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
        site = 'https://cpa-hub.g2afse.com/click?pid=726&offer_id=45'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(5)
    # page1
    # email
    chrome_driver.find_element_by_xpath('//*[@id="header"]/div/div/div[2]/input').send_keys(submit['health']['email'])
    sleep(1)
    # start now
    chrome_driver.find_element_by_xpath('//*[@id="submit-text"]').click()
    sleep(10)
    # page2
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="fn"]').send_keys(submit['health']['firstname'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="ln"]').send_keys(submit['health']['lastname'])
    # zipcode
    zipcode = submit['health']['zip'].split('.')[0]    
    chrome_driver.find_element_by_xpath('//*[@id="zip-input"]').send_keys(zipcode)
    # continue
    chrome_driver.find_element_by_xpath('//*[@id="survey-button1"]').click()
    sleep(3000)
    # page3







def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10036']
    Excel_name = ['health','']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    print(submit)
    submit['Mission_Id'] = '10036'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
