from selenium import webdriver
import datetime
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
from selenium.webdriver.common.action_chains import ActionChains #导入ActionChains模块
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
    if debug == 1:
        site = 'https://www.dovehill7.com/ee96ee6f97b54564c6659d01ec8b27946ed6c928-0-0-0/'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()    
    chrome_driver.refresh()
    sleep(3)
    # page1
    # how much
    handle = chrome_driver.current_window_handle    
    a = ['300','500','700','1000']
    num_ = random.randint(0,3)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="loanAmount"]'))
    s1.select_by_value(a[num_])
    # email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Uspd']['email'])
    # zipcode
    chrome_driver.find_element_by_xpath('//*[@id="zip"]').send_keys(submit['Uspd']['zip'])
    # checkbox
    chrome_driver.find_element_by_xpath('//*[@id="terms-check"]').click()      
    # get started
    chrome_driver.find_element_by_xpath('//*[@id="header"]/div/div/form/div[5]/button').click()      
    sleep(10)
    for i in range(40):
        handles=chrome_driver.window_handles
        if len(handles) != 1:
            break
        else:
            sleep(2)
    for i in handles:
        if i != handle:
            chrome_driver.switch_to.window(i)
            # first_name
            chrome_driver.find_element_by_xpath('//*[@id="firstName"]').send_keys(submit['Uspd']['first_name'])
            # last_name
            chrome_driver.find_element_by_xpath('//*[@id="lastName"]').send_keys(submit['Uspd']['last_name'])
            # address
            chrome_driver.find_element_by_xpath('//*[@id="address"]').send_keys(submit['Uspd']['address'])
            # date_of_birth
            date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])   
            # mm 
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="birth_date_month"]'))
            s1.select_by_value(date_of_birth[0])                      
            # dd
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="birth_date_day"]'))
            s1.select_by_value(date_of_birth[1])               

            # year
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="birth_date_year"]'))
            s1.select_by_value(date_of_birth[2])               
            # employer name
            chrome_driver.find_element_by_xpath('//*[@id="workCompanyName"]').send_keys(submit['Uspd']['employer'])

            # monthly Income
            a = ['6000','5000','4000','3000','4500','3500']
            num_ = random.randint(0,5)
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="incomeNetMonthly"]'))
            s1.select_by_value(a[num_])

            # income source
            chrome_driver.find_element_by_xpath('//*[@id="om_form_income_type_EMPLOYMENT"]').click()
            # activate Military
            chrome_driver.find_element_by_xpath('//*[@id="am_no"]').click()
            # Driver licence
            drivers_license = submit['Uspd']['drivers_license'].split('.')[0]
            chrome_driver.find_element_by_xpath('//*[@id="driversLicenseNumber"]').send_keys(drivers_license)
            # ssn
            chrome_driver.find_element_by_xpath('//*[@id="ssn"]').send_keys(submit['Uspd']['ssn'])
            # primary phone
            phone_primary = submit['Uspd']['home_phone'].split('.')[0]
            chrome_driver.find_element_by_xpath('//*[@id="homePhone"]').click()
            for key in phone_primary:
                chrome_driver.find_element_by_xpath('//*[@id="homePhone"]').send_keys(key)
            # employer phone                        
            phone_employer = submit['Uspd']['work_phone'].split('.')[0]
            chrome_driver.find_element_by_xpath('//*[@id="workPhone"]').click()
            for key in phone_employer:
                chrome_driver.find_element_by_xpath('//*[@id="workPhone"]').send_keys(key)
            # Banking Information
            # Pay Frequency
            num_ = random.randint(1,3)
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="incomePaymentFrequency"]'))
            s1.select_by_index(num_)                 
            # Next payday
            month = datetime.datetime.now().month
            payday = Submit_handle.get_next_payday()
            print(payday)
            chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate1"]').click()
            if len(str(month)) == 2:
                for key in str(month):
                    chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate1"]').send_keys(key)
            else:
                chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate1"]').send_keys('0'+str(month))        
            if len(str(payday[1])) == 1:
                chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate1"]').send_keys('0'+str(payday[1]))
            else:
                for key in str(payday[1]):
                    chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate1"]').send_keys(key)                            
            for key in str(payday[2]):
                chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate1"]').send_keys(key)
            if payday[1] == 15:
                day = 30
            else:
                if month == 12:
                    month = 1
                else:
                    month += 1
                day = 15
            chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate2"]').click()
            if len(str(month)) == 2:
                for key in str(month):
                    chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate2"]').send_keys(key)
            else:
                chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate2"]').send_keys('0'+str(month))        
            if len(str(payday[1])) == 1:
                chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate2"]').send_keys('0'+str(day))
            else:
                for key in str(day):
                    chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate2"]').send_keys(key)                            
            for key in str(payday[2]):
                chrome_driver.find_element_by_xpath('//*[@id="incomeNextDate2"]').send_keys(key)                
            # Direct Deposit
            chrome_driver.find_element_by_xpath('//*[@id="dd_yes"]').click()
            # Bank name
            s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="bankName"]'))
            try:
                s1.select_by_value(submit['Uspd']['bank_name'])                      
            except:
                s1.select_by_value('other')  
            # bank state 
            try:
                s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="bankState"]'))
                s1.select_by_value('other')
            except:
                pass
            # ABA
            aba_num = submit['Uspd']['routing_number'].split('.')[0]
            if len(aba_num) == 8:
                aba_num = '0'+aba_num
            print(aba_num)
            chrome_driver.find_element_by_xpath('//*[@id="bankAba"]').click()
            sleep(1)
            for key in aba_num:
                chrome_driver.find_element_by_xpath('//*[@id="bankAba"]').send_keys(key)
            # account number
            chrome_driver.find_element_by_xpath('//*[@id="bankAccountNumber"]').send_keys(submit['Uspd']['account_number'].split('.')[0])
            # Type of account
            chrome_driver.find_element_by_xpath('//*[@id="bat_yes"]').click()
            # checkbox1
            chrome_driver.find_element_by_xpath('//*[@id="haveRead"]').click()
            # checkbox2
            chrome_driver.find_element_by_xpath('//*[@id="consentEmailSms"]').click()
            # submit
            chrome_driver.find_element_by_xpath('//*[@id="button_status"]').click()
            sleep(300)
    return 1





def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10038']
    excel = 'Uspd'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    submit['Mission_Id'] = 10039
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
