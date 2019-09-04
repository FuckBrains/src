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

'''
test copyfile
Royal Cams(Done)
US
Email
'''

# test lead ai gaoshi



def web_submit(submit):
    # test
    # site = 'https://finaff.go2affise.com/click?pid=3464&offer_id=9436'
    # submit['Site'] = site
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    # print(10000)
    # print('=========')
    name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    # sleep(2)
    # try:
    #     chrome_driver.find_element_by_xpath('//*[@id="layout_9"]/div[11]/div/a').click()
    # except:
    #     pass
    chrome_driver.find_element_by_xpath('//*[@id="header_login"]/a[2]').click()
    sleep(2)
    try:
        chrome_driver.find_element_by_xpath('//*[@id="member_join_popup"]/div[3]/div/button').click()
        sleep(2)        
        chrome_driver.find_element_by_xpath('//*[@id="user_member_username"]').send_keys(name)
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="member_join_popup"]/div[3]/div/button').click()
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="user_member_password"]').send_keys(submit['Email']['Email_emu_pwd'])
        chrome_driver.find_element_by_xpath('//*[@id="user_member_terms_of_use"]').click()
        chrome_driver.find_element_by_xpath('//*[@id="member_join_popup"]/div[3]/div/form/div/div[2]/button').click()
        sleep(2)
    except:
        chrome_driver.find_element_by_xpath('//*[@id="user_member_username"]').send_keys(name)
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="user_member_password"]').send_keys(submit['Email']['Email_emu_pwd'])
        sleep(2)
        chrome_driver.find_element_by_xpath('//*[@id="user_member_terms_of_use"]').click()
        sleep(2)
        try:
            chrome_driver.find_element_by_xpath('//*[@id="member_join_popup"]/div[1]/form/div/div[2]/button').click()
        except:
            pass
        try:
            chrome_driver.find_element_by_xpath('//*[@id="member_join_popup"]/table/tbody/tr/td/div[1]/form/div/div[2]/button').click()
        except:
            pass    
        try:
            chrome_driver.find_element_by_xpath('//*[@id="member_join_popup"]/div[2]/form/div/div[2]/button ').click()
        except:
            pass             
               
        sleep(2)
    t = 0
    while True:
        if t >= 3:
            break
        try:
            chrome_driver.find_element_by_xpath('//*[@id="layout_9"]/div[18]/div/div/div/div/div/div[2]/a').click()
            break
        except Exception as e:
            sleep(30)
            t += 1
            pass
    chrome_driver.refresh()
    chrome_driver.find_element_by_xpath('//*[@id="user_email"]').send_keys(submit['Email']['Email_emu'])
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="add_confirm_email"]/div/div[2]/button').click()

    # sleep(2000)
    # 'register success and begin confirm email'
    site = ''
    flag = 0
    handle = chrome_driver.current_window_handle
    try:            
        site = email_confirm(submit['Email'])  
        print(site)      
    except Exception as e:
        writelog('email check failed',str(e))
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
    site = ''
    for i in range(20):
        msg_content = imap.email_getlink(submit,'From: Royalcams')
        # print(len(msg_content))
        if 'From: Royalcams' not in msg_content :
            print('Target Email Not Found !')
            sleep(15)
        else:
            # print(msg_content)
            a = msg_content.find('https://royalcams.com/members/confirm-email/')
            b = msg_content.find('"',a)
            site = msg_content[a:b]
            # # print(msg_content[a+32:b])
            # site = msg_content[a+35:b-50].replace('\r','').replace('\n','')
            # print(len(site))
            # site += "=" * ((4 - len(site) % 4) % 4)
            # # print(site)
            # site = base64.b64decode(site)

            # site = str(site)
            # c = site.find('https://www.scharferchat.com/activate/')
            # d = site.find('\\r',c)
            # site = site[c:d]
            return site            
    return site



def Landing_page(chrome_driver):
    # page1:https://trk.securesmrt-dt.com/c/1fbbec7f1742a68d?click_id=08f5cffc5eb14dec8a12d038c9ed2fb8db81&aff_id=87788&aff_sub=6708
    if '' in chrome_driver.page_source:
        chrome_driver.find_element_by_xpath('document.querySelector("#text03")').click()
        sleep(10)
        chrome_driver.find_element_by_xpath('//*[@id="text07"]').click()
        sleep(3)
        chrome_driver.find_element_by_xpath('//*[@id="text48"]').click()
        sleep(3)
        chrome_driver.find_element_by_xpath('//*[@id="text09"]').click()
        sleep(3)
        chrome_driver.find_element_by_xpath('//*[@id="text12"]').click()
        sleep(3)
        chrome_driver.find_element_by_xpath('//*[@id="text15"]').click()
        sleep(3)
        chrome_driver.find_element_by_xpath('//*[@id="text46"]').click()
        sleep(5)
    elif 'THESE WOMEN ARE ONLY LOOKING FOR CASUAL SEXUAL ENCOUNTERS' in chrome_driver.page_source:
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[2]/a[2]').click()
        sleep(3)
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/a[2]').click()
        sleep(3)
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/a[2]').click()
        sleep(3)
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[2]/a').click()
        sleep(5)


    return chrome_driver




if __name__=='__main__':
    Mission_list=['10001']
    Email_list =['aol.com']
    Excel_names = ['Auto']
    data = db.read_one_excel(Mission_list,Email_list,Excel_names)
    print(data)
    print(len(data))