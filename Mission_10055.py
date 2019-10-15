'''
ad1
Zippyloan
https://axisempire022.afftrack.com/click?aid=260&linkid=T718&s1=&s2=&s3=&s4=&s5=
Uspd
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
from selenium.webdriver.common.keys import Keys
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
    # Excel_10054 = 'Data2000'
    Excel_10054 = 'Uspd'    
    if debug == 1:
        site = 'https://axisempire022.afftrack.com/click?aid=260&linkid=T718&s1=&s2=&s3=&s4=&s5='
        submit['Site'] = site
    try:
        chrome_driver.get(submit['Site'])
    except:
        pass
    chrome_driver.maximize_window() 
    chrome_driver.refresh()
    if 'Personal Loans' not in chrome_driver.page_source:
        print('page not found')
        chrome_driver.close()
        chrome_driver.quit()
        return 0
    # click
    # page1
    # Cash needed
    sleep(3)
    index_ = random.randint(1,3)
    js="$('#amount > option:nth-child(2)').removeAttr('selected')"
    chrome_driver.execute_script(js)
    js = '$("#amount > option:nth-child('+str(index_)+')").attr("selected","selected")'
    chrome_driver.execute_script(js)
    sleep(1)
    # s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="amount"]'))
    # s1.select_by_value('2000')    
    sleep(1)

    # monthly income
    index_income = random.randint(0,6)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="income"]'))
    s1.select_by_index(index_income)
    sleep(1)

    # credit type
    index = random.randint(1,2)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="creditscore"]'))
    s1.select_by_index(index)
    sleep(1)

    # purpose of loan        
    index = random.randint(1,11)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="loan_purpose"]'))
    s1.select_by_index(index)
    sleep(3)

    # click to turn to page2
    chrome_driver.find_element_by_xpath('//*[@id="lander_submit"]').click()
    sleep(3)
    # page2
    # firstname
    chrome_driver.find_element_by_xpath('//*[@id="fname"]').send_keys(submit['Uspd']['first_name'])
    # lastname
    chrome_driver.find_element_by_xpath('//*[@id="lname"]').send_keys(submit['Uspd']['last_name'])
    # birthday
    date_of_birth = Submit_handle.get_auto_birthday(submit['Uspd']['date_of_birth'])
    for key in date_of_birth[0]:
        chrome_driver.find_element_by_xpath('//*[@id="dob"]').send_keys(key)
    for key in date_of_birth[1]:
        chrome_driver.find_element_by_xpath('//*[@id="dob"]').send_keys(key)
    for key in date_of_birth[2]:
        chrome_driver.find_element_by_xpath('//*[@id="dob"]').send_keys(key) 
    sleep(2)
    # click continue
    chrome_driver.find_element_by_xpath('//*[@id="section1"]/div[3]/div[2]/div/div/a').click()
    sleep(2)    
    # page3
    # employ
    chrome_driver.find_element_by_xpath('//*[@id="emp_status_toggle"]/label[1]').click()
    # name of employer
    chrome_driver.find_element_by_xpath('//*[@id="emp"]').send_keys(submit['Uspd']['employer'])
    # occupation
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="emp_title"]').send_keys(submit['Uspd']['occupation'])
    # work phone number
    chrome_driver.find_element_by_xpath('//*[@id="emp_phone"]').send_keys(submit['Uspd']['work_phone'])
    sleep(2)
    # time of work
    index_timeofwork = random.randint(1,9)
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="emp_year"]'))
    s1.select_by_value(str(index_timeofwork))
    sleep(3)
    # monthly income
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="income"]'))
    s1.select_by_index(index_income)
    sleep(3)
    # how do you receive
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="direct_deposit"]'))
    s1.select_by_index(1)
    sleep(3)
    # date of next payday
    js='document.getElementById("pay_date").removeAttribute("readonly")'
    chrome_driver.execute_script(js)
    payday = Submit_handle.get_next_payday()
    payday_ = payday[0]+' '+str(payday[1])+','+str(payday[2])
    chrome_driver.find_element_by_xpath('//*[@id="pay_date"]').send_keys(payday_)
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="employment-continue"]').click()
    sleep(3)
    # page3
    # email
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Uspd']['email'])
    #  phone
    chrome_driver.find_element_by_xpath('//*[@id="home_phone"]').send_keys(submit['Uspd']['home_phone'])
    # home adress
    chrome_driver.find_element_by_xpath('//*[@id="address"]').send_keys(submit['Uspd']['address']) 
    # zip
    zipcode = Submit_handle.get_zip(submit['Uspd']['zip'])
    chrome_driver.find_element_by_xpath('//*[@id="zip_code"]').send_keys(zipcode)  
    # timeofwork
    index_timeofwork = random.randint(1,7)
    js="$('#res_year > option:nth-child(10)').removeAttr('selected')"
    chrome_driver.execute_script(js)
    js = '$("#res_year > option:nth-child('+str(index_timeofwork)+')").attr("selected","selected")'
    chrome_driver.execute_script(js) 
    sleep(1)
    # own home 
    chrome_driver.find_element_by_xpath('//*[@id="rent_own_toggle"]/label[2]').click()
    # drivers_license
    drivers_license = submit['Uspd']['drivers_license'].split('.')[0]
    chrome_driver.find_element_by_xpath('//*[@id="license"]').send_keys(drivers_license)
    sleep(1)    
    # drivers_license state
    license_state = submit['Uspd']['drivers_license_state']
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="lic_state"]'))
    s1.select_by_value(str(license_state))
    # ssn
    ssn = submit['Uspd']['ssn'].split('.')[0]
    chrome_driver.find_element_by_xpath('//*[@id="ssn"]').send_keys(ssn)
    # bank name
    element_ = '//*[@id="bank_name"]'
    element = selenium_funcs.scroll_and_find_up(chrome_driver,element_)
    sleep(2)
    element.send_keys(submit['Uspd']['bank_name'])
    # routing number
    routing_number = submit['Uspd']['routing_number'].split('.')[0]
    chrome_driver.find_element_by_xpath('//*[@id="bank_routing"]').send_keys(routing_number)
    # account number
    account_number = submit['Uspd']['account_number'].split('.')[0]
    chrome_driver.find_element_by_xpath('//*[@id="bank_accnt"]').send_keys(account_number)
    sleep(2)
    # confirm
    chrome_driver.find_element_by_xpath('//*[@id="tcpa-checkbox"]').click()
    sleep(1)
    url = chrome_driver.current_url
    # submit
    chrome_driver.find_element_by_xpath('//*[@id="submitbutton"]').click()
    sleep(10)
    url_ = chrome_driver.current_url
    if url != url_:
        sleep(600)
    chrome_driver.close()
    chrome_driver.quit()
    return 1
    
def test():
    # db.email_test()
    Mission_list = ['10009']
    excel = 'Ukpd'
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # submit['Mission_Id'] = '10055'
    # chrome_driver = Chrome_driver.get_chrome(submit)
    # web_submit(submit,chrome_driver,1)


if __name__=='__main__':
    test()
