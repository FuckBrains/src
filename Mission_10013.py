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
        site = 'https://www.roblox.com/?v=rc&rbx_source=3&rbx_medium=cpa&rbx_campaign=1820'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    # click
    # sleep(2000)
    sleep(2)
    print('Loading finished')
    # mm
    # index_ = random.randint(2,10)

    # js = '$("#MonthDropdown > option:nth-child('+str(index_)+')").attr("selected","selected")'
    # chrome_driver.execute_script(js)    
    # sleep(2)
    # chrome_driver.find_element_by_xpath('//*[@id="MonthDropdown"]').click()
    num = random.randint(0,10)
    element = chrome_driver.find_element_by_xpath('//*[@id="MonthDropdown"]')
    s1 = Select(element)
    print(len(s1.options))
    options = s1.options
    for i in range(60):
        if len(options) <= 1:
            sleep(1)
        else:
            break    
    for option in options:
        print(option.text)
        sc = option.get_attribute("selected")
        if sc == 'true':
            chrome_driver.execute_script('arguments[0].removeAttribute(arguments[1])',option, 'selected')
            sc = option.get_attribute("selected")
            print(sc)
            # option.removeAttribute('selected')
            # print(sc)
            print('================')   
    # js="$('#MonthDropdown > option:nth-child(1)').removeAttr('selected')"
    # chrome_driver.execute_script(js)                 
    s1.select_by_index(num)


    # dd
    # index_ = random.randint(2,22)
    js="$('#DayDropdown > option:nth-child(1)').removeAttr('selected')"
    chrome_driver.execute_script(js)
    # js = '$("#DayDropdown > option:nth-child('+str(index_)+')").attr("selected","selected")'
    # chrome_driver.execute_script(js)      
    # sleep(2)
    # chrome_driver.find_element_by_xpath('//*[@id="DayDropdown"]').click()
    num = random.randint(0,22)    
    element = chrome_driver.find_element_by_xpath('//*[@id="DayDropdown"]')
    s1 = Select(element)
    print(len(s1.options))
    for option in s1.options:
        print(option.text)
        # print(option.value)
    s1.select_by_index(num)  
    # return  

    # year
    # index_ = random.randint(20,40)
    js="$('#YearDropdown > option:nth-child(1)').removeAttr('selected')"
    chrome_driver.execute_script(js)
    # js = '$("#YearDropdown > option:nth-child('+str(index_)+')").attr("selected","selected")'
    # chrome_driver.execute_script(js)      
    # sleep(2)
    # chrome_driver.find_element_by_xpath('//*[@id="YearDropdown"]').click()
    year = random.randint(1985,2005)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="YearDropdown"]'))
    print(len(s1.options))
    for option in s1.options:
        print(option.text)
        print(option.value)    
    s1.select_by_value(str(year))  
    # sleep(3000)
    # username
    username = Submit_handle.get_name_real()
    chrome_driver.find_element_by_xpath('//*[@id="signup-username"]').send_keys(username)

    # pwd
    pwd = Submit_handle.get_pwd_real()
    chrome_driver.find_element_by_xpath('//*[@id="signup-password"]').send_keys(pwd)

    # gender    
    if  submit[Excel_tag]['gender']== 'Female':
        chrome_driver.find_element_by_xpath('//*[@id="FemaleButton"]/div').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="MaleButton"]/div').click()
    # signup
    chrome_driver.find_element_by_xpath('//*[@id="signup-button"]').click()
    db.update_plan_status(2,submit['ID'])    

    sleep(30)
    chrome_driver.close()
    chrome_driver.quit()







def test():
    Mission_list = ['10000']
    Excel_name = ['Auto','']
    Mission_list = ['10066']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Mission_Id'] = '10066'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)

 

def test1():
    num_gender = random.randint(0,1)
    print(num_gender)


if __name__=='__main__':
    test()