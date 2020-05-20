import Dadao
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
import google
'''
'''


def web_submit(submit,chrome_driver,debug=0):  
    # test
    if debug == 1:
        site = 'https://elements.envato.com/sign-up'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    sleep(1)
    id_google = google.get_id()    
    # page1
    # join
    # chrome_driver.find_element_by_xpath('//*[@id="signUpFirstName"]').click()
    # sleep(1)    
    # alert
    # dig_alert = chrome_driver.switch_to.alert
    # sleep(1)
    # print(dig_alert.text)
    # dig_alert.accept()
    # sleep(5)    

    # page1
    # chrome_driver.switch_to_frame('frame')
    # firstname
    firstname = submit['Dadao']['firstname'] 
    chrome_driver.find_element_by_xpath('//*[@id="signUpFirstName"]').send_keys(firstname)
    sleep(1)
    # lastname
    lastname = submit['Dadao']['lastname']     
    chrome_driver.find_element_by_xpath('//*[@id="signUpLastName"]').send_keys(lastname)
    sleep(1)
    email = submit['Dadao']['email'] 
    chrome_driver.find_element_by_xpath('//*[@id="signUpEmail"]').send_keys(email)
    sleep(2)
    # username
    name = Submit_handle.get_fullname(submit['Dadao'])
    chrome_driver.find_element_by_xpath('//*[@id="signUpUsername"]').send_keys(name)
    sleep(1)
    # pwd
    pwd = Submit_handle.password_get_Nostale()    
    chrome_driver.find_element_by_xpath('//*[@id="signUpPassword"]').send_keys(pwd)
    sleep(1)   
    # recaptcha
    js = google.get_js(id_google)
    chrome_driver.execute_script(js)
    # click
    # js_submit = 'document.getElementsByTagName("button")[1].click();'
    # chrome_driver.execute_script(js)  
    print('js_submit click finished')  
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div[1]/main/div/div/div[2]/div/div/div/form/button').click()
    # sleep(5)    
    sleep(3000)
    return




    # # page3
    # elem = '//*[@id="first_name"]'
    # # firstname
    # firstname = submit['Dadao']['firstname']
    # chrome_driver.find_element_by_xpath(elem).send_keys(firstname)
    # # lastname
    # elem = '//*[@id="last_name"]'
    # lastname = submit['Dadao']['lastname']    
    # chrome_driver.find_element_by_xpath(elem).send_keys(lastname)
    # sleep(1)
    # # zip
    # elem = '//*[@id="zip"]'
    # submit['Dadao']['katou'] = submit['Dadao']['katou'].replace('\t','')
    # zip_ = Submit_handle.get_zip(submit['Dadao'])
    # chrome_driver.find_element_by_xpath(elem).send_keys(zip_)
    # sleep(1)
    # # card_number
    # elem = '//*[@id="cc"]'
    # card_number = submit['Dadao']['card_number'].replace('\t','')    
    # chrome_driver.find_element_by_xpath(elem).send_keys(card_number)
    # # mm
    # elem = '//*[@id="expMonth"]'
    # month = str(submit['Dadao']['month']).replace('\t','')
    # if len(month) == 1:
    #     month = '0'+month
    # month = month.replace(' ','')     
    # s1 = Select(chrome_driver.find_element_by_xpath(elem))
    # s1.select_by_value(month)
    # sleep(1)
    # # year
    # elem = '//*[@id="expYear"]'
    # year = str(submit['Dadao']['year'])
    # year = year.replace('\t','')
    # year = year.replace(' ','')      
    # if len(year) == 4:
    #     year = year[2:]      
    # s1 = Select(chrome_driver.find_element_by_xpath(elem))
    # s1.select_by_value(year)    
    # # cvv    
    # elem = '//*[@id="cvv"]'
    # cvv = submit['Dadao']['cvv'].replace('\t','')
    # if len(cvv) == 2:
    #     cvv = '0'+str(cvv)    
    # chrome_driver.find_element_by_xpath(elem).send_keys(cvv)
    # sleep(2)
    # # button
    # chrome_driver.find_element_by_xpath('//*[@id="signUp"]').click()
    # db.update_plan_status(1,submit['ID']) 
    # sleep(30)
    # return

 
def test():
    submit = {}
    # path = r'..\res\Dadao.xlsx'
    # sheet,workbook = Dadao.get_excel(path)   
    # Mission_Id = 11005
    # submit['Dadao'] = Dadao.get_one_data(sheet,Mission_Id)
    # print(submit)
    submit['Dadao'] = {}
    submit['Dadao']['Mission_Id'] = 11005
    submit['Dadao']['firstname'] = 'jonas' 
    submit['Dadao']['lastname'] = 'masha' 
    submit['Dadao']['email'] = 'jonasmasha11@gmail.com' 

    # submit['Dadao']['path'] = path
    # submit['Dadao']['workbook'] = workbook 
    chrome_driver = Chrome_driver.get_chrome(submit['Dadao'],pic=1)
    web_submit(submit,chrome_driver,debug=1)



if __name__=='__main__':
    test()