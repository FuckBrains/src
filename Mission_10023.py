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
        site = 'https://www.cpagrip.com/show.php?l=0&u=218456&id=23359'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(3)
    # page1
    # click
    chrome_driver.find_element_by_xpath('//*[@id="ytta"]').click()
    # how old
    old = ['//*[@id="q2"]/div[1]/label','//*[@id="q2"]/div[2]/label','//*[@id="q2"]/div[3]/label','//*[@id="q2"]/div[4]/label']
    age_num = random.randint(0,3)
    age = old[age_num]
    chrome_driver.find_element_by_xpath(age).click()
    # how many times to use facebook
    # how old
    old = ['//*[@id="q3"]/div[1]/label','//*[@id="q3"]/div[2]/label','//*[@id="q3"]/div[3]/label','//*[@id="q3"]/div[4]/label']
    age_num = random.randint(0,3)
    age = old[age_num]
    chrome_driver.find_element_by_xpath(age).click()    
    sleep(30)
    # page2
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="fn"]').send_keys(submit['Ukchoujiang']['firstname'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="ln"]').send_keys(submit['Ukchoujiang']['lastname'])
    # email
    chrome_driver.find_element_by_xpath('//*[@id="em"]').send_keys(submit['Ukchoujiang']['email'])
    # primary phone
    phone = submit['Ukchoujiang']['homephone']
    phone = Submit_handle.get_uk_phone1(phone)    
    chrome_driver.find_element_by_xpath('//*[@id="tel"]').send_keys(phone)
    # postcode
    chrome_driver.find_element_by_xpath('//*[@id="pc"]').send_keys(submit['Ukchoujiang']['zip'])
    # street address
    chrome_driver.find_element_by_xpath('//*[@id="ad"]').send_keys(submit['Ukchoujiang']['address'])
    # city
    chrome_driver.find_element_by_xpath('//*[@id="city"]').send_keys(submit['Ukchoujiang']['city'])
    # country
    chrome_driver.find_element_by_xpath('//*[@id="pt"]').send_keys(submit['Ukchoujiang']['country'])
    # date_of_birth
    date_of_birth = Submit_handle.get_auto_birthday('')
    # mm
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="dobday"]'))
    s1.select_by_value(date_of_birth[1])        
    sleep(3)
    # dd
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="dobmonth"]'))
    s1.select_by_value(date_of_birth[0])        
    sleep(3) 
    # year
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="DOBYEAR"]'))
    s1.select_by_value(date_of_birth[2])        
    sleep(3)
    # gender
    num_ = random.randint(0,1)
    if num_ == 0:
        chrome_driver.find_element_by_xpath('//*[@id="fieldslider"]/div[10]').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="fieldslider"]/div[11]').click()
    sleep(1)
    # checkbox
    chrome_driver.find_element_by_xpath('//*[@id="gdpr"]').click()
    sleep(1)
    # button
    chrome_driver.find_element_by_xpath('//*[@id="subbtn"]').click()
    sleep(300)
    return 1
    



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
