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
    Excel_tag = 'Auto'    
    if debug == 1:
        site = 'http://tracking.axad.com/aff_c?offer_id=181&aff_id=2138'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    chrome_driver.refresh()
    # click
    # Do you have car insurance
    

    sleep(2000)

    # mm
    num = random.randint(0,10)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="MonthDropdown"]'))
    s1.select_by_index(num)

    # dd
    num = random.randint(0,22)    
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="DayDropdown"]'))
    s1.select_by_index(num)

    # year
    year = random.randint(1985,2005)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="YearDropdown"]'))
    s1.select_by_value(str(year))  

    # username
    username = name_get_random(submit[Excel_tag])
    username = submit[Excel_tag]['firstname']+submit[Excel_tag]['lastname']
    chrome_driver.find_element_by_xpath('//*[@id="signup-username"]').send_keys(username)

    # pwd
    pwd = Submit_handle.password_get()
    chrome_driver.find_element_by_xpath('//*[@id="signup-password"]').send_keys(pwd)

    # gender    
    if  submit[Excel_tag]['gender']== 'Female':
        chrome_driver.find_element_by_xpath('//*[@id="FemaleButton"]/div').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="MaleButton"]/div').click()
    # signup
    chrome_driver.find_element_by_xpath('//*[@id="signup-button"]').click()
    sleep(20)
    chrome_driver.close()
    chrome_driver.quit()
    return 1


def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10046']
    excel = 'Auto'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Mission_Id'] = '10046'
    submit['Country'] = 'US'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)

def test1():
    num_gender = random.randint(0,1)
    print(num_gender)


if __name__=='__main__':
    test()