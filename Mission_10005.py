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



def web_submit(submit):
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    name = name_get.gen_one_word_digit(lowercase=False)
    chrome_driver.maximize_window()
    chrome_driver.refresh()
    flag = 0
    i = 0
    while i <=3:
        if 'Join CAM4' in chrome_driver.title:
            break
        else:
            chrome_driver.get(submit['Site'])
            sleep(5)
            i = i + 1   
    chrome_driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()      #18+
    chrome_driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()      #18+        
    name = name_get.gen_one_word_digit(lowercase=False)    
    try:
        chrome_driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]").click()      #question2
        chrome_driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]").click()      #question3
        chrome_driver.find_element_by_xpath("/html/body/div[1]/div[4]/span").click()            #create account
        chrome_driver.switch_to_frame('myForm')
        chrome_driver.find_element_by_xpath("//*[@id='userName']").send_keys(name)
        chrome_driver.find_element_by_xpath("//*[@id='newPassword']").send_keys(submit['Email_emu_pwd'])
        chrome_driver.find_element_by_xpath("//*[@id='email']").send_keys(submit['Email_emu'])
    except Exception as e:
        print('something error in registration',str(e))
        chrome_driver.close()
        chrome_driver.quit()
        return 0
    sleep(3)
    title = chrome_driver.title
    url = chrome_driver.current_url
    try:
        chrome_driver.find_element_by_xpath("//*[@id='paymentForm']/a/span").click()
    except Exception as e:
        chrome_driver.close()
        chrome_driver.quit()
        return 0
    status = 'fail'
    sleep(3)

    for i in range(3):
        if 'success' in chrome_driver.current_url :
            # status = 'success'
            # rantime = random.randint(5,10)
            # sleep(rantime*10)  
            # chrome_driver.close()
            # chrome_driver.quit()
            # return 1
            flag = 1
        else:
            chrome_driver.refresh()
    if flag==0:
        chrome_driver.close()
        chrome_driver.quit()
        return flag
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
        sleep(20)        
    else:
        flag = 1
        chrome_driver.close()
        chrome_driver.quit()
        return flag        
    handles=chrome_driver.window_handles   
    try:
        for i in handles:
            if i != handle:
                chrome_driver.switch_to.window(i)
                chrome_driver.refresh()                  
    except Exception as e:
        chrome_driver.close()
        chrome_driver.quit()    
        return flag    
    chrome_driver.close()
    chrome_driver.quit()
    return flag
        # submit['name'] = ng.gen_one_word_digit(lowercase=False)
        # status,submit['name'] = web_Submit(submit)

 
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
    site = email_confirm(submit)
    print(site)
