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



def web_submit(submit):
    # url = 'http://gkd.cooldatingz.com/c/11377/4?clickid=[clickid]&bid=[bid]&siteid=[siteid]&countrycode=[cc]&operatingsystem=[operatingsystem]&campaignid=[campaignid]&category=[category]&connection=[connection]&device=[device]&browser=[browser]&carrier=[carrier]'
    chrome_driver = Chrome_driver.get_chrome(submit)
    print('===========================')
    chrome_driver.get(submit['Site'])  
    # https://install.stream-all.com/?pid=54939&clickid=6288828472&subid=1462   

    # print(chrome_driver.page_source)
    handle1 = chrome_driver.current_window_handle    
    chrome_driver.find_element_by_xpath('//*[@id="extOpener"]/p[2]/a').click()
    handles=chrome_driver.window_handles
    print(len(handles))
    # sleep(300)
    for i in handles:
        if i != handle1:
            chrome_driver.switch_to.window(i)
            handle2 = chrome_driver.current_window_handle    
            # chrome_driver.find_element_by_xpath('//*[@id="page-content-container"]/div[6]/div[2]/a/img').click()
            try:
                chrome_driver.find_element_by_link_text('ADD TO CHROME').click()
            except:
                sleep(10)
                rob = Robot()
                rob.key_press('tab')
                rob.key_press('enter')                
                chrome_driver.find_element_by_link_text('ADD TO CHROME').click()
    sleep(10)
    handles=chrome_driver.window_handles
    print('find',handles,'windows')
    for i in handles:
        if i != handle1 and i != handle2:
            chrome_driver.switch_to.window(i)
            chrome_driver.refresh()
            i = 0
            while True:
                try:
                    if i >= 20:
                        break
                    chrome_driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div').click()
                    break
                except:
                    i+=1
                    sleep(3)
    sleep(30)
    rob = Robot()
    rob.key_press('tab')
    rob.key_press('enter')
    # url_jump1 = re.match('https://install.',chrome_driver.page_source)
    # sleep(1000)

 
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
    # web_Submit(submit)
    # BettinaNavarroGx@aol.com	G9x1C1zf
    # site = email_confirm(submit)
    # print(site)
    test()
