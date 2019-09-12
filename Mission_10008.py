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


'''
CashRequestOnline(Done)
'''



def web_submit(submit,chrome_driver,debug=0):
    # test
    if debug == 1:
        site = 'https://cashrequestonline.com/?cguid=8bdbc50e-ddcd-42af-a291-e6aa4508c989'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    # sleep(2000)
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    # sleep(1000)

    # page1
    # selector
    handle = chrome_driver.current_window_handle
    num_rent = random.randint(5,12)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="RequestedAmount"]'))
    s1.select_by_index(num_rent)  
    # input
    chrome_driver.find_element_by_xpath('//*[@id="ZipCode"]').click()    
    chrome_driver.find_element_by_xpath('//*[@id="ZipCode"]').send_keys((submit['Uspd']['zip'].split('.'))[0])
    # button
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="ApplyNow"]/a').click()
    
    # page2
    handles=chrome_driver.window_handles   
    for i in handles:
        if i != handle:
            chrome_driver.switch_to.window(i)
    # input email
    element = chrome_driver.find_element_by_xpath('//*[@id="Email"]')
    element.click()
    element.send_keys(submit['Email']['Email_emu'])
    # button
    sleep(2)
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[2]/div[2]/div/div/a').click()

    # page3
    # selector1
    # '/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[3]/div[1]/div/div/div[1]/label/span'
    # '/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[3]/div[1]/div/div/div[2]/label/span'
    # '/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[3]/div[1]/div/div/div[3]/label/span'
    if num_rent <= 10:
        num_rent_2 = 2
    elif num_rent == 11:
        num_rent_2 = 3
    else:
        num_rent_2 = 4
    xpath = '/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[3]/div[1]/div/div/div['+str(num_rent_2)+']/label/span'
    chrome_driver.find_element_by_xpath(xpath).click()
    sleep(2)
    # page4
    # firstname
    element = chrome_driver.find_element_by_xpath('//*[@id="FirstName"]')
    element.click()
    element.send_keys(submit['Uspd']['first_name'])
    # lastname
    element = chrome_driver.find_element_by_xpath('//*[@id="LastName"]')
    element.click()
    element.send_keys(submit['Uspd']['last_name'])    
    
    # button
    sleep(2)
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[4]/div[3]/div/div[2]/a').click()
    sleep(2)
    # page5
    # input phone
    element = chrome_driver.find_element_by_xpath('//*[@id="PhoneHome"]')
    element.click()
    element.send_keys((submit['Uspd']['home_phone'].split('.'))[0])
    # button
    sleep(2)
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[5]/div[2]/div/div[2]/a').click()
    # page6
    element = chrome_driver.find_element_by_xpath('//*[@id="Address1"]')
    element.click()
    element.send_keys(submit['Uspd']['address'])
    # button
    sleep(2)
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[6]/div[4]/div/div[2]/a').click()
    sleep(2)
    # page7
    # selector1    
    num_year = random.randint(1,4)
    xpath = '/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[7]/div[1]/div/div/div['+str(num_year)+']/label/span'
    chrome_driver.find_element_by_xpath(xpath).click()
    sleep(2)
    # page8
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[8]/div[1]/div/div/div[1]/label/span').click()
    sleep(2)
    # page9
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[9]/div[1]/div/div/div[1]/label/span').click()
    sleep(2)
    # page10
    birthday = submit['Uspd']['date_of_birth']
    month = birthday[0]
    year = birthday[2]
    day = birthday[1]
    # year
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="dp1563772774984"]/div/div/div/select[2]'))
    s1.select_by_value(year)  
    sleep(1)
    # month
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="dp1563772774984"]/div/div/div/select[1]'))
    s1.select_by_value(str(int(month)-1))  
    sleep(2)
    # day
    chrome_driver.find_element_by_link_text(str(day)).click()
    # button
    try:
        chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[10]/div[2]/div/div[2]/a').click()
    except:
        pass
    # page11
    # drivers_license
    element = chrome_driver.find_element_by_xpath('//*[@id="DriversLicense"]')
    element.click()
    element.send_keys(submit['Uspd']['drivers_license'])
    sleep(2)
    # button
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[11]/div[3]/div/div[2]/a').click()
    sleep(2)
    # page12
    # selector1
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[12]/div[1]/div/div/div[1]/label/span').click()
    # page13
    num_income = random.randint(1,5)
    xpath = '/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[13]/div[1]/div/div/div['+str(num_income)+']/label/span'
    chrome_driver.find_element_by_xpath(xpath).click()
    # page14
    # employer
    element = chrome_driver.find_element_by_xpath('//*[@id="EmployerName"]')
    element.click()
    element.send_keys(submit['Uspd']['employer'])
    # button
    sleep(2)
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[14]/div[2]/div/div[2]/a').click()
    # page15
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[15]/div[1]/div/div/div[1]/label/span').click()
    sleep(2)
    # employer phone
    element = chrome_driver.find_element_by_xpath()
    element.click()
    element.send_keys(submit['Uspd']['work_phone'])
    # button
    sleep(2)
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[16]/div[2]/div/div[2]/a').click()
    sleep(2)
    # page16
    # selector1
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[17]/div[1]/div/div/div[2]/label/span').click()
    # page17
    sleep(2)
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[18]/div[1]/div/div/div[3]/label/span').click()
    sleep(2)
    # page18
    chrome_driver.find_element_by_link_text('30').click()
    sleep(2)
    # page 19
    # input1
    element = chrome_driver.find_element_by_xpath('//*[@id="BankABA"]')
    element.click()
    element.send_keys((submit['Uspd']['routing_number'].split('.'))[0])
    sleep(2)
    # input2
    element = chrome_driver.find_element_by_xpath('//*[@id="BankAccountNumber"]')
    element.click()
    element.send_keys((submit['Uspd']['account_number'].split('.'))[0])
    # button
    sleep(2)
    element = chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[20]/div[4]/div/div[2]/a')
    sleep(2)
    # page20
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[21]/div[1]/div/div/div[1]/label/span').click()
    sleep(2)
    # page21
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[22]/div[1]/div/div/div[1]/label/span').click()
    sleep(2)
    # page22
    element = chrome_driver.find_element_by_xpath('//*[@id="SSN1"]')
    element.click()
    element.send_keys((submit['Uspd']['ssn'].split('.'))[0])
    sleep(2)
    chrome_driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[23]/div[3]/div[2]/a').click()    
    print('Sleeping 60 seconds')
    sleep(60)
    chrome_driver.close()
    chrome_driver.quit()
    return






 

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
            if url_link != '':
                break
        except Exception as e:
            print(str(e))
            print('===')
            pass
    return url_link





def test_2():
    Country ='US'
    Mission_list = ['10004']
    Email_list = ['hotmail','aol.com','yahoo.com','outlook.com']
    Excel_names = ['Auto','Usloan']
    dateofbirth_list = []
    for i in range(30):
        submit = db.read_one_info(Country,Mission_list,Email_list,Excel_names)
        # print(submit['Auto']['dateofbirth'])    
        dateofbirth_list.append(submit['Auto']['dateofbirth'])
    print('=================')
    print(dateofbirth_list)
    dateofbirth_list = ['9/19/1989', '9/19/1989', '9/19/1989', '6/25/1952', '12/21/1962', '3/18/1948', '11/13/1985', '6/25/1952', '11-01-1978', '10-07-1957', '11/13/1985', '10-07-1957', '10-02-1962', '12/21/1971', '3/13/1981', '11/13/1985', '12/21/1962', '09-01-1952', '10-07-1957', '12/21/1971', '9/19/1989', '7/19/1948', '5/31/1985', '09-01-1952', '11-11-1947', '3/13/1981', '3/18/1948', '12-08-1969', '01-05-1985', '9/19/1989']
    for date in dateofbirth_list:
        if '/' in date:
            birthday = date.split('/')
        elif '-' in date:
            birthday = date.split('-')
        print(birthday)




if __name__=='__main__':    
    submit = db.get_one_info()
    web_submit(submit)
