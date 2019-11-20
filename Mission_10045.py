'''
cpagrip
Get the Best Nutella Package!
http://zh.moneymethods.net/click.php?c=7&key=bbcprqa35ns2a5f44z14k2k3
health
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






def web_submit(submit,chrome_driver,debug=0):
    # test
    if debug == 1:
        site = 'https://axisempire022.afftrack.com/click?aid=270&linkid=T2381&s1=&s2=&s3=&s4=&s5='
        print(site)
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()    
    # sleep(2000)
    excel = 'health'
    # page1
    # gender
    num_gender = random.randint(0,1)
    if num_gender == 0:
        chrome_driver.find_element_by_xpath('//*[@id="form-step-one-top"]/div[2]/div/div/label[2]').click()
    # date_of_birth
    element = chrome_driver.find_element_by_xpath('//*[@id="form-step-one-top"]/div[3]/div/input')
    element.click()
    sleep(1)
    date_of_birth = Submit_handle.get_auto_birthday('')
    element.send_keys(date_of_birth[0])
    element.send_keys(date_of_birth[1])
    element.send_keys(date_of_birth[2])
    sleep(1)
    zipcode = Submit_handle.get_zip(submit['health']['zip'])
    print('zipcode:',zipcode)    
    chrome_driver.find_element_by_xpath('//*[@id="form-step-one-top"]/div[4]/div/input').send_keys(zipcode)
    sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="top"]').click()
    sleep(3)
    # page2
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[3]/a').click()
    sleep(2)
    # None of these happen
    try:
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[2]/div/div[6]/label/span').click()
        # continue
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[2]/a').click()
    except:
        pass
    sleep(3)
    # household size
    index = random.randint(1,4)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="houseHoldSize"]'))
    s1.select_by_index(index)   
    # household income
    index = random.randint(1,4)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="houseHoldIncome"]'))
    s1.select_by_index(index)       
    sleep(2)
    # continue
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div[2]/a').click()
    # height
    num_info = Submit_handle.get_height_info()
    chrome_driver.find_element_by_xpath('//*[@id="step2b-height_ft"]').send_keys(num_info['Height_FT'])
    chrome_driver.find_element_by_xpath('//*[@id="step2b-height_in"]').send_keys(num_info['Height_Inch'])
    chrome_driver.find_element_by_xpath('//*[@id="step2b-weight"]').send_keys(num_info['Weight'])
    sleep(2)
    # checkbox
    index = random.randint(0,2)
    if index==0:
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[5]/div[2]/div/div[1]/div[3]/div[1]/div/label').click()
    elif index == 1:
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[5]/div[2]/div/div[1]/div[3]/div[2]/div/label').click()
    else:
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[5]/div[2]/div/div[1]/div[3]/div[1]/div/label').click()
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[5]/div[2]/div/div[1]/div[3]/div[2]/div/label').click()
    sleep(2)
    # continue
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[5]/div[2]/a').click()
    sleep(5)
    # page3
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="step3-firstname"]').send_keys(submit['health']['firstname'])    
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="step3-lastname"]').send_keys(submit['health']['lastname'])    
    # email
    chrome_driver.find_element_by_xpath('//*[@id="step3-email"]').send_keys(submit['health']['email'])    
    # phone
    cellphone = Submit_handle.chansfer_float_into_int(submit['health']['homephone'].split('.')[0])
    element = chrome_driver.find_element_by_xpath('//*[@id="step3-phone"]')
    element.click()
    db.update_plan_status(1,submit['ID'])        
    print('cellphone:',cellphone)
    element.send_keys(cellphone)    
    # address
    chrome_driver.find_element_by_xpath('//*[@id="step3-address1"]').send_keys(submit['health']['address'])
    sleep(3)
    # get my quote
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[6]/div[2]/a').click()
    db.update_plan_status(2,submit['ID'])        
    sleep(300)

def test():
    Mission_list = ['10000']
    Excel_name = ['health','']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # print(submit)
    [print(item,submit['health'][item]) for item in submit['health'] if submit['health'][item]!=None]
    # zipcode = Submit_handle.get_zip(submit['health']['zip'])
    # print('zipcode:',zipcode)    
    # cellphone = Submit_handle.chansfer_float_into_int(submit['health']['homephone'].split('.')[0])
    # print('cellphone:',cellphone)    
    # print(len(cellphone))
    submit['Mission_Id'] = '10045'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)    
    # date_of_birth = Submit_handle.get_auto_birthday(submit['health']['date_of_birth'])
    # print(date_of_birth)
    # web_submit(submit,1)
    # print(submit['health'])
    # print(submit['health']['state'])
    # print(submit['health']['city'])
    # print(submit['health']['zip'])
    # print(submit['health']['date_of_birth'])
    # print(submit['health']['ssn'])

 

def test1():
    num_gender = random.randint(0,1)
    print(num_gender)


if __name__=='__main__':
    test()
    print('......')
