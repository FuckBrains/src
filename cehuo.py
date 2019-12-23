import Dadao
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
    # https://www.cam4.com/
    chrome_driver.get('https://www.google.com')
    sleep(1)
    print('stop')
    # while True:
    #     url = chrome_driver.current_url 
    #     print(url)
    #     if 'account.blizzard.com' in url :
    #         chrome_driver.execute_script("window.stop();") 
    #         print('stop')
    #         break
    #     else:
    #         sleep(0.5)
    chrome_driver.delete_all_cookies()
    with open('1.txt','r') as f:
        cookie_str = f.readlines()

    cookies = json.loads(cookie_str[0])
    # cookies = json.loads(submit['Cookie'])
    for cookie in cookies:
        # if 'expiry' in cookie:
        #     cookie['expiry'] = int(cookie['expiry']) 
        chrome_driver.add_cookie(cookie)  
    print('After add cookie') 
    cookies = chrome_driver.get_cookies()    
    print('cookies',cookies)    
    chrome_driver.get('https://account.blizzard.com/')     
    # chrome_driver.refresh()
    sleep(3000)

def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    # Mission_list = ['10023']
    # excel = 'Ukchoujiang'    
    # Excel_name = [excel,'']
    # Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    # submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    # submit['Mission_Id'] = '10023'
    # phone = submit[excel]['homephone']
    # phone = Submit_handle.get_uk_phone1(phone)
    # print(phone)
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)

def data_get():
    path = r'..\res\Dadao.xlsx' 
    sheet,workbook = Dadao.get_excel(path)   
    Mission_Id = 11001 
    submit = Dadao.get_one_data(sheet,Mission_Id)
    submit['Mission_Id'] = Mission_Id
    return submit
    chrome_driver = Chrome_driver.get_chrome(submit)    
    web_submit(submit,chrome_driver,debug=0)

    content = 1
    Dadao.write_status(path,workbook,submit,content)

def get_path():
    return path

def get_ip():
    for num_ip in range(6):
        try:
            city = ip_test.ip_Test('','',country=submit['country'])
            if  city != 'Not found':
                flag = 1
                proxy_info = ''
                break
            if num_ip == 5:
                print('Net wrong...!!!!!!')
                changer.Restart()
        except:
            changer.Restart()     

def get_cookie():
    path = get_path()
    with open('1.txt','r') as f:
        cookie_str = f.readlines()    

def main():
    while True:
        submit = data_get()
        if submit == None:
            return 
        get_ip(submit)


if __name__=='__main__':
    data_test()
