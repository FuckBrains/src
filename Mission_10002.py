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


'''
GETAROUND
Auto
'''



def web_submit(submit,chrome_driver,debug=0):
    # test
    chrome_driver.close()
    chrome_driver.quit()
    chrome_driver = Chrome_driver.get_chrome(submit)    
    if debug == 1:
        site = 'https://adpgtrack.com/click/5b73d90a6c42607b3b6c4322/146827/199595/subaccount'
        submit['Site'] = site
    print('222222222222222222222222')
    # sleep(3)
    chrome_driver.get(submit['Site'])
    # sleep(300)    
    print(submit['Site'])
    name = name_get.gen_one_word_digit(lowercase=False)
    # chrome_driver.maximize_window()
    # chrome_driver.refresh()
    print('Loading finished')
    Excel_name = 'health'    

    # year
    sleep(5)
    selenium_funcs.scroll_and_find(chrome_driver,'//*[@id="list-lead-form"]/div[1]/select')
    sleep(2)
    num = random.randint(2010,2018) 
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[1]/select'))
    s1.select_by_value(str(num)) 
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[2]/div[1]/div/input').send_keys(submit[Excel_name]['firstname'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[2]/div[2]/div/input').send_keys(submit[Excel_name]['lastname'])
    # email
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[3]/div/input').send_keys(submit[Excel_name]['email'])
    # phone
    # phone = submit[Excel_name]['homephone']
    phone = Submit_handle.get_phone(submit[Excel_name])
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[4]/div/input').send_keys(phone)
    # zip
    submit[Excel_name]['zip'] = Submit_handle.get_zip(submit[Excel_name])
    chrome_driver.find_element_by_xpath('//*[@id="postal-code"]').send_keys((submit[Excel_name]['zip']))
    # selector
    num = random.randint(1,15)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[7]/div/select'))
    s1.select_by_index(num)     
    # button
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/button').click()
    sleep(60)
    db.update_plan_status(2,submit['ID'])        
    chrome_driver.close()
    chrome_driver.quit()  
    return 1  


def test_post(submit):
    import luminati
    # pass
    # year=2015&country=US&zipcode=37189&first_name=jone&last_name=wiliiame&
    # email=jone123%40hotmail.com&phone=615-294-9618
    # &source=Twitter&source_other=&lead_page=getaround.com%2Fsharecar
    data = {}
    data['year'] = random.randint(2010,2018)
    data['country'] = 'US'
    Excel_name = 'health'
    zip_ = Submit_handle.get_zip(submit[Excel_name])
    phone = str(Submit_handle.get_phone(submit[Excel_name]))
    phone = phone[0:3]+'-'+phone[3:6]+'-'+phone[6:]
    data['zipcode'] = zip_
    data['first_name'] = submit[Excel_name]['firstname']
    data['last_name'] = submit[Excel_name]['lastname']
    data['email'] = submit[Excel_name]['email']
    data['phone'] = phone
    data['source'] = 'Twitter'
    data['source_other'] = ''
    data['lead_page'] = 'getaround.com/sharecar'
    port = 29610
    headers = get_headers()
    url = 'https://adpgtrack.com/click/5d43f1a4a03594103a75da46/146827/233486/subaccount'
    luminati.post_lpm(data,port,url,headers,debug=1)


def get_headers():
    headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    return headers



def post_test():
    import requests
    session = requests.session()
    session.proxies = {'http': proxy,
                       'https': proxy} 
    # print('http://lumtest.com/myip.json')
    for i in range(5):
        try:
            resp=session.get("http://lumtest.com/myip.json",timeout=5)
            print('===')
            break
        except:
            print('try',i,'time')
            pass
    print(resp.text)                       
    headers = {
    'accept': 'application/json',
    'Origin': 'http://petstore.swagger.io',
    'Referer': 'http://petstore.swagger.io/?url=https://raw.githubusercontent.com/luminati-io/luminati-proxy/master/lib/swagger.json',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    # data = {}
    url = 'http://192.168.30.131:22999/api/refresh_sessions/24003'
    # url = 'http://192.168.30.131:22999/api/refresh_sessions/24002'
    try:
        resp = requests.post(url,headers=headers)
        print(resp)
        print(resp.text)
    except Exception as e:
        print(str(e))



if __name__=='__main__':
    Mission_list = ['10002']
    excel = 'health'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # chrome_driver = Chrome_driver.get_chrome()
    print(submit)
    # web_submit(submit,chrome_driver)
    test_post(submit)
