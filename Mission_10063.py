'''
adpump
Nostale_FR
https://adpgtrack.com/click/5d15c5d8a035945cc309af93/157000/224520/subaccount
Uspd
'''
from selenium.webdriver import ActionChains
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
    # email_list = ['aol.com','gmail.com','hotmail.com','outlook.com']
    # Mission_list = ['10052']    
    # print(submit['Email'])
    # end = submit['Email']['Email_emu'].split('@')[1]
    # print(end)
    # if end not in email_list:
    #     email = db.read_one_selected_email(Mission_list,email_list)
    #     print(email)
    #     if len(email) == 0:
    #         return
    #     if debug == 0:
    #         db.write_one_info(Mission_list,email,Cookie = '')        
    #     submit['Email'] = email['Email']
    # print(submit['Email'])
    # return
    if debug == 1:
        site = 'https://w.myspicylinks.com/index.php?id_promo=5024105_1&promokeys=e180940561f0ce6b151baadf02d96fef'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    # yes next
    element = '//*[@id="questions"]/div[1]/div[2]/a[1]'
    element = selenium_funcs.scroll_and_find_up(chrome_driver,element)
    element.click()
    sleep(1)
    # 2
    element = '//*[@id="questions"]/div[2]/div[2]/a[1]'
    element = selenium_funcs.scroll_and_find_up(chrome_driver,element)
    element.click()
    sleep(1)

    # 3
    element = ['//*[@id="questions"]/div[3]/div[2]/a[1]','//*[@id="questions"]/div[3]/div[2]/a[2]','//*[@id="questions"]/div[3]/div[2]/a[3]']
    num = random.randint(0,2)
    chrome_driver.find_element_by_xpath(element[num]).click()
    sleep(1)

    # 4
    element = ['//*[@id="questions"]/div[4]/div[2]/a[1]','//*[@id="questions"]/div[4]/div[2]/a[2]','//*[@id="questions"]/div[4]/div[2]/a[3]','//*[@id="questions"]/div[4]/div[2]/a[4]','//*[@id="questions"]/div[4]/div[2]/a[5]','//*[@id="questions"]/div[4]/div[2]/a[6]']
    num = random.randint(0,5)
    chrome_driver.find_element_by_xpath(element[num]).click()
    sleep(1)
    try:
        chrome_driver.find_element_by_xpath('//*[@id="questions"]/div[5]/div[2]/a[1]').click()
    except:
        pass

    sleep(10)
    # email
    email = submit['fr_soi']['email']
    try:
        chrome_driver.find_element_by_xpath('//*[@id="emailPG"]').send_keys(email)
    except:
        return 1
    sleep(1)
    element = chrome_driver.find_element_by_xpath('//*[@id="pg_submit"]')
    actions = ActionChains(chrome_driver)
    actions.move_to_element_with_offset(element,30,15).click().perform()
    num = random.randint(180,300)
    sleep(num)
    return 1
   

def test():
    Mission_list = ['10000']
    excel = 'fr_soi'
    Excel_name = ['fr_soi','']
    Email_list = ['hotmail.com','outlook.com','','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # print(submit)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]

    # date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])
    # print(date_of_birth)
    submit['Mission_Id'] = '10048'
    submit['Country'] = 'FR'    
    chrome_driver = Chrome_driver.get_chrome(submit)    
    web_submit(submit,chrome_driver,1)
    # print(submit['Email'])
    # print(submit['Email']['Email_emu'])
    # print(submit['Email']['Email_emu_pwd'])
    # # print(submit['Uspd']['zip'])
    # # print(submit['Uspd']['date_of_birth'])
    # # print(submit['Uspd']['ssn'])

 

def test1():
    num_gender = random.randint(0,1)
    print(num_gender)


if __name__=='__main__':
    test()
    print('......')