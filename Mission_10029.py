from selenium import webdriver
from selenium.webdriver import ActionChains
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
        site = 'https://track.amcmpn.com/click?pid=665&offer_id=21490'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    excel = 'Ukchoujiang'
    sleep(3)
    # gendor
    gendor = ['//*[@id="input1"]/div/div/div[3]/div[2]/div[3]/div[1]/div/label[1]/label','//*[@id="input1"]/div/div/div[3]/div[2]/div[3]/div[1]/div/label[2]/label']
    num_ = random.randint(0,1)
    chrome_driver.find_element_by_xpath(gendor[num_]).click()

    # first name
    chrome_driver.find_element_by_xpath('//*[@id="first-name"]').send_keys(submit[excel]['firstname'])

    # surname
    chrome_driver.find_element_by_xpath('//*[@id="last-name"]').send_keys(submit[excel]['lastname'])

    # email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit[excel]['email'])

    # date_of_birth  
    birthday = Submit_handle.get_auto_birthday('')      
    element = chrome_driver.find_element_by_xpath('//*[@id="input1"]/div/div/div[3]/div[2]/div[3]/div[5]/div/input')
    element.click()
    db.update_plan_status(1,submit['ID'])    
    sleep(1)
    # dd
    day = birthday[1]
    month = birthday[0]
    year = birthday[2]    
    try:
        chrome_driver.find_element_by_xpath('//*[@id="bdate-day"]').send_keys(str(day))
        # mm
        chrome_driver.find_element_by_xpath('//*[@id="bdate-month"]').send_keys(str(month))
        # year
        chrome_driver.find_element_by_xpath('//*[@id="bdate-year"]').send_keys(str(year))
    except:
        # birthday = str(day)+'/'+str(month)+'/'+str(year)
        # element.send_keys(birthday)
        return 0
    sleep(2)
    buttons = chrome_driver.find_elements_by_class_name('shineAnimation')
    for button in buttons:    
        try:
            button.click()
        except:
            pass
    # element = chrome_driver.find_element_by_xpath('//*[@id="form-submit"]/div')
    # actions = ActionChains(chrome_driver)
    # actions.move_to_element_with_offset(element,30,15).click().perform()    
    # sleep(10) 
    # continue
    buttons = chrome_driver.find_elements_by_class_name('shineAnimation')
    for button in buttons:    
        try:
            button.click()
        except:
            pass
    # element = chrome_driver.find_element_by_xpath('//*[@id="form-submit"]/div')
    # actions = ActionChains(chrome_driver)
    # actions.move_to_element_with_offset(element,30,15).click().perform()      
    # sleep(10)
    # postcode

    postcode = submit[excel]['zip']    
    for i in range(6):
        try:
            element = chrome_driver.find_element_by_xpath('//*[@id="postcode"]')
            element.send_keys(postcode)
        except:
            sleep(10)
    # address
    sleep(5)
    element = '//*[@id="address"]'
    for i in range(10):
        try:
            chrome_driver.find_element_by_xpath(element).click()   
            num = random.randint(0,1)  
            js="$('#address > option:nth-child(1)').removeAttr('selected')"
            chrome_driver.execute_script(js)      
            s1 = Select(chrome_driver.find_element_by_xpath(element))
            s1.select_by_index(num)
        except:
            sleep(10)   
    # mobile
    mobile = submit[excel]['homephone']
    mobile = mobile.replace(' ','')
    mobile = mobile[-9:]
    element = chrome_driver.find_element_by_xpath('//*[@id="phone"]')
    element.click()
    element.send_keys(mobile)
    sleep(1)
    # continue
    buttons = chrome_driver.find_elements_by_class_name('shineAnimation')
    for button in buttons:    
        try:
            button.click()
        except:
            pass
    # element = chrome_driver.find_element_by_xpath('//*[@id="form-submit"]/div')
    # actions = ActionChains(chrome_driver)
    # actions.move_to_element_with_offset(element,30,15).click().perform()  
    db.update_plan_status(2,submit['ID'])
    sleep(180)


def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10029']
    Excel_name = ['Ukchoujiang','']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # print(submit)
    submit['Mission_Id'] = '10029'
    submit['Country'] = 'GB'
    excel = 'Ukchoujiang'
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]    
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)
    # mobile = submit[excel]['homephone']
    # mobile = mobile.replace(' ','')
    # mobile = mobile[-9:]   
    # print(mobile) 


if __name__=='__main__':
    test()
