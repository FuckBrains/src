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


'''
GETAROUND
Auto
'''



def web_submit(submit,debug=0):
    # test
    if debug == 1:
        site = 'https://adpgtrack.com/click/5b73d90a6c42607b3b6c4322/146827/199595/subaccount'
        submit['Site'] = site
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    # chrome_driver.refresh()
    # chrome_driver.find_element_by_xpath('//*[@id="site-header"]/div/div/a[1]').click()
    i = 0
    while True:
        try:
            chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[1]/select')
            break
        except:
            i+=1
            if i >= 5:
                break
    # year
    num = random.randint(2010,2018) 
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[1]/select'))
    s1.select_by_value(str(num)) 
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[2]/div[1]/div/input').send_keys(submit['Auto']['firstname'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[2]/div[2]/div/input').send_keys(submit['Auto']['lastname'])
    # email
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[3]/div/input').send_keys(submit['Auto']['email'])
    # phone
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[4]/div/input').send_keys((submit['Auto']['homephone']).split('.')[0])
    # zip
    submit['Auto']['zip'] = Submit_handle.get_zip(submit['Auto']['zip'])
    chrome_driver.find_element_by_xpath('//*[@id="postal-code"]').send_keys((submit['Auto']['zip']))
    # selector
    num = random.randint(1,15)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[7]/div/select'))
    s1.select_by_index(num)     
    # button
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/button').click()
    sleep(15)
    chrome_driver.close()
    chrome_driver.quit()    
    return




 



if __name__=='__main__':
    submit = db.get_one_info()
    print(submit)
    web_submit(submit)
