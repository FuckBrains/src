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
        site = 'https://www.cpagrip.com/show.php?l=0&u=218456&id=26188'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(3)
    # page1
    # select
    num_ = random.randint(1,2)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="vote"]'))
    s1.select_by_index(num_)        
    sleep(1)
    # input
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['health']['email'])
    sleep(1)    
    # checkbox
    chrome_driver.find_element_by_xpath('//*[@id="email-checkbox"]/label/span[1]').click()
    sleep(1)    
    # click
    chrome_driver.find_element_by_xpath('//*[@id="button-row"]/div/button').click()
    sleep(3) 
    # page2
    # zipcode
    zipcode = submit['health']['zip'].split('.')[0]
    chrome_driver.find_element_by_xpath('//*[@id="zip"]').send_keys(zipcode)

    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="fname"]').send_keys(submit['health']['firstname'])

    # lasename
    chrome_driver.find_element_by_xpath('//*[@id="lname"]').send_keys(submit['health']['lastname'])

    # address
    chrome_driver.find_element_by_xpath('//*[@id="address"]').send_keys(submit['health']['address'])

    # dateofbirth
    chrome_driver.find_element_by_xpath('//*[@id="dob_holder"]').click()
    sleep(1)
    if 'dateofbirth' in submit['health']:
        date_of_birth = Submit_handle.get_auto_birthday(submit['health']['dateofbirth'])    
    else:
        date_of_birth = Submit_handle.get_auto_birthday('')         
    for key in date_of_birth[0]:
        chrome_driver.find_element_by_xpath('//*[@id="dob_month_digit"]').send_keys(key)
    for key in date_of_birth[1]:
        chrome_driver.find_element_by_xpath('//*[@id="dob_day"]').send_keys(key)
    for key in date_of_birth[2]:
        chrome_driver.find_element_by_xpath('//*[@id="dob_year"]').send_keys(key)     

    # Mobile phone number
    home_phone = submit['health']['homephone'].split('.')[0]
    chrome_driver.find_element_by_xpath('//*[@id="phone"]').send_keys(home_phone)

    # male female
    num_ = random.randint(0,1)
    if num_ == 0:
        chrome_driver.find_element_by_xpath('//*[@id="reg-form"]/div[12]/div/div/div[1]/label/span').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="gender-f"]/label/span').click()
    # continue
    chrome_driver.find_element_by_xpath('//*[@id="reg-form"]/div[13]/div/button').click()
    sleep(30)
    return 1




def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10026']
    Excel_name = ['health','']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    print(submit)
    submit['Mission_Id'] = '10026'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
