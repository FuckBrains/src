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
        site = 'https://track.amcmpn.com/click?pid=668&offer_id=20836'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(3)
    # request sample
    chrome_driver.find_element_by_xpath('//*[@id="main-section"]/div[1]/div[1]/div/div[4]/div[1]/a/span').click()
    sleep(1)
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="first-name"]').send_keys(submit['Ukchoujiang']['firstname'])
    sleep(1)

    # surname
    chrome_driver.find_element_by_xpath('//*[@id="last-name"]').send_keys(submit['Ukchoujiang']['lastname'])
    sleep(1)

    # gender
    chrome_driver.find_element_by_xpath('//*[@id="shortform"]/div/div[2]/div[3]/div/div/div[1]/input').click()
    sleep(1)
    num_ = random.randint(0,1)
    if num_ == 0:
        chrome_driver.find_element_by_xpath('//*[@id="shortform"]/div/div[2]/div[3]/div/div/div[2]/div/label').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="shortform"]/div/div[2]/div[3]/div/div/div[3]/div/label').click()
    # email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Ukchoujiang']['email'])
    sleep(1)

    chrome_driver.find_element_by_xpath('//*[@id="shortform"]/div/div[2]/div[5]/div/div/div/div[1]/input').click()
    date_of_birth = Submit_handle.get_auto_birthday('')
    # day
    chrome_driver.find_element_by_xpath('//*[@id="bdate-date"]').send_keys(date_of_birth[1])
    sleep(1)

    # mm
    chrome_driver.find_element_by_xpath('//*[@id="bdate-month"]').send_keys(date_of_birth[0])
    sleep(1)

    # year
    chrome_driver.find_element_by_xpath('//*[@id="bdate-year"]').send_keys(date_of_birth[2])
    sleep(1)

    # click
    chrome_driver.find_element_by_xpath('//*[@id="shortform"]/div/div[4]/button').click()
    sleep(3)
    # ok continue
    chrome_driver.find_element_by_xpath('//*[@id="optinform"]/div/div/div[3]/button/span').click()
    sleep(3)
    # postcode
    chrome_driver.find_element_by_xpath('//*[@id="postcode"]').send_keys(submit['Ukchoujiang']['zip'])
    sleep(1)

    sleep(300)



def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10023']
    excel = 'Ukchoujiang'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Mission_Id'] = '10023'
    phone = submit[excel]['homephone']
    phone = Submit_handle.get_uk_phone1(phone)
    print(phone)
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()

