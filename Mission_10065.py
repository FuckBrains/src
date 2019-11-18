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
    Excel_tag = 'Ukchoujiang'    
    if debug == 1:
        site = 'https://www.roblox.com/?v=rc&rbx_source=3&rbx_medium=cpa&rbx_campaign=1820'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(2)
    # mm
    # index_ = random.randint(2,10)
    js="$('#MonthDropdown > option:nth-child(1)').removeAttr('selected')"
    chrome_driver.execute_script(js)
    num = random.randint(0,10)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="MonthDropdown"]'))
    s1.select_by_index(num)


    # dd
    # index_ = random.randint(2,22)
    js="$('#DayDropdown > option:nth-child(1)').removeAttr('selected')"
    chrome_driver.execute_script(js)
    num = random.randint(0,22)    
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="DayDropdown"]'))
    s1.select_by_index(num)    

    # year
    # index_ = random.randint(20,40)
    js="$('#YearDropdown > option:nth-child(1)').removeAttr('selected')"
    chrome_driver.execute_script(js)
    year = random.randint(1985,2005)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="YearDropdown"]'))
    s1.select_by_value(str(year))   

    # username
    username = Submit_handle.get_name_real()
    chrome_driver.find_element_by_xpath('//*[@id="signup-username"]').send_keys(username)
    sleep(2)
    # pwd
    pwd = Submit_handle.get_pwd_real()
    chrome_driver.find_element_by_xpath('//*[@id="signup-password"]').send_keys(pwd)

    # gender
    num_ = random.randint(0,1) 
    if  num_==0:
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
    Mission_list = ['10000']
    excel = 'Ukchoujiang'
    Excel_name = ['Ukchoujiang','']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    print(submit)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]    
    # date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])
    # print(date_of_birth)
    # web_submit(submit,1)
    # print(submit['Uspd'])
    # print(submit['Uspd']['state'])
    # print(submit['Uspd']['city'])
    # print(submit['Uspd']['zip'])
    # print(submit['Uspd']['date_of_birth'])
    # print(submit['Uspd']['ssn'])

 

def test1():
    num_gender = random.randint(0,1)
    print(num_gender)


if __name__=='__main__':
    test()