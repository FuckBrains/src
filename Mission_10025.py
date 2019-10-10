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
        site = 'https://www.cpagrip.com/show.php?l=0&u=218456&id=20581'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    # yes up
    chrome_driver.find_element_by_xpath('//*[@id="onesignal-popover-allow-button"]').click()
    sleep(1)
    # yes
    chrome_driver.find_element_by_xpath('//*[@id="question-box"]/div[1]/a[1]').click()
    sleep(1)
    # home owner
    chrome_driver.find_element_by_xpath('//*[@id="question-box"]/div[2]/a[1]').click()
    sleep(10)
    # accept
    chrome_driver.find_element_by_xpath('//*[@id="qubiq-container"]/main/div/form/div/div[3]/div/div/button').click()    
    sleep(1)
    # email
    chrome_driver.find_element_by_name('ld_email').send_keys(submit['Ukchoujiang']['email'])
    sleep(1)
    # next
    chrome_driver.find_element_by_xpath('//*[@id="qubiq-container"]/main/div/form/div/div[3]/button').click()
    sleep(1)
    # gender    
    num_ = random.randint(0,1)
    if num_ == 0:
        chrome_driver.find_element_by_xpath('//*[@id="ld_title_Mr"]').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="ld_title_Ms"]').click()
    sleep(2)
    # zipcode
    chrome_driver.find_element_by_name('ld_zip_code').send_keys(submit['Ukchoujiang']['zip'])
    sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="qubiq-container"]/main/div/form/div/div[3]/button').click()
    sleep(10)
    # date_of_birth
    date_of_birth = Submit_handle.get_auto_birthday('')
    # dd
    s1 = Select(chrome_driver.find_element_by_name('ld_dayob'))
    s1.select_by_value(date_of_birth[1])        
    sleep(3)
    # mm
    s1 = Select(chrome_driver.find_element_by_xpath('ld_monthob'))
    s1.select_by_value(date_of_birth[0])        
    sleep(3) 
    # year
    s1 = Select(chrome_driver.find_element_by_xpath('ld_yearob'))
    s1.select_by_value(date_of_birth[2])        
    sleep(3)
    # firstname
    chrome_driver.find_element_by_name('fname').send_keys(submit['Ukchoujiang']['firstname'])
    # lastname
    chrome_driver.find_element_by_name('lname').send_keys(submit['Ukchoujiang']['lastname'])
    # mobile phone
    phone = submit['Ukchoujiang']['homephone']
    phone = Submit_handle.get_uk_phone1(phone)
    chrome_driver.find_element_by_name('ld_phone_cell').send_keys(phone)

    # address no
    chrome_driver.find_element_by_name().send_keys()

    street_no = random.randint(1,30)
    sleep(2)
    # checkbox
    chrome_driver.find_element_by_class_name('answer-checkbox').click()
    sleep(2)
    # continue
    chrome_driver.find_element_by_class_name('button-next').click()
    sleep(120)
    return 1


def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10024']
    excel = 'Ukchoujiang'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Mission_Id'] = '10024'
    phone = submit[excel]['homephone']
    phone = Submit_handle.get_uk_phone1(phone)
    print(phone)
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()