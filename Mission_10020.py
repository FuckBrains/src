'''
cpagrip
Get the Best Nutella Package!
http://zh.moneymethods.net/click.php?c=7&key=bbcprqa35ns2a5f44z14k2k3
Uspd
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
        site = 'http://lub.lubetadating.com/c/13526/1?clickid=[clickid]&bid=[bid]&siteid=[siteid]&countrycode=[cc]&operatingsystem=[operatingsystem]&campaignid=[campaignid]&category=[category]&connection=[connection]&device=[device]&browser=[browser]&carrier=[carrier]'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()    
    # sleep(2000)
    # chrome_driver.find_element_by_xpath('').click()
    # chrome_driver.find_element_by_xpath('').send_keys(submit['Uspd']['state'])
    if 'https://vouchersavenue.com/' not in chrome_driver.current_url:
    	print('Url wrong!!!!!!!!!!!!!!!!!')
    	chrome_driver.close()
    	chrome_driver.quit()
    	return 0
    # mrs mr
    num_gender = random.randint(0,1)
    if num_gender == 0:
    	chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[1]/div/div[1]/label').click()
    else:
    	chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[1]/div/div[2]/label').click()
    # chrome_driver.find_element_by_xpath().click()
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[2]/input').send_keys(submit['Uspd']['first_name'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[3]/input').send_keys(submit['Uspd']['last_name'])
    # address
    chrome_driver.find_element_by_xpath('//*[@id="address"]').send_keys(submit['Uspd']['address'])
    # zipcode
    zipcode = Submit_handle.get_zip(submit['Uspd']['zip'])
    print('zipcode:',zipcode)
    for key in zipcode:
        chrome_driver.find_element_by_xpath('//*[@id="postal_code"]').send_keys(int(key))
    # city
    chrome_driver.find_element_by_xpath('//*[@id="locality"]').send_keys(submit['Uspd']['city'])
    # state
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[7]/select'))
    s1.select_by_value(submit['Uspd']['state'])    
    # email
    chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[8]/input').send_keys(submit['Uspd']['email'])
    # cellphone
    cellphone = Submit_handle.chansfer_float_into_int(submit['Uspd']['home_phone'])
    print('cellphone:',cellphone)
    for key in cellphone:
        chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[9]/input').send_keys(int(key))
    date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])
    # MM
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="month"]'))
    s1.select_by_value(date_of_birth[0])    
    # DD
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="day"]'))
    s1.select_by_value(date_of_birth[1])     
    # Year
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="year"]'))
    s1.select_by_value(date_of_birth[2])   
    sleep(5)

    # i agree
    element = selenium_funcs.scroll_and_find_up(chrome_driver,'//*[@id="signupForm"]/div[12]/label/input')
    element.click()
    # sleep(2)
    try:
        # get paid
        element = selenium_funcs.scroll_and_find_up(chrome_driver,'//*[@id="signup_coreg"]/div/div/label/input[1]')
        element.click()   
    except:
        pass     
        # chrome_driver.find_element_by_xpath('').click()    
    # chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div[12]/label/input').click()
    # continue
    chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/button').click()
    sleep(30)
    chrome_driver.refresh()
    sleep(5)
    chrome_driver.close()
    chrome_driver.quit()
    return     



def test():
    Mission_list = ['10000']
    Excel_name = ['Uspd','']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # print(submit)
    # date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])
    # print(date_of_birth)
    web_submit(submit,1)
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
    print('......')
