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
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pyrobot



def web_submit_(submit,chrome_driver,debug=0):
    # test
    if debug == 1:
        site = 'http://www.baidu.com'
        submit['Site'] = site
    # js = 'window.location.href="%s"'(submit['Site'])
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(5000)


def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10023']
    excel = 'Ukchoujiang'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    submit['Mission_Id'] = '10023'
    phone = submit[excel]['homephone']
    phone = Submit_handle.get_uk_phone1(phone)
    print(phone)
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)

def web_submit(submit,chrome_driver,debug=0):
    # Mission_list = ['10023']
    # excel = 'Ukchoujiang'    
    # Excel_name = [excel,'']
    # Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    # submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    # submit['Mission_Id'] = '10023'    
    # chrome_driver = Chrome_driver.get_chrome(submit)
    # url = 'http://dategd.com/index.html'
    # chrome_driver.close()
    # chrome_driver = Chrome_driver.get_chrome_normal(submit)    
    submit['Site'] = 'http://dategd.com/index.html'
    flag = Chrome_driver.get_flag(submit['ID'])        
    print('Status in Mission_Id 10064:',flag)
    print("submit['ID']",submit['ID'])  
    Chrome_driver.set_flag(submit['ID'],2)
    flag = Chrome_driver.get_flag(submit['ID'])    
    print('Status in Mission_Id 10064 after set:',flag)
    a=b+1 
    chrome_driver.get(submit['Site'])
    sleep(3)
    handles=chrome_driver.window_handles
    print(handles)
    page_source = chrome_driver.page_source
    a = page_source.find('Block</span>')
    b = page_source.find('id="',a)
    c = page_source.find('"',b+4)
    element = page_source[b+4:c]
    print(element)
    # print(page_source)
    handle = chrome_driver.current_window_handle
    # '//*[@id="_nk54g1x38z2o"]/div[3]/span[2]'
    for i in range(10):
    	try:
    		chrome_driver.find_element_by_id(element).click()
    		break
    	except:
    		sleep(1)
    # chrome_driver.find_element_by_partial_link_text('Allow').click()
    sleep(3)
    handles=chrome_driver.window_handles
    print(handles)
    for i in handles:
        if i != handle:
            chrome_driver.switch_to.window(i)
            # url = 'https://newsadsppush.com/v1/iframe-vac/63581.html?webmaster_id=63581&host=dategd.com&&isIframe=true&deviceId=t_dz2icinqupdm&locker_source=direct&n=1'
            # chrome_driver.get(url)
            for i in range(30):
            	try:
            		chrome_driver.find_element_by_xpath('/html/body/div/div').click()
            		break
            	except:
            		sleep(1)
            print('==========')
            robot = pyrobot.Robot()
            Keys_ = pyrobot.Keys()
            # robot.key_press(Keys.tab)
            # robot.key_press(Keys.tab)
            # robot.key_press(Keys.tab)            
            ActionChains(chrome_driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()           
            ActionChains(chrome_driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()           
            ActionChains(chrome_driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()           
            robot.key_press(Keys_.enter)
            # ActionChains(chrome_driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()           
            # ActionChains(chrome_driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()           
            # ActionChains(chrome_driver).key_down(Keys.TAB).key_up(Keys.TAB).send_keys(Keys.ENTER).perform()                       
            # ActionChains(chrome_driver).send_keys(Keys.ENTER).perform()
            print('++++')  
            sleep(30)                    
            # isSucess=chrome_driver.switch_to.alert.text
            # print(isSucess)
            # #确定
            # chrome_driver.switch_to.alert.accept()
            # chrome_driver.find_element_by_partial_link_text('Allow').click()
    sleep(30)
    return 0

def cpl():
	submit = {}
	chrome_driver = Chrome_driver.get_chrome_normal()
	web_submit(submit,chrome_driver)

if __name__=='__main__':
    cpl()
