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
        site = 'https://cpa-hub.g2afse.com/click?pid=726&offer_id=50'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()   
    chrome_driver.refresh()
    sleep(5)
    # page1
    # Do you like shop online
    chrome_driver.find_element_by_xpath('//*[@id="q1"]/div[2]').click()
    sleep(3)
    chrome_driver.find_element_by_xpath('//*[@id="q2"]/div[2]').click()
    sleep(3)
    pick = ['//*[@id="q3"]/div[2]','//*[@id="q3"]/div[4]','//*[@id="q3"]/div[3]','//*[@id="q3"]/div[5]']
    num_r = random.randint(0,3)
    chrome_driver.find_element_by_xpath(pick[num_r]).click()
    sleep(3)
    chrome_driver.find_element_by_xpath('//*[@id="q5"]/input').send_keys(submit['health']['email'])
    sleep(3)
    chrome_driver.find_element_by_xpath('//*[@id="subbtn"]').click()
    sleep(3)
    







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


def test():
    # db.email_test()
    Mission_list = ['10022']
    Excel_name = ['health','']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    print(submit)
    submit['Mission_Id'] = '10022'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
