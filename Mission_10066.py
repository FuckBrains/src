# https://www.roblox.com/?v=rc&rbx_source=3&rbx_medium=cpa&rbx_campaign=1820
# roblox
'''
Adsmain
roblox
Auto
'''

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


# --test--
# --test2--



def name_get_random(submit):
    # names = []
    # username = submit['firstname']+submit['lastname']
    # names.append(username)
    # username = name_get.gen_two_words(split=' ', lowercase=False)
    # names.append(username)
    username = name_get.gen_one_word_digit(lowercase=False,digitmax=100000)
    # names.append(username)
    # num_name = random.randint(0,2)
    return username


def web_submit(submit,chrome_driver,debug=0):
    # test
    # Excel_10054 = 'Data2000'
    chrome_driver.close()
    chrome_driver.quit()
    chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
    Excel_tag = 'Ukchoujiang'    
    if debug == 1:
        site = 'https://fireads.online/link/683/50457261'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    # sleep(2000)
    # click
    # sleep(2000)
    chrome_driver.find_element_by_xpath('//*[@id="reg-form"]/div[1]/div[2]/div[2]').click()
    sleep(1)

    # choose age
    age = random.randint(19,50)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="age-field"]'))
    s1.select_by_value(str(age))
    sleep(1)
    # next
    chrome_driver.find_element_by_xpath('//*[@id="reg-form"]/div[1]/div[2]/div[2]').click()

    try:
        # next
        chrome_driver.find_element_by_xpath('//*[@id="reg-form"]/div[1]/div[2]/div[2]').click()
    except:
        pass
    # Email
    sleep(2)
    email = submit['Ukchoujiang']['email']
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
    db.update_plan_status(2,submit['ID'])
    sleep(180)
    chrome_driver.close()
    chrome_driver.quit()



def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10066']
    excel = 'Ukchoujiang'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Mission_Id'] = '10066'
    phone = submit[excel]['homephone']
    phone = Submit_handle.get_uk_phone1(phone)
    print(phone)
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)
 

def test1():
    num_gender = random.randint(0,1)
    print(num_gender)


if __name__=='__main__':
    test()