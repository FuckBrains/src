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
        site = 'http://viewallhealth.com/click.php?c=11&key=yoau3ub9118rgpqq3weq4062'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(5)
    # page1
    # click yes trump
    chrome_driver.find_element_by_xpath('//*[@id="choices"]/div[1]').click()
    sleep(5)
    # email
    chrome_driver.find_element_by_xpath('//*[@id="last-step"]/input').send_keys(submit['health']['email'])
    sleep(1)
    # continue
    chrome_driver.find_element_by_xpath('//*[@id="subbtn"]').click()
    sleep(15)
    # page2
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="slider-container"]/div[1]/input[1]').send_keys(submit['health']['firstname'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="slider-container"]/div[1]/input[2]').send_keys(submit['health']['lastname'])
    # zipcode
    zipcode = submit['health']['zip'].split('.')[0]
    chrome_driver.find_element_by_xpath('//*[@id="slider-container"]/div[1]/input[3]').send_keys(zipcode)
    # continue
    sleep(3)
    js = "$('#submit-btn').click()"
    chrome_driver.execute_script(js)
    sleep(3)
    # street
    chrome_driver.find_element_by_xpath('//*[@id="slider-container"]/div[2]/input').send_keys(submit['health']['address'])
    # phone
    home_phone = submit['health']['homephone'].split('.')[0]    
    for num in home_phone[0:3]:
        chrome_driver.find_element_by_xpath('//*[@id="slider-container"]/div[2]/div[2]/input[1]').send_keys(int(num))
    for num in home_phone[3:6]:
        chrome_driver.find_element_by_xpath('//*[@id="slider-container"]/div[2]/div[2]/input[2]').send_keys(int(num))
    for num in home_phone[6:]:
        chrome_driver.find_element_by_xpath('//*[@id="slider-container"]/div[2]/div[2]/input[3]').send_keys(int(num))
    sleep(3)
    js = "$('#submit-btn').click()"
    chrome_driver.execute_script(js)
    sleep(3)
    # page3
    # if 'dateofbirth' in submit['health']:
    #     date_of_birth = Submit_handle.get_auto_birthday(submit['health']['dateofbirth'])    
    # else:
    date_of_birth = Submit_handle.get_auto_birthday('')    
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="dobmonth"]'))
    s1.select_by_value(date_of_birth[0])        
    sleep(1)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="dobday"]'))
    s1.select_by_value(date_of_birth[1])        
    sleep(1) 
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="DOBYEAR"]'))
    s1.select_by_value(date_of_birth[2])        
    sleep(1)          
    num_sex = random.randint(0,1)
    if num_sex == 0:
        chrome_driver.find_element_by_xpath('//*[@id="female"]').click()
    sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="chkboxn"]').click()
    sleep(1)
    js = "$('#submit-btn').click()"
    chrome_driver.execute_script(js)
    sleep(30)
    return 1




def test():
    # db.email_test()
    Mission_list = ['10027']
    Excel_name = ['health','']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    print(submit)
    submit['Mission_Id'] = '10027'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
