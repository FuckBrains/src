from time import sleep
import random
import os
import time
import sys
import json
import re
from urllib import request, parse
import name_get
import Chrome_driver
import email_imap as imap
import re
from pyrobot import Robot
import Submit_handle
from selenium.webdriver.support.ui import Select


'''
Adsmain health
Auto
'''

def web_submit(submit,debug=0):
    # url = 'http://gkd.cooldatingz.com/c/11377/4?clickid=[clickid]&bid=[bid]&siteid=[siteid]&countrycode=[cc]&operatingsystem=[operatingsystem]&campaignid=[campaignid]&category=[category]&connection=[connection]&device=[device]&browser=[browser]&carrier=[carrier]'
    if debug == 1:
        site = 'http://im.datingwithlili.com/im/click.php?c=8&key=0jp93r1877b94stq2u8rd6hd'
        submit['Site'] = site     
    chrome_driver = Chrome_driver.get_chrome(submit)
    print('===========================')
    chrome_driver.get(submit['Site']) 
    sleep(3000) 
    flag = 0
    i = 0
    while i <=3:
        if 'trustedhealthquotes.com' in chrome_driver.current_url:
            break
        else:
            writelog(chrome_driver.current_url)
            chrome_driver.get(site)
            sleep(5)
            i = i + 1   
    try:
        if 'trustedhealthquotes.com' in chrome_driver.current_url:
            chrome_driver.find_element_by_xpath('//*[@id="address_1_zip"]').send_keys(submit['Auto']['zip'])
            chrome_driver.find_element_by_xpath('//*[@id="quickform-submit"]').click()
            handles = chrome_driver.window_handles
            if len(handles) == 2:
                chrome_driver.switch_to.window(handles[1])
                a = [
                '//*[@id="insured_1_gender_male"]',
                '//*[@id="insured_1_gender_female"]'
                ]
                num = random.randint(0,1)
                chrome_driver.find_element_by_xpath(a[num]).click()
                birthday = Submit_handle.get_auto_birthday(submit['Auto']['dateofbirth'])
                month = birthday[0]
                day = birthday[1]
                year = birthday[2]
                chrome_driver.find_element_by_xpath('//*[@id="insured_1_dobMM"]').send_keys(month)
                chrome_driver.find_element_by_xpath('//*[@id="insured_1_dobDD"]').send_keys(day)
                chrome_driver.find_element_by_xpath('//*[@id="insured_1_dobYYYY"]').send_keys(year)
                num_info = Submit_handle.get_height_info()
                chrome_driver.find_element_by_xpath('//*[@id="insured_1_heightFT"]').send_keys(num_info['Height_FT'])
                chrome_driver.find_element_by_xpath('//*[@id="insured_1_heightIN"]').send_keys(num_info['Height_Inch'])
                chrome_driver.find_element_by_xpath('//*[@id="insured_1_weight"]').send_keys(num_info['Weight'])
                chrome_driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(submit['Auto']['firstname'])
                chrome_driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(submit['Auto']['lastname'])
                chrome_driver.find_element_by_xpath('//*[@id="address_1_street1"]').send_keys(submit['Auto']['address'])
                chrome_driver.find_element_by_xpath('//*[@id="address_1_city"]').send_keys(submit['Auto']['city'])
                s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="address_1_state"]'))
                s1.select_by_value(str(submit['Auto']['state']))  # 选择value="o2"的项   
                homephone = submit['Auto']['homephone'].split('.')[0]                
                chrome_driver.find_element_by_xpath('//*[@id="phone1"]').send_keys(str(homephone)[0:3])
                chrome_driver.find_element_by_xpath('//*[@id="phone_2"]').send_keys(str(homephone)[3:6])
                chrome_driver.find_element_by_xpath('//*[@id="phone3"]').send_keys(str(homephone)[6:10])
                chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['Auto']['email'])
                num_click = random.randint(1,4)
                # sleep(2000)
                for i in range(num_click):
                    chrome_driver.find_element_by_xpath('//*[@id="plus"]').click()
                chrome_driver.find_element_by_xpath('//*[@id="income-widget"]/label[4]').click()
                chrome_driver.find_element_by_xpath('//*[@id="healthForm"]/div[14]/button').click()
                sleep(20)
                flag = 1
    except Exception as e:
        print(str(e))
    # sleep(3000)
    try:       
        chrome_driver.close()
        chrome_driver.quit()
    except Exception as e:
        print(str(e))
    return flag




 
def check_email(submit):
    print(submit['Email_emu'])
    data = {'email': submit['Email_emu']}
    data = parse.urlencode(data).encode('gbk')
    req = request.Request(url, data=data)
    page = ''
    for i in range(5):
        try:
            page = request.urlopen(req,timeout=10.0).read()
        except:
            continue
        if str(page) != '':
            break
    print(page)
    if 'GOOD_EMAIL' not in str(page):
        if page == '':
            return -1 #netwrong
        else:
            return 1 #fail
    else:
        print(submit['Email_emu'],'is GOOD_EMAIL')
        return 0 #success
    

def check_name(submit):
    data = {'username':submit['name']}
    data = parse.urlencode(data).encode('gbk')
    req = request.Request(url2, data=data)
    page = ''
    for i in range(5):
        try:
            page = request.urlopen(req,timeout=10.0).read()
        except Exception as msg:
            print(msg)
            continue   
        if str(page) != '':
            break
    print(page)
    if 'OK' not in str(page):
        return 1 #fail
    else:
        return 0    #success


def email_confirm(submit):
    site = ''
    for i in range(10):
        msg_content = imap.email_getlink(submit,'Subject: Verify at Cam4 to Continue')
        print(len(msg_content))
        if 'cam4' not in msg_content:
            print('Target Email Not Found !')
            sleep(10)
        else:
            c = msg_content.find('get verified:')
            a = msg_content.find('http://www.cam4.com/signup/confirm?uname=',c)
            b = msg_content.find('\n',a)
            site = msg_content[a:b]
            return site
    return site



if __name__=='__main__':
    submit={}
    submit['ua'] = ''
    submit['name'] = 'dfdss2343'
    submit['pwd'] = 'cvbsasdsddasz'
    submit['Email_emu'] = 'BettinaNavarroGx@aol.com'
    submit['Email_emu_pwd'] = 'G9x1C1zf'
	# LlwthdKlhcvr@hotmail.com----glL9jPND4nDp    
    # site='http://www.baidu.com'
    web_submit(submit)
    # BettinaNavarroGx@aol.com	G9x1C1zf
    # site = email_confirm(submit)
    # print(site)
    # test()
