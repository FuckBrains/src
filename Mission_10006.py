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
import imap_test



'''
GUARDIANS_OF_AMBER_DOI(Done)
'''


def web_submit(submit,chrome_driver,debug=0):
    # test
    if debug == 1:
        site = 'https://track.adgaem.com/click?pid=1337&offer_id=62396'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()
    chrome_driver.refresh()    
    # email
    element = selenium_funcs.scroll_and_find(chrome_driver,'//*[@id="email2"]')
    element.send_keys(submit['Email']['Email_emu'])
    # pwd
    element = selenium_funcs.scroll_and_find(chrome_driver,'//*[@id="password2"]')
    element.send_keys(submit['Email']['Email_emu_pwd'])
    sleep(2)
    # button
    chrome_driver.find_element_by_xpath('//*[@id="regForm2"]/button').click()
    if site != '':
        newwindow='window.open("' + site + '");'
        chrome_driver.execute_script(newwindow)  
    else:
        flag = 1
        chrome_driver.close()
        chrome_driver.quit()
        return flag        
    handles=chrome_driver.window_handles   
    for i in handles:
        if i != handle:
            chrome_driver.switch_to.window(i)
            chrome_driver.refresh() 
            sleep(30)
            chrome_driver.close()
            chrome_driver.quit()
            return flag    



 

def email_confirm(submit):
    print('----------')
    for i in range(5):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']
            title = 'Guardians of Ember: Confirm Your Registration'
            pattern = r'.*?(https://join.guardiansofember.gameforge.com/en_GB/landing/confirm/.*?-(\w){12})'
            url_link = emaillink.get_email(name,pwd,title,pattern)
            if url_link != '':
                break
            else:
                print('Email not Received!Sleeping for 10 seconds...')
        except Exception as e:
            print('Email not Received!Sleeping for 10 seconds...')
            sleep(10)
            print(str(e))
            print('===')
    return url_link




if __name__=='__main__':
    test()

