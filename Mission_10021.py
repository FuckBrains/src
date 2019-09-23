'''
ad1
Auto Insurance CPL
http://lub.lubetadating.com/c/10655/a?
'''
from time import sleep
import random
import os
import time
import sys
import json
import re
from urllib import request, parse
import name_get
import Chrome_driver
import email_imap as imap
import db
import name_get
import emaillink



def web_submit(submit,chrome_driver,debug=0):
    chrome_driver.get(submit['Site']) 
    # sleep(2000)   
    Mission = '10021'
    email_list = ['hotmail.com','outlook.com','gmail.com','msn.com']
    submit1 = db.get_unique_soi_email(Mission,email_list)
    submit['SOI'] = submit1['SOI']
    print(submit['SOI']['email'])
    try:
        chrome_driver.find_element_by_xpath('//*[@id="Popup_contentDiv"]/div/div/span').click()
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="show-profile"]/p[5]/input').send_keys(submit['SOI']['email'])
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="unlock"]').click()
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="show-profile"]/p[5]/div/a').click()
    except Exception as e:
        sleep(3)
        chrome_driver.close()
        chrome_driver.quit()
        return 1


def test():
    # db.email_test()
    Mission_list = ['10009']
    Excel_name = ['SOI','']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # db.read_all_info()
    print(submit)
    # chrome_driver = Chrome_driver.get_chrome()
    web_submit(submit,debug=0)


if __name__ == '__main__':
    test()
