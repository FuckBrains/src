import Dadao
from selenium import webdriver
from selenium.webdriver import ActionChains
import json
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
    # https://www.cam4.com/
    cookies = get_account(submit)
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

    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry']) +86400
        chrome_driver.add_cookie(cookie)  
    print('After add cookie') 
    # cookies = chrome_driver.get_cookies()    
    # print('cookies',cookies)    
    chrome_driver.get('https://account.blizzard.com/')     
    try:
        chrome_driver.find_element_by_xpath(xpath_payment)
    except:
        chrome_driver.refresh()
    xpath_payment = '//*[@id="app"]/main/section[1]/div/ul/li[7]/a'
    flag_info = 0
    while True:
        for j in range(10):
            chrome_driver.find_element_by_xpath(xpath_payment).click()
            print('click payment method')        
            for i in range(10):
                try:
                    a = chrome_driver.find_element_by_class_name('mt-card-top')
                    print(a)
                    element = a.find_element_by_tag_name('a')
                    print(element)
                    element.click()
                    print('find and click add a new payment method')
                    break
                except Exception as e:
                    print(str(e))
                    print('find not add a new payment method')                    
                    sleep(3)
            sleep(5)
            for i in range(10):
                try:
                    chrome_driver.find_element_by_class_name('btn-primary').click()
                    print('find and click continue button')
                    break
                except:
                    print('find not continue button')                    
                    sleep(3)
            for i in range(10):
                try:
                    element = chrome_driver.find_element_by_xpath('//*[@id="firstName"]')
                    flag_info = 1
                    break
                except:
                    sleep(3)
            if flag_info !=1:
                chrome_driver.refresh()
            else:
                break
        if flag_info != 1:
            print('Does not find info page !!!!!!!!!!')
            chrome_driver.close()
            chrome_driver.quit()
            return
        info = []
        for i in range(6):
            a = get_info()
            info.append(a)
        chrome_driver.find_element_by_xpath('//*[@id="firstName"]').send_keys(info[0])        
        chrome_driver.find_element_by_xpath('//*[@id="lastName"]').send_keys(info[1])
        chrome_driver.find_element_by_xpath('//*[@id="addressLine1"]').send_keys(info[2])
        chrome_driver.find_element_by_xpath('//*[@id="city"]').send_keys(info[3])
        chrome_driver.find_element_by_xpath('//*[@id="region"]').send_keys(info[4])
        chrome_driver.find_element_by_xpath('//*[@id="postalCode"]').send_keys(info[5])
        sleep(2)
        chrome_driver.find_element_by_xpath('/html/body/app-root/div/div/app-address-selection/div/app-actions-with-cancel/div/button[1]').click()
        sleep(5)    
        flag_card = 0
        for i in range(10):
            try:
                chrome_driver.find_element_by_xpath('//*[@id="cardNumber"]')
                flag_card = 1
            except:
                sleep(3)
        if flag_card == 0:
            print('No card info to input after send info')
            chrome_driver.close()
            chrome_driver.quit()
            return
        path_card = '//*[@id="cardNumber"]'
        path_day = '//*[@id="expiryDate"]'
        path_cvv = '//*[@id="cvv"]'
        path_button = '//*[@id="primaryButton"]'
        while True:
            submit,path,workbook = get_data()
            submit['status'] = 'badname'
            for i in submit['badname']:
                submit['row'] = i
                write_status(path,workbook,submit,'badname')              
            card = submit['card_number'].replace('\t','')
            month = submit['month'].replace('\t','')
            cvv = submit['cvv'].replace('\t','')
            if len(month) == 1:
                month = '0' + month
            chrome_driver.find_element_by_xpath(path_card).send_keys(card)
            element = chrome_driver.find_element_by_xpath(path_day)
            for num in month:
                element.send_keys(int(num))
            chrome_driver.find_element_by_xpath(path_cvv).send_keys(cvv)
            sleep(2)
            chrome_driver.find_element_by_xpath(path_button).click()
            flag_error = 0
            flag_success = 0
            flag_account_ban = 0
            error_info = 'An error occurred.'
            success_info = 'Payment method successfully added'
            account_ban_info = 'Heads up!'
            for i in range(20):
                try:
                    element = chrome_driver.find_element_by_xpath('//*[@id="app"]/main/section[2]/div/div[2]/div[1]/div[2]/ul/li/span')
                    if element.text == error_info:
                        print('Find fail text')
                        flag_error = 1
                except:
                    print('Find not fail text')
                try:
                    element = chrome_driver.find_element_by_class_name('success-title')
                    if success_info in element.text:
                        print('Find success text')                        
                        flag_success = 1
                except:
                    print('Find not success text')
                try:
                    element = chrome_driver.find_element_by_xpath('/html/body/app-root/div/div/app-init-token-error/div/div[2]/h5')
                    if account_ban_info in element.text:
                        print('Find account ban text')                        
                        flag_account_ban = 1
                except:
                    print('Find not account ban text')
                if flag_error == 0 and flag_success == 0 and flag_account_ban == 0:
                    sleep(3)
                else:
                    break
            if flag_error == 1:
                '''
                fail
                '''
                print('Find fail info')
                if flag_account_ban == 1:
                    print('Account ban')
                    chrome_driver.close()
                    chrome_driver.quit()
                    return
                Dadao.write_status(path,workbook,submit,error_info)
                path_card = '//*[@id="encryptedCardNumber"]'
                path_day = '//*[@id="encryptedExpiryDate"]'
                path_cvv = '//*[@id="encryptedSecurityCode"]'
                path_button = '//*[@id="encryptedSecurityCode"]'
                try:
                    chrome_driver.find_element_by_xpath(path_card)
                except:
                    print('Does not Find card input xpath')
                    path_cardtype = '//*[@id="paymentoptionslist"]/li[3]/form/button'
                    chrome_driver.find_element_by_xpath(path_cardtype).click()
                    print('Find visa select button')
                    path_card = '//*[@id="cardNumber"]'
                    path_day = '//*[@id="expiryDate"]'
                    path_cvv = '//*[@id="cvv"]'
                    path_button = '//*[@id="primaryButton"]'
                    card_name = '//*[@id="cardholderName"]' 
                    name = submit['firstname'] + ' ' + submit['lastname']
                    for i in range(30):
                        try:
                            chrome_driver.find_element_by_xpath(card_name).send_keys(name)
                            break
                        except:
                            sleep(1)

            elif flag_success == 1:
                # success
                print('Find success info')
                Dadao.write_status(path,workbook,submit,success_info)
            elif flag_account_ban == 1:
                # account ban
                print('Find account ban info!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                chrome_driver.close()
                chrome_driver.quit()
                return
            else:
                print('Find none of success, fail or account ban info')
                sleep(3000)

def get_account(submit):
    path = select_account(submit)
    with open(path,'r') as f:
        cookie_str = f.readlines()
    print(cookie_str)
    cookies = json.loads(cookie_str[0])
    return cookies

def remove_account(file):
    os.remove(file)

def select_account(submit):
    path_country = r'..\res\cookies\US'
    modules = os.listdir(path_country)
    # print(modules)
    modules_path = [os.path.join(path_country,file) for file in modules]
    return modules_path[0]

def get_info():
    a = 'abcdefghijklmnopqrstuvwxyz'
    length = random.randint(4,8)
    b = []
    for i in range(length):
        c = random.randint(0,len(a)-1)
        b.append(a[c])
    print(b)
    d = ''
    for i in b:
        d += i
    print(d)
    return d

def test1():
    with open('1.txt','r') as f:
        cookie_str = f.readlines() 
    print(cookie_str[0])
    return cookie_str[0]    

def test():
    submit = get_data()[0]
    print(submit)
    print(type(submit))
    submit['Mission_Id'] = 11002
    submit['Country'] = 'US'
    chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
    web_submit(submit,chrome_driver)

def get_data():
    path = r'..\res\Dadao.xlsx' 
    sheet,workbook = Dadao.get_excel(path)   
    Mission_Id = 11001 
    submit = Dadao.get_one_data(sheet,Mission_Id)
    submit['Mission_Id'] = Mission_Id
    return submit,path,workbook    

if __name__=='__main__':
    submit,_,_ =get_data()
    print(submit)
