'''
resslead
First Choice Auto Loan
http://resslead.o18.click/c?o=715556&m=1846&a=39977
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
        site = 'http://resslead.o18.click/c?o=715556&m=1846&a=39977'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()    
    # new car old car
    try:
        num_gender = random.randint(0,1)
        if num_gender == 0:
            chrome_driver.find_element_by_xpath('//*[@id="lander_submit"]').click()
        else:
            chrome_driver.find_element_by_xpath('//*[@id="lander_submit"]').click()
        sleep(3)
        # firstname
        chrome_driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(submit['Uspd']['first_name'])
        # lastname
        chrome_driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(submit['Uspd']['last_name'])
    except:
        print('submit wrong')
        chrome_driver.close()
        chrome_driver.quit()
        return 0
    # email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Uspd']['email'])
    #  phone
    chrome_driver.find_element_by_xpath('//*[@id="home_phone"]').send_keys(submit['Uspd']['home_phone'])
    # home adress
    chrome_driver.find_element_by_xpath('//*[@id="address"]').send_keys(submit['Uspd']['address']) 
    # zip
    zipcode = Submit_handle.get_zip(submit['Uspd']['zip'])
    chrome_driver.find_element_by_xpath('//*[@id="zip_code"]').send_keys(zipcode)  
    # city
    chrome_driver.find_element_by_xpath('//*[@id="city"]').send_keys(submit['Uspd']['city'])
    # birth
    date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])
    for key in date_of_birth[0]:
        chrome_driver.find_element_by_xpath('//*[@id="dob"]').send_keys(key)
    for key in date_of_birth[1]:
        chrome_driver.find_element_by_xpath('//*[@id="dob"]').send_keys(key)
    for key in date_of_birth[2]:
        chrome_driver.find_element_by_xpath('//*[@id="dob"]').send_keys(key)                
    # ssn
    chrome_driver.find_element_by_xpath('//*[@id="ssn"]').send_keys(submit['Uspd']['ssn'])
    sleep(5)
    # credit type
    num_credit = random.randint(1,2)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="creditscore"]'))
    s1.select_by_index(num_credit)
    sleep(5)
    #  Time at Residence
    num_residence = random.randint(0,8)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="res_year"]'))
    s1.select_by_index(num_residence)
    sleep(5)
    # Rent or Own Your Home? 
    num_rent = random.randint(1,2)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="rent_own"]'))
    s1.select_by_index(num_rent)
    sleep(5)
    # Monthly Mortgage or Rent 
    num_monthly = random.randint(1,16)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="rent"]'))
    s1.select_by_index(num_monthly)
    sleep(5)
    # employer name 
    chrome_driver.find_element_by_xpath('//*[@id="emp"]').send_keys(submit['Uspd']['employer'])
    # Position
    chrome_driver.find_element_by_xpath('//*[@id="emp_title"]').send_keys(submit['Uspd']['occupation'])
    # time at work
    num_work = random.randint(1,9)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="emp_year"]'))
    s1.select_by_index(num_work)
    sleep(5)
    # monthly income
    num_income = random.randint(1,7)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="income"]'))
    s1.select_by_index(num_income)
    sleep(5)
    # work phone number
    chrome_driver.find_element_by_xpath('//*[@id="emp_phone"]').send_keys(submit['Uspd']['work_phone'])
    #  Available
    num_done = random.randint(0,1)
    if num_done == 0:
        chrome_driver.find_element_by_xpath('//*[@id="confirm"]/div[14]/div[2]/div/div/div/span[2]').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="confirm"]/div[14]/div[2]/div/div/div/span[3]').click()
    sleep(3)
    # click
    chrome_driver.find_element_by_xpath('//*[@id="certify"]').click()
    sleep(3)
    # Apply
    chrome_driver.find_element_by_xpath('//*[@id="confirm_submit"]').click() 
    sleep(30)
    return 1
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
    # print(submit['Uspd']['first_name'])
    # print(submit['Uspd']['last_name'])
    # print(submit['Uspd']['email'])
    # print(submit['Uspd']['date_of_birth'])
    # print(submit['Uspd']['ssn'])


 

def test1():
    num_gender = random.randint(0,1)
    print(num_gender)


if __name__=='__main__':
    test()
    print('......')