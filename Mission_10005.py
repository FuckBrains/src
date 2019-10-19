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
import Submit_handle
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

def web_submit(submit,chrome_driver,debug=0):
    name = check_name()
    while True:
        print('checking email')
        flag_check = check_email(submit['Email'])
        if flag_check == 1:
            print('used email:',submit['Email']['Email_emu'])
            db.write_one_info([str(submit['Mission_Id'])],submit)                        
            # continue
        else:
            print('find a good email:',submit['Email']['Email_emu'])
            break
        Mission_list = ['10005','10043']
        Excel_name = ['','Email']
        Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
        submit1 = db.read_one_excel(Mission_list,Excel_name,Email_list)
        submit['Email'] = submit1['Email']
    chrome_driver.get(submit['Site'])
    i = 0
    sleep(5)
    print('Loading finished')
    chrome_driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]").click()      #18+        
    sleep(2)
    # name = name_get.gen_one_word_digit(lowercase=False)    
    try:
        pwd = Submit_handle.password_get()
        chrome_driver.find_element_by_xpath("/html/body/div/div[2]/div/div[1]").click()      #question2
        sleep(2)
        chrome_driver.find_element_by_xpath("/html/body/div/div[3]/div/div[1]").click()      #question3
        sleep(3)
        chrome_driver.find_element_by_xpath("/html/body/div/div[4]/span").click()            #create account
        chrome_driver.switch_to_frame('myForm')
        chrome_driver.find_element_by_xpath("//*[@id='userName']").send_keys(name)
        chrome_driver.find_element_by_xpath("//*[@id='newPassword']").send_keys(pwd)
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
    db.write_one_info([str(submit['Mission_Id'])],submit)
    site = ''
    flag = 1
    handle = chrome_driver.current_window_handle
    try:            
        site = email_confirm(submit)  
        print(site)      
    except Exception as e:
        print('email check failed',str(e))
    if 'http://www.cam4.com/signup/confirm' in site:
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
                cookie_str = json.dumps(cookies)
                submit['Cookie'] = cookie_str
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

def activate(submit,chrome_driver):
    # https://www.cam4.com/
    chrome_driver.get('http://www.cam4.com/female')
    cookies = json.loads(submit['Cookie'])
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry']) 
        chrome_driver.add_cookie(cookie)    
    chrome_driver.get('http://www.cam4.com/female')
    try:
        chrome_driver.find_element_by_id('promotionsConsentModalLink').click()
        print('find no thanks')
    except:
        print('not find no thanks')
    randtime = random.randint(3,5)
    sleep(randtime)
    time_num =random.randint(3,6)
    flag = 1
    for i in range(time_num):
        num = random.randint(1,20)
        try:
            chrome_driver.get('http://www.cam4.com/female')
            #directoryDiv > div:nth-child(7) > div > a.clearfix > img
            #directoryDiv > div:nth-child(16) > div > a.clearfix > img
            #chrome_driver.find_element_by_xpath('//*[@id="directoryDiv"]/div['+str(num)+']/div/a[2]').click()
            #chrome_driver.find_element_by_css_selector('directoryDiv > div:nth-child(16) > div > a.clearfix > img')
            a = '//*[@id="directoryDiv"]/div['+str(num)+']/div/a[2]/img'
            chrome_driver.find_element_by_xpath(a).click()
            print('==================')
            cookies = chrome_driver.get_cookies()
            print(type(cookies))
            cookie_str = json.dumps(cookies)
            submit['Cookie'] = cookie_str
            # submit['Cookie'] = chrome_driver.get_cookies()                 
            db.update_cookie(submit)
        except:
            chrome_driver.get('http://www.cam4.com/female')
            print('no vedio find')
        sleep_time = random.randint(1,3)
        sleep(sleep_time*60)
    return 1

def email_confirm(submit,debug=0):
    print('----------')
    for i in range(3):
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


def test():
# mcsesofnkkt@hotmail.com----i4GkF2o4H9IF
# sotoyhj@hotmail.com----kqg8i7ytMJS6
# tasleestwrf@hotmail.com----wG01G8emF32q
# soaseighyyb@hotmail.com----P7sPF2g5YxY0
# soroattrxwv@hotmail.com----yMy3A1M0hERw
# boehlapgqkes@yahoo.com----vAinly5636
# WebsterCrystalkOoUf@yahoo.com----p3gxyxmjK
# InaJacknYsM@yahoo.com----loAO0Rs2v
# seanoawktws@outlook.com----9m8KQ7KDaSr9
# leasleshmrfj@outlook.com----eo4Xs2Umpxof
# satesethoxet@outlook.com----u4BLG0yzenXH
# shutoughfvkide@hotmail.com----vLnWz2K8zczx
# timpesmbo@hotmail.com----TvKwJ1plwvXG
# teythounfsd@hotmail.com----Lil2H74c3SX9
# filipeadcglrd@yahoo.com----MulGrEW640
# lavadivucfexha@yahoo.com----WomBolt960
# barberbofsjuis@yahoo.com----pYXiS430
# mcsethaymesnj@outlook.com----90r7v4l1zz1X
# tetosyifxcm@outlook.com----RYdQs2L6moHY
# gewekrj@outlook.com----6waNv29guUEQ
# zaringjlzok@yahoo.com----MCMakEn72
# ilolihgbftz@yahoo.com----ALpERt732
# lisesonoim@hotmail.com----uw21X4EPLNrP
# mcseyssewtma@hotmail.com----1NFG70TuPnnj
# tataffeapyj@hotmail.com----I4Hmr7fVND4w
# smounenxgugw@outlook.com----jSKXI17499Yt
# seysoughlwxbgq@outlook.com----VJnJI3pnI8Kr
# smotenrudi@outlook.com----46ra36fe8pvO
# GilbertaKitchinMTOO@yahoo.com----Grc15111ed----855381539009----1995-5-22
# AlaneProvoVKH@yahoo.com----saP8aovnww----855381314464----1995-12-24



    submit = {}
    submit['Email']= {
    'Email_emu': 'chris_riggan009@outlook.com', 
    'Email_emu_pwd': 'cradaju3!'
    } 
    # MicmjkwNjwihtfe@hotmail.com xRJAZZ2Ct
    site = email_confirm(submit)
    print(site)
    # MellvvukyCfedcc@hotmail.com 1ZYC5Cxwwj08u
    # import imap_test
    # imap_test.Email_emu_getlink(submit['Email'])


if __name__=='__main__':
    test()
