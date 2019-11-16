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
    chrome_driver.close()
    chrome_driver.quit()
    chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
    if debug == 1:
        site = 'http://da.off3riz.com/aff_c?offer_id=86&aff_id=1346'
        submit['Site'] = site
    # js = 'window.location.href="%s"'(submit['Site'])
    chrome_driver.get(submit['Site'])
    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    # accept
    sleep(3)
    chrome_driver.find_element_by_xpath('//*[@id="content"]/div[3]/div/div').click()
    sleep(1)
    # sono
    index = random.randint(1,3)
    element = '//*[@id="lookingFor"]'
    s1 = Select(chrome_driver.find_element_by_xpath(element))
    s1.select_by_index(index)  
    sleep(3)    
    # next
    chrome_driver.find_element_by_xpath('//*[@id="next_step"]').click()  
    # LA MIA ETÀ:  
    sleep(3)    
    index = random.randint(3,23)
    element = '//*[@id="UserForm_yearsold"]'
    s1 = Select(chrome_driver.find_element_by_xpath(element))
    s1.select_by_index(index)  
    # next
    chrome_driver.find_element_by_xpath('//*[@id="next_step"]').click()  
    sleep(3)

    # next    
    chrome_driver.find_element_by_xpath('//*[@id="next_step"]').click()  
    sleep(3)

    # email
    email = submit['it_soi']['email']
    chrome_driver.find_element_by_xpath('//*[@id="UserForm_email"]').send_keys(email)
    sleep(3)

    # pwd
    element = chrome_driver.find_element_by_xpath('//*[@id="UserForm_password"]')
    element.click()
    pwd = Submit_handle.password_get_Nostale()
    element.send_keys(pwd) 
    # next
    sleep(3)

    chrome_driver.find_element_by_xpath('//*[@id="start_button"]').click()   
    sleep(180)
    chrome_driver.close()
    chrome_driver.quit()    
    return 1




def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10059']
    excel = 'it_soi'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Mission_Id'] = '10059'
    submit['Country'] = 'IT'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
