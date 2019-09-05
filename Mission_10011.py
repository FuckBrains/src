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
import emaillink
import Submit_handle
import selenium_funcs


'''
Health-insurance
Auto
'''



def web_submit(submit,debug = 0):
    # test
    if debug == 1:
        site = 'http://ads.g4-tracking.com/aff_c?offer_id=2954&aff_id=58624'
        submit['Site'] = site
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    # sleep(2000)
    chrome_driver.maximize_window()
    # chrome_driver.refresh()
    # sleep(1000)
    # page1
    # zip
    chrome_driver.find_element_by_xpath('//*[@id="zip_code"]').send_keys(submit['Auto']['zip'])
    sleep(1)
    # button
    chrome_driver.find_element_by_xpath('//*[@id="get_quotes"]').click()
    # sleep(30)
    # page2
    # height_ft selector
    num_info = Submit_handle.get_height_info()
    handle = chrome_driver.current_window_handle
    while True:
        try:
            chrome_driver.switch_to.window(handle)
            print(chrome_driver.current_url)
            handles=chrome_driver.window_handles
            print(handles)
            # print(chrome_driver.page_source)
            element = selenium_funcs.scroll_and_find(chrome_driver,'//*[@id="occupation"]')
            print('break')
            break
        except Exception as e:
            print(str(e))
            print('sleep')
            sleep(2)
    element = selenium_funcs.scroll_and_find(chrome_driver,'//*[@id="height_feet"]')
    sleep(2)
    s1 = Select(element)
    s1.select_by_value(num_info['Height_FT'])      
    # height_in selector
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="height_inches"]'))
    s1.select_by_value(num_info['Height_Inch'])       
    # weight input
    element = chrome_driver.find_element_by_xpath('//*[@id="weight"]')
    element.send_keys(num_info['Weight'])
    # occupation selector
    num_rent = random.randint(5,20)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="occupation"]'))
    s1.select_by_index(num_rent)       
    # annual income input
    num_income = random.randint(1,9)*10000+random.randint(0,9)*1000
    chrome_driver.find_element_by_xpath('//*[@id="income"]').send_keys(num_income)    
    # education level selector
    num_rent = random.randint(1,7)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="education_level"]'))
    s1.select_by_index(num_rent)       
    # dateofbirth_mm selector
    birthday = Submit_handle.get_auto_birthday(submit['Auto']['dateofbirth'])
    mm = birthday[0]
    day = birthday[1]
    year = birthday[2]    
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="dob_month"]'))
    s1.select_by_index(int(mm))       
    # dateofbirth_dd selector

    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="dob_day"]'))
    s1.select_by_index(int(day))       
    # dateofbirth_year selector
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="dob_year"]'))
    s1.select_by_value(year)       
    # marital status selector
    num_marital_status = random.randint(1,6)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="marital_status"]'))
    s1.select_by_index(num_marital_status)       
    # gender button
    if submit['Auto']['gender'] == 'Female':
        chrome_driver.find_element_by_xpath('//*[@id="applicant_info_div"]/div[16]/div/div/div[2]/label').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="applicant_info_div"]/div[16]/div/div/div[1]/label').click()    
    sleep(2)
    # next button
    chrome_driver.find_element_by_xpath('//*[@id="applicant_info_button"]').click()

    sleep(2000)



 

def email_confirm(submit):
    print('----------')
    for i in range(5):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']
            title = 'Activate Membership to Start Earning Rewards'
            pattern = r'.*?(https://opinionoutpost.com/Membership/Intake\?signuptoken=.*?\&resp=([0-9]{5,15}))'
            url_link = emaillink.get_email(name,pwd,title,pattern)
            if url_link != '':
                break
        except Exception as e:
            print(str(e))
            print('===')
            pass
    return url_link





def test_2():
    Country ='US'
    Mission_list = ['10004']
    Email_list = ['hotmail','aol.com','yahoo.com','outlook.com']
    Excel_names = ['Auto','Usloan']
    dateofbirth_list = []
    for i in range(30):
        submit = db.read_one_info(Country,Mission_list,Email_list,Excel_names)
        # print(submit['Auto']['dateofbirth'])    
        dateofbirth_list.append(submit['Auto']['dateofbirth'])
    print('=================')
    print(dateofbirth_list)
    dateofbirth_list = ['9/19/1989', '9/19/1989', '9/19/1989', '6/25/1952', '12/21/1962', '3/18/1948', '11/13/1985', '6/25/1952', '11-01-1978', '10-07-1957', '11/13/1985', '10-07-1957', '10-02-1962', '12/21/1971', '3/13/1981', '11/13/1985', '12/21/1962', '09-01-1952', '10-07-1957', '12/21/1971', '9/19/1989', '7/19/1948', '5/31/1985', '09-01-1952', '11-11-1947', '3/13/1981', '3/18/1948', '12-08-1969', '01-05-1985', '9/19/1989']
    for date in dateofbirth_list:
        if '/' in date:
            birthday = date.split('/')
        elif '-' in date:
            birthday = date.split('-')
        print(birthday)




if __name__=='__main__':    
    submit = db.get_one_info()
    print(submit)
    web_submit(submit,1)
