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



def get_robot():
    import pyrobot as pr
    robot = pr.Robot()
    # robot.sleep(5)  
    # robot.take_screenshot().save("asdf.png", "PNG")
    Keys = pr.Keys()
    return robot,Keys
    # robot.key_press(Keys.enter)     

def web_submit(submit,chrome_driver,debug=0):
    # test
    if debug == 1:
        site = 'https://www.cpagrip.com/show.php?l=0&u=218456&id=25228'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    robot,Keys = get_robot()
    # for i in range(13):
    #     print(i)
    #     robot.key_press(Keys.tab)
    # robot.key_press(Keys.enter)
    num_ = random.randint(0,1)
    # gender
    if num_ == 0:
        chrome_driver.find_element_by_xpath('//*[@id="input1"]/div/div/div[3]/div[2]/div[3]/div[1]/div/label[1]/label').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="input1"]/div/div/div[3]/div[2]/div[3]/div[1]/div/label[2]/label').click()
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="first-name"]').send_keys(submit['Ukchoujiang']['firstname'])
    sleep(1)
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="last-name"]').send_keys(submit['Ukchoujiang']['lastname'])
    sleep(1)

    # Email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Ukchoujiang']['email'])
    sleep(1)

    # date_of_birth
    date_of_birth = Submit_handle.get_auto_birthday('')    
    chrome_driver.find_element_by_xpath('//*[@id="input1"]/div/div/div[3]/div[2]/div[3]/div[5]/div/input').click()     
    sleep(1)    
    # day
    chrome_driver.find_element_by_xpath('//*[@id="bdate-day"]').send_keys(date_of_birth[1])
    sleep(1)

    # month
    chrome_driver.find_element_by_xpath('//*[@id="bdate-month"]').send_keys(date_of_birth[0])
    sleep(1)

    # year
    chrome_driver.find_element_by_xpath('//*[@id="bdate-year"]').send_keys(date_of_birth[2])
    sleep(1)

    chrome_driver.maximize_window()
    for i in range(7):
        print(i)
        robot.key_press(Keys.tab)
    robot.key_press(Keys.enter)
    sleep(3)
    # continue
    chrome_driver.find_element_by_xpath('//*[@id="form-submit"]').click()
    sleep(300)
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
