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
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

'''
GETAROUND
Auto
'''



def web_submit(submit,chrome_driver,debug=0):
    # test
    if debug == 1:
        site = 'https://adpgtrack.com/click/5b73d90a6c42607b3b6c4322/146827/199595/subaccount'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    print('Loading finished')
    # username
    name = submit['email'].split('@')[0]+str(random.randint(100,100000))
    chrome_driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)
    # password
    pwd = Submit_handle.get_pwd_real2()
    chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(pwd)
    # email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['email'])
    # next
    chrome_driver.find_element_by_xpath('//*[@id="nextBtn"]').click()
    WebDriverWait(chrome_driver,20).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="J2"]/div/div/div[1]/div[1]'),"Get Verified. It's Free!"))

    # page2
    # Name on Card
    fullname = submit['firstname'] + submit['lastname']
    chrome_driver.find_element_by_xpath('//*[@id="fullname"]').send_keys(fullname)   
    # card number
    chrome_driver.find_element_by_xpath('//*[@id="cc"]').send_keys(submit['card_number'])
    # month
    elem = '//*[@id="expMonth"]'
    month = str(submit['month'])
    if len(month) == 1:
        month = '0'+month
    s1 = Select(chrome_driver.find_element_by_xpath(elem))
    s1.select_by_value(month)       
    # year
    elem = '//*[@id="expYear"]'
    year = str(submit['year'])
    s1 = Select(chrome_driver.find_element_by_xpath(elem))
    s1.select_by_value(year)   
    # cvv    
    chrome_driver.find_element_by_xpath('//*[@id="cvv"]').send_keys(submit['cvv'])    
    # zip    
    chrome_driver.find_element_by_xpath('//*[@id="zip"]').send_keys(submit['zipcode'])
    # submit
    chrome_driver.find_element_by_xpath('//*[@id="signUp"]').click()
    sleep(15)
    fail_xpath = '/html/body/div[1]/div[2]/section/div/div[2]/div[2]/div/div/div/p'
    fail_text = 'Seems like something went wrong. Please try again, or contact customer service 888-548-7893.'
    success_xpath = '//*[@id="topRow"]/div/h2/span'
    success_text = 'Welcome to HookupHereNow!'
    if EC.text_to_be_present_in_element((By.XPATH,fail_xpath),fail_text):
        flag = 0
    elif EC.text_to_be_present_in_element((By.XPATH,success_xpath),success_text):
        flag = 1
    else:
        flag = 2
    return flag

 



if __name__=='__main__':
    submit = db.get_one_info()
    chrome_driver = Chrome_driver.get_chrome()
    print(submit)
    web_submit(submit,chrome_driver)
