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






def web_submit(submit):
    # test
    # site = 'https://finaff.go2affise.com/click?pid=3464&offer_id=9436'
    # submit['Site'] = site
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    chrome_driver.find_element_by_xpath('//*[@id="site-header"]/div/div/a[1]').click()
    i = 0
    while True:
    	try:
    		chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[1]/select').click()
    	except:
    		i+=1
    		if i >= 5:
    			break
    # page2
    num = random.randint(2010,2018) 
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="site-header"]/div/div/a[1]'))
    s1.select_by_value(str(num)) 
    s1 = Select(chrome_driver.find_element_by_xpath('//*[@id="site-header"]/div/div/a[1]'))
    s1.select_by_value(str(num))     
    s2 = Select(chrome_driver.find_element_by_xpath('//*[@id="site-header"]/div/div/a[1]'))
    s2.select_by_index(1)  
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[3]/div[1]/div/input').send_keys(submit['Firstname'])
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[3]/div[2]/div/input').send_keys(submit['Lastname'])
    # email
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[4]/div/input').send_keys(submit['Email_emu'])
    # phone
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[5]/div/input').send_keys(submit['Homephone'])
    # zipcode
    chrome_driver.find_element_by_xpath('//*[@id="postal-code"]').send_keys(submit['Zip'])
    num = random.randint(0,15) 
    s2 = Select(chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/div[8]/div/select'))
    s2.select_by_index(1)   
    chrome_driver.find_element_by_xpath('//*[@id="list-lead-form"]/button').click()  
    sleep(30)
    chrome_driver.close()
    chrome_driver.quit()
    return




 

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





if __name__=='__main__':
    submit={}
    submit['Ua'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    submit['Firstname'] = 'KIRSTEN'
    submit['Lastname'] = 'WOLD'
    submit['City'] = 'SPOKANE'
    submit['State'] = 'WA'
    submit['Homephone'] = '5093270780'
    submit['Email'] = 'kdwold@live.com'
    submit['Address'] = '2509 W. SHARP AVE.'   
    submit['zipcode'] = '79108'
    submit['month'] = '4'
    submit['day'] = '12'
    submit['year'] = '1964'
    submit['Height_FT'] = '5'
    submit['Height_Inch'] = '11'
    submit['Weight'] = '175'
    submit['Email_emu'] = 'GaleXavierapZeQ@yahoo.com'
    submit['Email_emu_pwd'] = 'd9TY7k80H'
    # test_num()
    # web_Submit(submit)
    site=email_confirm(submit)
    print(site)
