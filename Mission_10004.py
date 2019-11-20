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
import State_Mapper



'''
Opinion_Outpost(Done)
'''


def web_submit(submit,chrome_driver,debug=0):
    # test
    if debug == 1:
        site = 'http://im.datingwithlili.com/im/click.php?c=37&key=ke4vt3yj5mu5i073gefwk9cv'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    # sleep(1000)
    if submit['Auto']['gender'] == 'Female':
        # women
        chrome_driver.find_element_by_xpath('//*[@id="female"]').click()
    else:
        # man
        chrome_driver.find_element_by_xpath('//*[@id="male"]').click()

    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="firstname"]').send_keys(submit['Auto']['firstname'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="lastname"]').send_keys(submit['Auto']['lastname'])
    # email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Email']['Email_emu'])
    # corfirm email
    chrome_driver.find_element_by_xpath('//*[@id="confirmemail"]').send_keys(submit['Email']['Email_emu'])
    # choose
    chrome_driver.find_element_by_xpath('//*[@id="checkbox"]').click()
    sleep(2)
    # button
    element = selenium_funcs.scroll_and_find(chrome_driver,'//*[@id="registerBtn"]')
    sleep(2)
    element.click()
    db.update_plan_status(1,submit['ID'])    

    sleep(5)
    site = ''
    flag = 0
    handle = chrome_driver.current_window_handle
    try:            
        site = email_confirm(submit)  
        print(site)      
    except Exception as e:
        print(str(e))
        pass
        # writelog('email check failed',str(e))
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
            birthday = Submit_handle.get_auto_birthday(submit['Auto']['dateofbirth'])
            # mm
            chrome_driver.find_element_by_xpath('//*[@id="siq-monthdob-id"]').click()
            sleep(1)
            chrome_driver.find_element_by_xpath('//*[@id="siq-monthdob-id"]').send_keys(birthday[0])
            # dd
            chrome_driver.find_element_by_xpath('//*[@id="siq-daydob-id"]').click()
            sleep(1)
            chrome_driver.find_element_by_xpath('//*[@id="siq-daydob-id"]').send_keys(birthday[1])
            # yy
            chrome_driver.find_element_by_xpath('//*[@id="siq-yeardob-id"]').click()
            sleep(1)
            chrome_driver.find_element_by_xpath('//*[@id="siq-yeardob-id"]').send_keys(birthday[2])
            sleep(2)
            # # country
            # chrome_driver.find_element_by_xpath()
            # # language
            # chrome_driver.find_element_by_xpath()
            # # selector
            chrome_driver.find_element_by_xpath('//*[@id="siq-agreetermscond-id-1"]').click()
            sleep(2)
            # button
            chrome_driver.find_element_by_xpath('//*[@id="sip-confirm"]').click()
            sleep(2)
            # page2
            # race
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="siq-raceUS-id"]'))
            s1.select_by_value(str(1))  # 选择value="o2"的项   
            # ethnicity
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="siq-ethnicityUS-id"]'))
            s1.select_by_value(str(2))  # 选择value="o2"的项              
            # income
            num_income = random.randint(2,9)
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="siq-incomeNova-id"]'))
            s1.select_by_index(num_income)  # 选择value="o2"的项               
            # home address_1_state
            element = chrome_driver.find_element_by_xpath('//*[@id="siq-addressline1-id"]')
            selenium_funcs.clear_deep(element)
            sleep(1)
            element.send_keys(submit['Auto']['address'])
            # city
            element = chrome_driver.find_element_by_xpath('//*[@id="siq-city-id"]')
            selenium_funcs.clear_deep(element)
            element.send_keys(submit['Auto']['city'])
            sleep(1)            
            # zip code
            element = chrome_driver.find_element_by_xpath('//*[@id="siq-postalcodeNoCheck-id"]')
            zipcode = submit['Auto']['zip'].split('.')[0]
            selenium_funcs.clear_deep(element)
            sleep(1)            
            for key in zipcode:
                element.send_keys(int(key))
            # state
            # //*[@id="siq-state-id"]
            state = State_Mapper.Mapping_state()
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="siq-state-id"]'))
            s1.select_by_visible_text(state[submit['Auto']['state']])  # 选择value="o2"的项             
            # next
            sleep(3)
            chrome_driver.find_element_by_xpath('//*[@id="sip-confirm"]').click()
            sleep(30)
            pwd = Submit_handle.password_get()
            chrome_driver.find_element_by_xpath('//*[@id="siq-password-id"]').send_keys(pwd)
            sleep(1)
            chrome_driver.find_element_by_xpath('//*[@id="siq-confirmpassword-id"]').send_keys(pwd)
            sleep(1)
            chrome_driver.find_element_by_xpath('//*[@id="sip-confirm"]').click()
            sleep(15)
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
            title = 'Activate Membership to Start Earning Rewards'
            pattern = r'.*?(https://opinionoutpost.com/Membership/Intake\?signuptoken=.*?\&resp=([0-9]{5,15}))'
            url_link = emaillink.get_email(name,pwd,title,pattern)
            print(url_link)
            if url_link != '':
                break
        except Exception as e:
            print(str(e))
            print('===')
            pass
    return url_link





def test():
    Mission_list = ['10004']
    Excel_name = ['Auto','Email']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # print(submit)
    # state = State_Mapper.Mapping_state()
    # print(state)
    # date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])
    # print(date_of_birth)
    web_submit(submit,1)
    # print(submit['Uspd'])
    # print(submit['Uspd']['state'])
    # print(submit['Uspd']['city'])
    # print(submit['Uspd']['zip'])
    # print(submit['Uspd']['date_of_birth'])
    # print(submit['Uspd']['ssn'])

 

def test1():
    num_gender = random.randint(0,1)
    print(num_gender)

if __name__=='__main__':
    test()
