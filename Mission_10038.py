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
from selenium.webdriver.common.action_chains import ActionChains #导入ActionChains模块
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
        site = 'https://personalloans.com/'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(3)
    try:
        chrome_driver.find_element_by_class_name('bsac-container bsac-type-custom_code').click()
    except:
        pass
    # page1
    # brightnessLine=chrome_driver.find_element_by_id('//*[@id="form"]/fieldset/div[2]/div')
    # 定位到进度条
    # brightnessLine.get_attribute("title")#通过title属性获取当前的值
    brightnessSlider=chrome_driver.find_element_by_xpath('//*[@id="form"]/fieldset/div[2]/div/div/div')
    #定位到滑动块
    move_num = random.randint(10,150)
    print('Move',move_num)
    ActionChains(chrome_driver).click_and_hold(brightnessSlider).move_by_offset(move_num,7).release().perform()#通过move_by_offset()移动滑块，-6表示在水平方向上往左移动6个像素，7表示在垂直方向上往上移动7个像素    
    # email address
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Uspd']['email'])
    # click
    chrome_driver.find_element_by_xpath('//*[@id="form-submit"]').click()
    sleep(10)
    # page2
    # credit type
    for i in range(10):
        try:
            chrome_driver.find_element_by_xpath('//*[@id="creditType"]')
            break
        except:
            sleep(10)
    num_ = random.randint(0,1)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="creditType"]'))
    if num_ == 0:
        s1.select_by_value('good')
    else:
        s1.select_by_value('fair')    
    sleep(1)    
    # loan reason
    num_reason = random.randint(1,12)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="loanReason"]'))
    s1.select_by_index(num_reason)
    sleep(1)    
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="fName"]').send_keys(submit['Uspd']['first_name'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="lName"]').send_keys(submit['Uspd']['last_name'])
    # birthday
    date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])   
    # mm
    chrome_driver.find_element_by_xpath('//*[@id="birthdateMonth"]').send_keys(date_of_birth[0])

    # dd
    chrome_driver.find_element_by_xpath('//*[@id="birthdateDay"]').send_keys(date_of_birth[1])

    # year
    chrome_driver.find_element_by_xpath('//*[@id="birthdateYear"]').send_keys(date_of_birth[2])
    sleep(1)
    # military
    elements = chrome_driver.find_element_by_xpath('//*[@id="label-armedForces-no"]').click()
    # continue
    element = '//*[@id="nextButton"]'
    target = selenium_funcs.scroll_and_find_up(chrome_driver,element)
    sleep(2)
    target.click()
    sleep(5)
    # page3
    # phone
    # phone = submit['Uspd']['home_phone'].split('.')[0]
    chrome_driver.find_element_by_xpath('//*[@id="phone"]').send_keys(submit['Uspd']['home_phone'].split('.')[0])
    # address
    chrome_driver.find_element_by_xpath('//*[@id="address"]').send_keys(submit['Uspd']['address'])
    # zipcode    
    chrome_driver.find_element_by_xpath('//*[@id="zip"]').send_keys(submit['Uspd']['zip'])
    # city
    chrome_driver.find_element_by_xpath('//*[@id="city"]').click()
    sleep(1)
    # length at address
    num_ = random.randint(3,10)
    print('value is :',num_)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="lengthAtAddress"]'))
    s1.select_by_value(str(num_))
    sleep(1)    

    # own home
    chrome_driver.find_element_by_xpath('//*[@id="label-rentOwn-rent"]').click()
    # employment
    # income source
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="incomeSource"]'))
    s1.select_by_value('EMPLOYMENT')
    sleep(1)    
    # time employed 
    num_time = random.randint(2,4)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="timeEmployed"]'))
    s1.select_by_index(num_time)
    sleep(1)    
    # get paid  
    num_paid = random.randint(1,4) 
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="paidEvery"]'))
    s1.select_by_index(num_paid)
    sleep(1)
    # employer name    
    chrome_driver.find_element_by_xpath('//*[@id="employerName"]').send_keys(submit['Uspd']['employer'])
    # employer's phone
    chrome_driver.find_element_by_xpath('//*[@id="employerPhone"]').send_keys(submit['Uspd']['work_phone'].split('.')[0])    
    # monthly gross income    
    num_income = random.randint(1,12)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="monthlyNetIncome"]'))
    s1.select_by_index(num_income)
    sleep(1)
    # Identity and Bank Information
    # Driver's License or state ID
    chrome_driver.find_element_by_xpath('//*[@id="license"]').send_keys(submit['Uspd']['drivers_license'].split('.')[0])    
    # ssn
    chrome_driver.find_element_by_xpath('//*[@id="ssn"]').send_keys(submit['Uspd']['ssn'].split('.')[0])    
    # bank account type
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="accountType"]'))
    s1.select_by_value('checking')
    sleep(1)
    # checkbox            
    chrome_driver.find_element_by_xpath('//*[@id="privacyPolicy"]').click()
    sleep(3)
    # mobile phone
    phone = submit['Uspd']['home_phone'].split('.')[0]    
    chrome_driver.find_element_by_xpath('//*[@id="smsCellphone"]').send_keys(phone)
    sleep(3)
    # submit
    chrome_driver.find_element_by_xpath('//*[@id="submitButton"]').click()
    db.update_plan_status(2,submit['ID'])    
    sleep(100)





def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10038']
    excel = 'Uspd'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    submit['Mission_Id'] = '10038'
    chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
