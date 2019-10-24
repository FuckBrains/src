
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
import db
import selenium_funcs
import emaillink


'''
CindyMatches (Done)
'''



def detect_email():
    url = r'https://www.cam4.com/signup/email?pageLocale=en'
    url2 = r'https://www.cam4.com/signup/username?pageLocale=en'


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




def web_submit(submit,chrome_driver,debug=0):
    Mission = '10021'
    # email_list = ['hotmail.com','outlook.com','gmail.com','msn.com']
    while True:
        submit1 = db.get_unique_soi_email(Mission)
        print(submit1)
        submit['SOI'] = submit1['SOI']
        if '@aol.com' in submit['SOI']['email']:
            continue
        else:
            break
    print(submit['SOI']['email'])    
    if debug == 1:
        site = 'http://flusnlb.com/0AqV'
        submit['Site'] = site        
    chrome_driver.get(submit['Site'])
    name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    # sleep(2000)
    # if 'cindyrnatches.com/landing?' not in chrome_driver.current_url:
    #     print('url wrong:',chrome_driver.current_url)
    #     chrome_driver.close()
    #     chrome_driver.quit()
    #     return
    sleep(5)
    try:
        chrome_driver.find_element_css_selector('body > div.container-fluid.splash > section > div:nth-child(2) > div > a').click()
    except:
        pass
    chrome_driver.find_element_by_xpath('//*[@id="email"]').send_keys(submit['SOI']['email'])
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="signupForm"]/div/div[3]/div[1]/button').click()
    # try:
    #     chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(submit['Email']['Email_emu_pwd'])
    # except:
    #     pass
    sleep(2)
    # ok
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[1]/div[2]/div/div/a').click()
    # next
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[2]/div[2]/div/a').click()
    # yes1
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[3]/div[2]/div/a[1]').click()
    # yes2
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[4]/div[2]/div/a[1]').click()
    # yes3
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[5]/div[2]/div/a[1]').click()
    # yes4
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[6]/div[2]/div/a[1]').click()
    # 3 answers
    keyword = ['Skinny','Regular','BBW','Big tits are a must','Sexy ass is a must']    
    keywords = get_keyword(keyword)
    for keyword in keywords:
        chrome_driver.find_element_by_partial_link_text(keyword).click()
        sleep(1)
    # 'next'
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[7]/div[2]/div[2]/a[1]').click()
    # 3 answers
    keyword = ['18 - 25','26 - 35','36 - 45','46 - 55','55+']
    keywords = get_keyword(keyword)
    for keyword in keywords:
        chrome_driver.find_element_by_partial_link_text(keyword).click()
        sleep(1)
    # next    
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[8]/div[2]/div[2]/a[1]').click()
    # 3 answers    
    keyword = ['One night stand','Sex on multiple occasions','Regular sex','Serious Dating','Marriage']
    keywords = get_keyword(keyword)
    for keyword in keywords:
        chrome_driver.find_element_by_partial_link_text(keyword).click()
        sleep(1)
    # next
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[9]/div[2]/div[2]/a[1]').click()
    # 3 answers
    keyword = ['Within walking','Same city','Nearby cities are OK','Same country',"Doesn't matter"]
    keywords = get_keyword(keyword)
    for keyword in keywords:
        chrome_driver.find_element_by_partial_link_text(keyword).click()
        sleep(1)   
    # next
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[10]/div[2]/div[2]/a').click()
    # start now
    chrome_driver.find_element_by_xpath('//*[@id="submit"]').click()
    sleep(5)
    # enter here    
    chrome_driver.find_element_by_xpath('//*[@id="q1"]/center/a/div').click()
    sleep(5)
    # next
    chrome_driver.find_element_by_xpath('//*[@id="btn_step1"]').click()
    # pwd
    pwd = Submit_handle.password_get() 
    chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(pwd)
    # next
    chrome_driver.find_element_by_xpath('//*[@id="btn_step2"]').click()
    # enter
    chrome_driver.find_element_by_xpath('//*[@id="btn_step3"]').click()
    sleep(90)
    chrome_driver.find_element_by_xpath('//*[@id="modalWindow_uni"]/p/a').click()
    sleep(90)
    return 1

 
def email_confirm(submit):
    print('----------')
    for i in range(10):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']
            title = 'Please verify your e-mail address'
            pattern = r'.*?(https://cindyrnatches.com/accounts/verify/email/[\w]{1,100})'
            # pattern = r'.*?(https://opinionoutpost.com/Membership/Intake\?signuptoken=.*?\&resp=([0-9]{5,15}))'
            url_link = emaillink.get_email(name,pwd,title,pattern)
            if 'Bad' in url_link:
            	print('Get duplicated email')
            	url_link = emaillink.get_email(name,pwd,title,pattern,True)
            if 'http' in url_link :
                break
        except Exception as e:
            print(str(e))
            print('===')
            sleep(15)
            pass
    return url_link

def get_keyword(keyword):
    keywords = []
    for i in range(3):
        num_ = random.randint(0,len(keyword)-1)  
        print(num_)  
        print(keyword[num_])
        keywords.append(keyword[num_])
        keyword.pop(num_)
    print(keywords)
    return keywords



def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_Id = '10012'
    Mission_list = [Mission_Id]
    excel = 'Email'    
    Excel_name = ['',excel]
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    # submit['Mission_Id'] = Mission_Id
    print(submit)
    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None]
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    # submit['Country'] = 'FR'
    submit['Alliance'] = 'offeriz'
    submit['Account'] = 1
    submit['Mission_Id'] = Mission_Id
    submit['ua']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)
    # submit['Email']['Email_emu'] = 'ThynnFoordbP@yahoo.com'
    # submit['Email']['Email_emu_pwd'] = 'tb3yy7c1k'
    # email_confirm(submit,debug=1)

if __name__=='__main__':
    test()
