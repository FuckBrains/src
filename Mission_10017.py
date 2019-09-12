'''
Flirt
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
import emaillink



def web_submit(submit,chrome_driver,debug=0):
    # test
    # Excel_10054 = 'Data2000'
    # Excel_10054 = 'Uspd'    
    if debug == 1:
        site = 'http://zh.moneymethods.net/click.php?c=11&key=75uwb87m43ef55qo3ytehrd1'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()
    chrome_driver.refresh()      
    sleep(5)
    chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[1]/div/div/div/div[1]/label').click()
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[2]/div/div[2]/button[1]').click()
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[3]/div/div[1]/div/div[1]/label').click()
    sleep(2)
    num_eye = random.randint(0,3)
    if num_eye == 0:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[4]/div/div[1]/button[1]').click()
    elif num_eye == 1:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[4]/div/div[1]/button[2]').click()
    elif num_eye == 2:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[4]/div/div[1]/button[3]').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[4]/div/div[1]/button[4]').click()
    sleep(2)
    num_hare = random.randint(0,3)
    if num_hare == 0:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[5]/div/div[1]/button[1]').click()
    elif num_hare == 1:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[5]/div/div[1]/button[2]').click()
    elif num_hare == 2:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[5]/div/div[1]/button[3]').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[5]/div/div[1]/button[4]').click()
    sleep(2)
    index = random.randint(0,4)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[6]/div/div[1]/div/select'))
    s1.select_by_index(index)    
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[6]/div/div[2]/button[1]').click()
    sleep(2)
    num_noob = random.randint(0,3)
    if num_noob == 0:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[7]/div/div[1]/button[1]').click()
    elif num_noob == 1:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[7]/div/div[1]/button[2]').click()
    elif num_noob == 2:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[7]/div/div[1]/button[3]').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[7]/div/div[1]/button[4]').click()
    sleep(2)    
    num_ass = random.randint(0,3)
    if num_ass == 0:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[8]/div/div[1]/button[1]').click()
    elif num_ass == 1:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[8]/div/div[1]/button[2]').click()
    elif num_ass == 2:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[8]/div/div[1]/button[3]').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[8]/div/div[1]/button[4]').click()
    sleep(10) 
    chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[10]/div/div/button').click()  
    sleep(5)
    name = name_get.gen_one_word_digit(lowercase=False)  
    pwd = Submit_handle.password_get()    
    try:
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[11]/div/div[2]/button').click()   
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)
        sleep(1)
        chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(pwd)
        sleep(1)
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[12]/div/div[4]/button[1]').click()
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Email']['Email_emu'])
        sleep(1)
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[13]/div/div[2]/button[1]').click()
        sleep(10)
    except:
        if chrome_driver.find_element_by_xpath('//*[@id="username"]'):
            print('==============')
            print('==============')            
        chrome_driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)
        sleep(1)
        chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(pwd)
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Email']['Email_emu'])
        sleep(1)
        chrome_driver.find_element_by_xpath('//*[@id="regform"]/div[1]/div[11]/div/div[6]/button').click()
        sleep(10)  
    sleep(20)          
    site = ''
    handle = chrome_driver.current_window_handle
    try:            
        site = email_confirm(submit)  
        print(site)      
    except Exception as e:
        print('email check failed',str(e))
    if site != '':
        newwindow='window.open("' + site + '");'
        chrome_driver.execute_script(newwindow)
        sleep(30)        
    else:
        chrome_driver.close()
        chrome_driver.quit()
        return         
    handles=chrome_driver.window_handles   
    sleep(10)
    try:
        for i in handles:
            if i != handle:
                chrome_driver.switch_to.window(i)
                try:
                    chrome_driver.refresh()
                    sleep(20)
                    try:
                        chrome_driver.find_element_by_xpath('//*[@id="mainContainer"]/div/section/ul[1]/li[3]/div/a').click()
                    except:
                        pass
                except:
                    pass                        
    except:
        pass
    return 1




def email_confirm(submit):
    print('----------')
    for i in range(5):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']
            title = ('service@ga.mydates.com','')
            # 'https://mydates.com?code=0df6c9c9-12ba-46a6-8282-7b6a4c9f2103&trk=5fzb3wd'
            pattern = r'.*?(https://mydates.com\?code=[0-9a-zA-Z]{1,10}-[0-9a-zA-Z]{1,10}-[0-9a-zA-Z]{1,10}-[0-9a-zA-Z]{1,10}-[0-9a-zA-Z]{1,20}&trk=[0-9a-zA-Z]{1,10})'
            # url_link = emaillink.get_email(name,pwd,title,pattern)
            # if 'http' in url_link :
            #     print(url_link)
            #     break
            # title = ('supportlivecam.com','')
            # pattern = r'.*?Confirm Your Email.*?(http://trk.email.supportlivecam.com/[0-9a-zA-Z]{1,30}/[0-9a-zA-Z]{1,1000})By clicking on the'
            url_link = emaillink.get_email(name,pwd,title,pattern,True)
            if 'http' in url_link :
                url_link = url_link.replace('?','/?').replace('&amp;','&')
                print(url_link)
                break            
        except Exception as e:
            print(str(e))
            print('===')
            pass
    return url_link


def web_confirm():
    url='https://mydates.com/?code=685bae42-d07c-400e-9eef-91b1627f94c1&trk=5g2959w'
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get(url)    
    try:
        chrome_driver.find_element_by_xpath('//*[@id="mainContainer"]/div/section/ul[1]/li[3]/div/a').click()
    except:    
        pass
    sleep(300)



def test():
    # db.email_test()
    Mission_list = ['10009']
    Excel_name = ['','Email']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # db.read_all_info()
    # print(submit)
    # excel_list = []
    # for i in range(400):
    #     submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    #     # print(submit)
    #     excel_list.append(submit['Email']['Email_Id'])
    # # print(excel_list)
    # print(len(excel_list))
    # print(len(set(excel_list)))

    # date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])
    # print(date_of_birth)
    web_submit(submit,1)
    # print(submit['Uspd'])
    # print(submit['Uspd']['state'])
    # print(submit['Uspd']['city'])
    # print(submit['Uspd']['zip'])
    # print(submit['Uspd']['date_of_birth'])
    # print(submit['Uspd']['ssn'])

 

def email_test():
    
    submit = {'Email':{'Email_Id': '6f4ff393-aa34-11e9-a4ec-0003b7e49bfc', 'Email_emu': 'SummerCopelandk@aol.com', 'Email_emu_pwd': 'reo3xzpL', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': 'Good'}}
    email_confirm(submit)


if __name__=='__main__':
    web_confirm()
    print('......')