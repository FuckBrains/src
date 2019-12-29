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
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

'''
'''


def web_submit(submit,chrome_driver,debug=0):  
    # test
    if debug == 1:
        site = 'http://nc.fclitloan.com/click.php?c=9&key=mqrrjq7g3e8ayad39m7if251'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    sleep(1)
    # page1
    # join
    chrome_driver.find_element_by_xpath('//*[@id="join-button"]/a').click()
    sleep(1)    
    # alert
    dig_alert = chrome_driver.switch_to.alert
    sleep(1)
    print(dig_alert.text)
    dig_alert.accept()
    sleep(5)    

    # page2
    chrome_driver.switch_to_frame('frame')
    name = Submit_handle.get_name_real()
    chrome_driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)
    sleep(1)
    pwd = Submit_handle.password_get_Nostale()    
    chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(pwd)
    sleep(1)   
    email = submit['Dadao']['email'] 
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(email)
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="nextBtn"]').click()
    sleep(5)
    # page3
    elem = '//*[@id="first_name"]'
    # firstname
    firstname = submit['Dadao']['firstname']
    chrome_driver.find_element_by_xpath(elem).send_keys(firstname)
    # lastname
    elem = '//*[@id="last_name"]'
    lastname = submit['Dadao']['lastname']    
    chrome_driver.find_element_by_xpath(elem).send_keys(lastname)
    sleep(1)
    # zip
    elem = '//*[@id="zip"]'
    zip_ = submit['Dadao']['katou'].replace('\t','')
    zip_ = Submit_handle.get_zip(zip_)
    chrome_driver.find_element_by_xpath(elem).send_keys(zip_)
    sleep(1)
    # card_number
    elem = '//*[@id="cc"]'
    card_number = submit['Dadao']['card_number'].replace('\t','')    
    chrome_driver.find_element_by_xpath(elem).send_keys(card_number)
    # mm
    elem = '//*[@id="expMonth"]'
    month = str(submit['Dadao']['month']).replace('\t','')
    if len(month) == 1:
        month = '0'+month
    month = month.replace(' ','')     
    s1 = Select(chrome_driver.find_element_by_xpath(elem))
    s1.select_by_value(month)
    sleep(1)
    # year
    elem = '//*[@id="expYear"]'
    year = str(submit['Dadao']['year'])
    year = year.replace('\t','')
    year = year.replace(' ','')      
    if len(year) == 4:
        year = year[2:]      
    s1 = Select(chrome_driver.find_element_by_xpath(elem))
    s1.select_by_value(year)    
    # cvv    
    elem = '//*[@id="cvv"]'
    cvv = submit['Dadao']['cvv'].replace('\t','')
    if len(cvv) == 2:
        cvv = '0'+str(cvv)    
    chrome_driver.find_element_by_xpath(elem).send_keys(cvv)
    sleep(2)
    # button
    chrome_driver.find_element_by_xpath('//*[@id="signUp"]').click()
    db.update_plan_status(1,submit['ID']) 
    sleep(30)
    return








    name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    print('Loading finished')
    # username
    name_ = submit['email'].split('@')[0]
    if '.' in name_:
        name_ = name_.split('.')[0]
    if ' ' in name_:
        name_ = name_.split(' ')[0]
    if '-' in name_:
        name_ = name_.split('-')[0]
    if '_' in name_:
        name_ = name_.split('_')[0]        
    name = name_+str(random.randint(10,1000))
    if len(name)>=16:
        num_rand = random.randint(8,14)
        name = name[:num_rand]
    chrome_driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)

    # password
    pwd = Submit_handle.get_pwd_real2()
    if '-' in pwd:
        pwd = pwd.split('-')[0]
    if '_' in pwd:
        pwd = pwd.split('_')[0]           
    chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(pwd)
    # email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['email'])
    submit['status'] = 'email uploaded'

    # next
    chrome_driver.find_element_by_xpath('//*[@id="nextBtn"]').click()
    WebDriverWait(chrome_driver,20).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="J2"]/div/div/div[1]/div[1]'),"Get Verified. It's Free!"))

    # page2
    # Name on Card
    fullname = submit['firstname'] + ' ' + submit['lastname']
    if len(fullname) >= 16:
        fullname = fullname[0:15]
    if '-' in fullname:
        fullname = fullname.split('-')[0]
    if '_' in fullname:
        fullname = fullname.split('_')[0]         
    chrome_driver.find_element_by_xpath('//*[@id="fullname"]').send_keys(fullname)   
    # card number
    card_number = submit['card_number'].replace('\t','')
    chrome_driver.find_element_by_xpath('//*[@id="cc"]').send_keys(card_number)
    # month
    elem = '//*[@id="expMonth"]'
    month = str(submit['month']).replace('\t','')
    if len(month) == 1:
        month = '0'+month
    month = month.replace(' ','')    
    s1 = Select(chrome_driver.find_element_by_xpath(elem))
    s1.select_by_value(month)
    # year
    elem = '//*[@id="expYear"]'
    year = str(submit['year'])
    year = year.replace('\t','')
    year = year.replace(' ','')      
    if len(year) == 4:
        year = year[2:]  
    s1 = Select(chrome_driver.find_element_by_xpath(elem))
    s1.select_by_value(year)   
    # cvv    
    cvv = submit['cvv'].replace('\t','')
    chrome_driver.find_element_by_xpath('//*[@id="cvv"]').send_keys(cvv)    
    # zip    
    zipcode = submit['katou'].replace('\t','')
    chrome_driver.find_element_by_xpath('//*[@id="zip"]').send_keys(zipcode)
    # submit
    try:
        chrome_driver.find_element_by_xpath('//*[@id="signUp"]').click()
        sleep(30)
    except:
        pass
    submit['status'] = 'cvv uploaded'
    return submit
    # fail_xpath = '/html/body/div[1]/div[2]/section/div/div[2]/div[2]/div/div/div/p'
    # fail_text = 'Seems like something went wrong. Please try again, or contact customer service 888-548-7893.'
    # success_xpath = '//*[@id="colText"]/div/div[1]/div/h2'
    # success_text = 'Welcome to HookupHereNow!'
    # fail_xpath2 = '//*[@id="J2"]/div/div/div[1]/div[2]/div[2]/form/div[1]/span'
    # fail_text2 = 'The card used to verify has been declined. Please confirm info, or use a new card to verify.'
    # submit['password'] = pwd
    # submit['fullname'] = fullname
    # xpaths = [fail_xpath,fail_xpath2,success_xpath]
    # texts = [fail_text,fail_text2,success_text]
    # flags = dict(zip(xpaths,texts))
    # flag_return = 0
    # for text in texts:
    #     if text in chrome_driver.page_source:
    #         submit['status'] = text
    #         if text == success_text:
    #             chrome_driver.find_element_by_xpath('//*[@id="nextBtn"]').click()
    #             sleep(15)
            # flag_return = 1
    # if flag_return != 1 :
    #     submit['status'] = 0
    # for xpath_ in xpaths:
    #     try:
    #         if EC.text_to_be_present_in_element((By.XPATH,xpath_),flags[xpath_])(chrome_driver):
    #             if xpath_ == success_xpath:
    #                 submit['status'] = 'success'
    #                 chrome_driver.find_element_by_xpath('//*[@id="nextBtn"]').click()
    #                 sleep(15)
    #             else:
    #                 submit['status'] = flags[xpath_]
    #             break
    #     except:
    #         pass

 
def test():
    year = '\t2022\t '
    year = str(year)
    year = year.replace('\t','')
    year = year.replace(' ','')      
    if len(year) == 4:
        year = year[2:]    
    print(year)  


if __name__=='__main__':
    test()