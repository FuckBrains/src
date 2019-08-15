'''
adpump
Nostale_FR
https://adpgtrack.com/click/5d15c5d8a035945cc309af93/157000/224520/subaccount
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
    if debug == 1:
        site = 'https://adpgtrack.com/click/5d15c5d8a035945cc309af93/157000/224520/subaccount'
        submit['Site'] = site
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    # point
    chrome_driver.find_element_by_xpath('//*[@id="scroll2"]/span').click()
    sleep(5)
    # cookies
    chrome_driver.find_element_by_xpath('//*[@id="accept_btn"]').click()
    sleep(5)  
    # play
    chrome_driver.find_element_by_xpath('//*[@id="trigger-overlay"]').click()
    sleep(5)
    # email
    chrome_driver.find_element_by_xpath('//*[@id="vld-mail"]').send_keys(submit['Email']['Email_emu'])
    # password
    chrome_driver.find_element_by_xpath('//*[@id="validate"]').send_keys(submit['Email']['Email_emu_pwd'])
    sleep(3)
    #play button
    chrome_driver.find_element_by_xpath('//*[@id="regForm1"]/button').click()
    chrome_driver.close()
    chrome_driver.quit()
    return     
def test():
    Mission_list = ['10000']
    Excel_name = ['Uspd','Email']
    Email_list = ['hotmail.com','outlook.com','','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # print(submit)
    # date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])
    # print(date_of_birth)
    web_submit(submit,1)
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