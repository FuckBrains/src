'''
Adsmain
Trusted Health Quotes
https://track.amcmpn.com/click?pid=668&offer_id=19917
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




def web_submit(submit,debug=0):
    # test
    # Excel_10054 = 'Data2000'
    Excel_10054 = 'Uspd'    
    if debug == 1:
        site = 'https://track.amcmpn.com/click?pid=668&offer_id=19917'
        submit['Site'] = site
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    # click
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="zip-form"]/div[1]/button').click()
    sleep(5)
    # date of birth
    date_of_birth = Submit_handle.get_auto_birthday(submit[Excel_10054]['date_of_birth'])
    for key in date_of_birth[0]:
        chrome_driver.find_element_by_xpath('//*[@id="dob"]').send_keys(key)
    for key in date_of_birth[1]:
        chrome_driver.find_element_by_xpath('//*[@id="dob"]').send_keys(key)
    for key in date_of_birth[2]:
        chrome_driver.find_element_by_xpath('//*[@id="dob"]').send_keys(key)
    # height fit
    num_info = Submit_handle.get_height_info()
    chrome_driver.find_element_by_xpath('//*[@id="height-feet"]').send_keys(str(num_info['Height_FT']))
    # height in
    chrome_driver.find_element_by_xpath('//*[@id="height-inches"]').send_keys(str(num_info['Height_Inch']))
    # weight
    chrome_driver.find_element_by_xpath('//*[@id="weight"]').send_keys(str(num_info['Weight']))
    sleep(3)
    # household Size
    index = random.randint(1,11)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="household-size"]'))
    s1.select_by_index(index)
    sleep(3)
    # gender
    num_gender = random.randint(0,1)
    if num_gender == 0:
        chrome_driver.find_element_by_xpath('//*[@id="section-one"]/div[4]/div/label[1]').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="section-one"]/div[4]/div/label[2]').click()
    sleep(3)
    #  A&B
    num_AB = random.randint(0,1)
    if num_AB == 0:
        chrome_driver.find_element_by_xpath('//*[@id="section-one"]/div[5]/label[1]').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="section-one"]/div[5]/label[2]').click()
    sleep(2)
    #  health conditions
    chrome_driver.find_element_by_xpath('//*[@id="section-one"]/div[6]/label[2]').click()
    sleep(2)
    # continue
    chrome_driver.find_element_by_xpath('//*[@id="submit"]').click()
    sleep(2)
    # fisrt name
    chrome_driver.find_element_by_xpath('//*[@id="first-name"]').send_keys(submit[Excel_10054]['first_name'])
    # last name
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="last-name"]').send_keys(submit[Excel_10054]['last_name'])
    # address
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="address"]').send_keys(submit[Excel_10054]['address'])
    # zip
    chrome_driver.find_element_by_xpath('//*[@id="zip-code"]').clear()
    zipcode = Submit_handle.get_zip(submit[Excel_10054]['zip'])
    chrome_driver.find_element_by_xpath('//*[@id="zip-code"]').send_keys(zipcode)
    sleep(2)    
    # city 
    chrome_driver.find_element_by_xpath('//*[@id="city"]').send_keys(submit[Excel_10054]['city'])
    sleep(2)
    # state
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="state"]'))
    s1.select_by_value(submit[Excel_10054]['state'])
    sleep(2)
    # phone
    chrome_driver.find_element_by_xpath('//*[@id="phone-number"]').send_keys(submit[Excel_10054]['home_phone'])
    sleep(2)
    # email
    chrome_driver.find_element_by_xpath('//*[@id="email-address"]').send_keys(submit[Excel_10054]['email'])
    sleep(2)
    # click view quotes
    chrome_driver.find_element_by_xpath('//*[@id="submit"]').click()
    sleep(30)




















    # # sleep(2000)
    # # chrome_driver.find_element_by_xpath('').click()
    # # chrome_driver.find_element_by_xpath('').send_keys(submit['Uspd']['state'])

    # # firstname
    # chrome_driver.find_element_by_xpath('//*[@id="user_add_form"]/div/div/div[2]/input').send_keys(submit['Ukpd']['firstname'])    
    # # email    
    # chrome_driver.find_element_by_xpath('//*[@id="inputEmail"]').send_keys(submit['Ukpd']['email'])

    # # comfirm1
    # chrome_driver.find_element_by_xpath('//*[@id="user_add_form"]/div/div/div[13]/div/label/span').click()
    # # comfirm2
    # chrome_driver.find_element_by_xpath('//*[@id="user_add_form"]/div/div/div[14]/div/label/span').click()
    # # claim button
    # chrome_driver.find_element_by_xpath('//*[@id="user_add_form"]/div/div/button[2]').click()    
    # sleep(10)
    # try:
    #     chrome_driver.find_element_by_xpath('//*[@id="congratspopup"]/div/div/div/div/button').click()
    # except:
    #     pass
    # sleep(20)




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