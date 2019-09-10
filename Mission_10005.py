import emaillink
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
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC




'''
Cam4
'''


def detect_email():
    url = r'https://www.cam4.com/signup/email?pageLocale=en'
    url2 = r'https://www.cam4.com/signup/username?pageLocale=en'

def check_name():    
    url2 = r'https://www.cam4.com/signup/username?pageLocale=en'
    for i in range(10):
        name = name_get.gen_one_word_digit(lowercase=False)
        print(name)
        data = {'username':name}
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
            print('try',i,'time') #fail
        else:
            print('find good name:',name)
            break    #success
    return name

def web_submit(submit):
    name = check_name()
    while True:
        Mission_list = ['10005']
        Excel_name = ['','Email']
        Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
        submit1 = db.read_one_excel(Mission_list,Excel_name,Email_list)
        submit['Email'] = submit1['Email']  
        flag_check = check_email(submit['Email'])
        if flag_check == 1:
            print('used email:',submit['Email']['Email_emu'])
            db.write_one_info([str(submit['Mission_Id'])],submit)                        
            continue
        else:
            print('find a good email:',submit['Email']['Email_emu'])
            db.write_one_info([str(submit['Mission_Id'])],submit)            
            break
    chrome_driver = Chrome_driver.get_chrome(submit)
    print('==============')
    # wait = WebDriverWait(chrome_driver, 60) #等待的最大时间
    # input = wait.until(
    #     EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/div[1]'))
    # )
    # chrome_driver.maximize_window()
    # input.click()
    # chrome_driver.refresh()
    flag = 0
    i = 0
    while i <=3:
        if 'Join CAM4' in chrome_driver.title:
            print('find cam4')
            break
        else:
            try:
                chrome_driver.get(submit['Site'])
            except:
                pass
            sleep(5)
            i = i + 1   
    chrome_driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()      #18+
    chrome_driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()      #18+        
    # name = name_get.gen_one_word_digit(lowercase=False)    
    try:
        chrome_driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]").click()      #question2
        chrome_driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]").click()      #question3
        chrome_driver.find_element_by_xpath("/html/body/div[1]/div[4]/span").click()            #create account
        chrome_driver.switch_to_frame('myForm')
        chrome_driver.find_element_by_xpath("//*[@id='userName']").send_keys(name)
        chrome_driver.find_element_by_xpath("//*[@id='newPassword']").send_keys(submit['Email']['Email_emu_pwd'])
        chrome_driver.find_element_by_xpath("//*[@id='email']").send_keys(submit['Email']['Email_emu'])
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
                try:
                    chrome_driver.refresh() 
                except:
                    pass

                # url_active = 'https://www.cam4.com/'
                # chrome_driver.get(url_active)
                # chrome_driver.find_element_by_xpath('//*[@id="femalePreference"]').click()
                # sleep(3)
                # Chrome_driver.find_element_by_xpath('//*[@id="startWatching"]').click()
                cookies = chrome_driver.get_cookies()
                print(type(cookies))
                cookie_str = json.dumps(cookies)
                submit['Cookie'] = cookie_str
                # submit['Cookie'] = chrome_driver.get_cookies()                 
                db.update_cookie(submit)
                sleep(10)
    except Exception as e:
        print(str(e))
        chrome_driver.close()
        chrome_driver.quit()    
        return flag 
    chrome_driver.close()
    chrome_driver.quit()
    # sleep(20) 
    return flag
        # submit['name'] = ng.gen_one_word_digit(lowercase=False)
        # status,submit['name'] = web_Submit(submit)
 
def check_email(submit):
    url = r'https://www.cam4.com/signup/email?pageLocale=en'
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

def activate():
    site_url = 'https://www.baidu.com'
    # https://www.cam4.com/
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get(site_url)
    print('cam4....................')
    sleep(3000)

def email_confirm(submit,debug=0):
    print('----------')
    for i in range(2):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']          
            title = ('Verify at Cam4 to Continue','welcome@cam4.biz')
            pattern = r'.*?get verified:.*?(http://www.cam4.com/signup/confirm\?uname=.*?)Thank you'
            url_link = emaillink.get_email(name,pwd,title,pattern,True,debug)
            if 'http' in url_link :
                break                            
        except Exception as e:
            print(str(e))
            print('===')
            pass
        sleep(30)
    return url_link



def test_url():
    submit={}
    submit1 = {}
    submit1['ua'] = ''
    submit1['name'] = 'dfdss2343'
    submit1['pwd'] = 'cvbsasdsddasz'
    submit1['Email_emu'] = 'JaneAguilarl@yahoo.com'
    submit1['Email_emu_pwd'] = 'JIo7Ul0J'
    submit['Email'] = submit1
    # LlwthdKlhcvr@hotmail.com----glL9jPND4nDp    
    # site='http://www.baidu.com'
    submit1['Site'] = 'http://teamanita.com/click.php?c=2&key=l13335ju3dk7yyfdkh780kpw'
    web_submit(submit)
    # BettinaNavarroGx@aol.com  G9x1C1zf
    # site = email_confirm(submit,1)
    # print(site)
    # return site,submit
    # check_name()    


def test_email_live():
    submit = {}
    submit['Mission_Id'] = '10005'
    for i in range(20):
        Mission_list = ['10005']
        Excel_name = ['','Email']
        Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
        submit1 = db.read_one_excel(Mission_list,Excel_name,Email_list)
        submit['Email'] = submit1['Email']  
        flag_check = check_email(submit['Email'])
        if flag_check == 1:
            print('used email:',submit['Email']['Email_emu'])
            # db.write_one_info([str(submit['Mission_Id'])],submit)                        
            continue
        else:
            print('find a good email:',submit['Email']['Email_emu'])
            # db.write_one_info([str(submit['Mission_Id'])],submit)            
            continue    
if __name__=='__main__':
    test_email_live()

