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
        site = 'http://da.off3riz.com/aff_c?offer_id=625&aff_id=1230'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(3)
    # comfirm
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div/a').click()
    # click
    rand_1 = ['/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/a','/html/body/div[1]/div[2]/div/div[3]/div[1]/div[2]/a','/html/body/div[1]/div[2]/div/div[3]/div[1]/div[3]/a','/html/body/div[1]/div[2]/div/div[3]/div[1]/div[4]/a']
    rand_num = random.randint(0,3)
    chrome_driver.find_element_by_xpath(rand_1[rand_num]).click()
    # click2
    rand_2 = ['/html/body/div[1]/div[2]/div/div[4]/div[1]/div[1]/a','/html/body/div[1]/div[2]/div/div[4]/div[1]/div[2]/a','/html/body/div[1]/div[2]/div/div[4]/div[1]/div[3]/a','/html/body/div[1]/div[2]/div/div[4]/div[1]/div[4]/a']
    rand_num = random.randint(0,3)    
    chrome_driver.find_element_by_xpath(rand_2[rand_num]).click()
    # click3
    rand_3 = ['/html/body/div[1]/div[2]/div/div[5]/div[1]/div[1]/a','/html/body/div[1]/div[2]/div/div[5]/div[1]/div[2]/a','/html/body/div[1]/div[2]/div/div[5]/div[1]/div[3]/a','/html/body/div[1]/div[2]/div/div[5]/div[1]/div[4]/a']
    rand_num = random.randint(0,3)    
    chrome_driver.find_element_by_xpath(rand_3[rand_num]).click()
    # click4
    rand_4 = ['/html/body/div[1]/div[2]/div/div[6]/div[1]/div[1]/a','/html/body/div[1]/div[2]/div/div[6]/div[1]/div[2]/a','/html/body/div[1]/div[2]/div/div[6]/div[1]/div[3]/a','/html/body/div[1]/div[2]/div/div[6]/div[1]/div[4]/a']
    rand_num = random.randint(0,3)    
    chrome_driver.find_element_by_xpath(rand_4[rand_num]).click()
    sleep(10)
    # continue
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[8]/div/a').click()
    sleep(3)
    name = name_get.gen_one_word_digit(lowercase=False,digitmax=100000)

    chrome_driver.find_element_by_xpath('//*[@id="registration"]/div[2]/input').send_keys(name)
    sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="emailPG"]').send_keys(submit['fr_soi']['email'])
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="registration"]/div[4]/button').click()
    sleep_rand = random.randint(60,180)
    sleep(sleep_rand)
    db.update_plan_status(2,submit['ID'])    


def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    # Mission_list = ['10044']
    # excel = 'fr_soi'    
    # Excel_name = [excel,'']
    # Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    # submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit = {}
    submit['Mission_Id'] = '10044'
    submit['Country'] = 'FR'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)

def test1():
    num = random.randint(0,1)
    print(num)

if __name__=='__main__':
    test()
