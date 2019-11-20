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


'''
Best Obama Care - US(Done)
Auto
'''


def web_submit(submit,chrome_driver,debug=0):
    # test
    if debug == 1:
        site = 'http://lub.lubetadating.com/c/12981/4?clickid=[clickid]&bid=[bid]&siteid=[siteid]&countrycode=[cc]&operatingsystem=[operatingsystem]&campaignid=[campaignid]&category=[category]&connection=[connection]&device=[device]&browser=[browser]&carrier=[carrier'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])

    chrome_driver.maximize_window()
    chrome_driver.refresh()
    # sleep(1000)
    # page1
    chrome_driver.find_element_by_xpath('//*[@id="zip-submit"]').click()
    sleep(10)
    # page2
    # zipcode
    # chrome_driver.find_element_by_xpath('//*[@id="zipcode"]').send_keys((submit['Auto']['zip'].split('.'))[0])
    # sleep(2)
    # street address
    chrome_driver.find_element_by_xpath('//*[@id="home_street"]').send_keys(submit['Auto']['address'])
    sleep(2)
    num_info = Submit_handle.get_height_info()
    # Height Ft
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="height_feet"]'))
    s1.select_by_value(str(num_info['Height_FT']))      
    # Height In
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="height_inches"]'))
    s1.select_by_value(str(num_info['Height_Inch']))      
    # Weight
    chrome_driver.find_element_by_xpath('//*[@id="weight"]').send_keys(str(num_info['Weight']))
    # Household Size
    index = random.randint(1,4)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="household_size"]'))
    s1.select_by_index(index)      
    # Income
    index = random.randint(6,12)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="income"]'))
    s1.select_by_index(index)      
    # button
    chrome_driver.find_element_by_xpath('//*[@id="submit-form-part-one"]').click()
    db.update_plan_status(1,submit['ID'])        
    sleep(3)
    # page3
    # selector1
    index = random.randint(1,4)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="life_event"]'))
    s1.select_by_index(index)
    sleep(2)       
    # button
    chrome_driver.find_element_by_xpath('//*[@id="submit-form-part-two"]').click()
    sleep(3)
    # page4
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="name_first"]').send_keys(submit['Auto']['firstname'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="name_last"]').send_keys(submit['Auto']['lastname'])

    # email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Auto']['email'])

    # mobile
    phone = Submit_handle.chansfer_float_into_int(submit['Auto']['homephone'])

    element = chrome_driver.find_element_by_xpath('//*[@id="phone_home_visible"]')
    for key in phone:
        element.send_keys(int(key))
    # birthday
    birthday = Submit_handle.get_auto_birthday(submit['Auto']['dateofbirth'])
    element = chrome_driver.find_element_by_xpath('//*[@id="date_of_birth_visible"]')
    element.click()
    for key in birthday[0]:
        element.send_keys(int(key))
    for key in birthday[1]:
        element.send_keys(int(key))
    for key in birthday[2]:
        element.send_keys(int(key))    
    sleep(2)
    # gender
    if submit['Auto']['gender'] == 'Female':
        chrome_driver.find_element_by_xpath('//*[@id="form-part-three"]/div[6]/label[3]/input').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="form-part-three"]/div[6]/label[2]/input').click()

    # button
    chrome_driver.find_element_by_xpath('//*[@id="submit-form-part-three"]').click()
    db.update_plan_status(2,submit['ID'])        
    sleep(30)
    chrome_driver.close()
    chrome_driver.quit()





 

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



def test():
    Country ='US'
    Mission_list = ['10004']
    Email_list = ['hotmail','aol.com','yahoo.com','outlook.com']
    Excel_names = ['Auto','Uspd']
    submit = db.read_one_info(Country,Mission_list,Email_list,Excel_names)
    print(submit)
    birthday = Submit_handle.get_auto_birthday(submit['Auto']['dateofbirth'])
    print(birthday)
    for key in birthday[0]:
        print(int(key))
    for key in birthday[1]:
        print(int(key))  
    print(int(birthday[2]))  
    # web_submit(submit,1)


def test_2():
    Country ='US'
    Mission_list = ['10004']
    Email_list = ['hotmail','aol.com','yahoo.com','outlook.com']
    Excel_names = ['Auto','Uspd']
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
    test()
