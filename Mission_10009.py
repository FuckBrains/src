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
import name_get
import emaillink


'''
Stripchat(Done)
'''

def get_name():
    name = name_get.gen_one_word_digit(lowercase=False)  
    a_name = ['a','b','c','d','e','f','g','h','i','j','k','l','a','b','c','d','e','f','g','h','i','j','k','l']
    num_name = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9]
    num_insert = random.randint(2,len(name))
    # print(name[0:num_insert] )
    name_3 = random.randint(0,10)
    first_insert = a_name[name_3]+str(num_name[name_3])
    name = name[0:num_insert]+ first_insert+ str(num_name[num_insert])+name[num_insert:-1]+a_name[num_insert]
    print(name) 
    return name    

def web_submit(submit,chrome_driver,debug=0):
    if debug == 1:
        # site = 'http://track.meanclick.com/im/click.php?c=9&key=4ld1iyw2l4iwy1u0k4n8hn1c'
        site = 'https://creative.strpjmp.com/LPExperience/?action=signUpModalDirectLinkInteractive&campaignId=66a29c1c25bce64b38c92f4bcf56b4e21e619817ab1aab514ce8203143a60a47&creativeId=703743f02fd260bf1c2309c89b9ebf898145c006091f4ce79fe9822a73fddf22&domain=stripchat&exitPages=LPSierra%2CLPSierra%2CLPAkira&memberId=D-602781-1564542573-bjuOIMY723549&modelName=EvyDream&shouldRedirectMember=1&sourceId=&userId=32976296468dd516e6deecdb98dd5a54eee16e2ef856a243a1eb8e54921f0f03'
        submit['Site'] = site   
    chrome_driver.get(submit['Site'])
    # sleep(2000)
    chrome_driver.refresh()    
    name = get_name()
    # sleep(2000)  
    # 'https://creative.strpjmp.com/LPExperience/?action=signUpModalDirectLinkInteractive&campaignId=66a29c1c25bce64b38c92f4bcf56b4e21e619817ab1aab514ce8203143a60a47&creativeId=703743f02fd260bf1c2309c89b9ebf898145c006091f4ce79fe9822a73fddf22&domain=stripchat&exitPages=LPSierra%2CLPSierra%2CLPAkira&memberId=D-602781-1564542573-bjuOIMY723549&modelName=EvyDream&shouldRedirectMember=1&sourceId=&userId=32976296468dd516e6deecdb98dd5a54eee16e2ef856a243a1eb8e54921f0f03'
    if 'creative.strpjmp.com' in chrome_driver.current_url:
        try:
            chrome_driver.find_element_by_xpath('/html/body/div/div[2]/header/div/div/nav[1]/div[1]/a').click()
        except:
            pass
    chrome_driver.find_element_by_xpath('//*[@id="body"]/div/div/header/div/div/nav[2]/div[3]/a[2]').click()
    sleep(3)
    try:
        chrome_driver.find_element_by_xpath('//*[@id="sign_up_input_login"]').send_keys(name)
    except Exception as e:
        print('get site but cannot click',str(e))
        # sleep(2000)
        chrome_driver.close()
        chrome_driver.quit()
        return 0
    sleep(3)
    url_current = chrome_driver.current_url
    try:
        # chrome_driver.find_element_by_xpath('//*[@id="sign_up_input_login"]')
        chrome_driver.find_element_by_xpath('//*[@id="sign_up_input_email"]').send_keys(submit['Email']['Email_emu'])
    except Exception as e:
        print('get site but fail to register',str(e))
        chrome_driver.close()
        chrome_driver.quit()
        return 0         
    sleep(3)    
    try:
        chrome_driver.find_element_by_class_name('btn-login').click()
        print('Jump1')
    except Exception as e:
        print('get site but fail to register',str(e))
        chrome_driver.close()
        chrome_driver.quit()
        return 0 
    # try:
    #     chrome_driver.find_element_by_css_selector('#sign_up_input_email')
    #     print('get site but fail to register',str(e))
    #     chrome_driver.close()
    #     chrome_driver.quit()  
    #     return 0
    # except Exception as e:
    #     print('regester success')
    sleep(5)
        # chrome_driver.find_element_by_xpath('//*[@id="sign_up_input_login"]')
    # if chrome_driver.current_url == url_current:
    #     chrome_driver.close()
    #     chrome_driver.quit()
    #     return 0
    db.write_one_info([str(submit['Mission_Id'])],submit) 
    print('Wait 30 seconds to get email from stripchat')       
    sleep(20)
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
        sleep(10)        
    else:
        chrome_driver.close()
        chrome_driver.quit()
        return 1       
    handles=chrome_driver.window_handles   
    try:
        for i in handles:
            if i != handle:
                chrome_driver.switch_to.window(i)
                if 'Email successfully confirmed' not in chrome_driver.page_source:
                    chrome_driver.refresh()
                for i in range(2):
                    try:
                        chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(submit['Email']['Email_emu_pwd'])
                        sleep(1)
                        chrome_driver.find_element_by_xpath('//*[@id="confirmPassword"]').send_keys(submit['Email']['Email_emu_pwd'])
                        sleep(1)
                        chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/form/div[4]/button').click()
                        sleep(1)
                        cookies = chrome_driver.get_cookies()
                        cookie_str = json.dumps(cookies)
                        submit['Cookie'] = cookie_str
                        db.update_cookie(submit) 
                        break                          
                    except Exception as e:
                        print('',str(e))
                        chrome_driver.close()
                        chrome_driver.quit()    
                        return 1                       
    except Exception as e:
        print('',str(e))
        chrome_driver.close()
        chrome_driver.quit()    
        return 1
    try:
        chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/a').click()
    except:
        chrome_driver.close()
        chrome_driver.quit()    
        return 1             
    sleep(5)
    try:
        chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/div[3]/div[7]/div/a').click()
        sleep(5)
        cookies = chrome_driver.get_cookies()
        print(type(cookies))
        cookie_str = json.dumps(cookies)
        submit['Cookie'] = cookie_str
        # submit['Cookie'] = chrome_driver.get_cookies()                 
        db.update_cookie(submit)
        sleep(10)        
    except:
        chrome_driver.close()
        chrome_driver.quit()
        return 1
    sleep(10)        
    chrome_driver.close()
    chrome_driver.quit()
    return 1

def email_confirm(submit,debug=0):
    print('----------')
    'http://trk.email.supportlivecam.com/5d98b9e3f31adfe9/4jSW2YXJcfberP75P97dFQUi6qHxSNMJtfJRkyiZ5E9qw2qbjXUhJJhikE1gA83zGAGRQxCMANZDtJMi8UK1yZXcNLevh7yhEgXDk9aE1GaEMHJXiRSi3DvJatWgh43zVH1KC2PQftWjZcfSACY2rpHKu5VAzTR5cmMZBa2cCqEWkDoBNeLyHSwMv7U1Z7UQfof6VANgVCpo7gCzM8SN4VYNBX6fCrRPJTQKyZhSmZuuv5yPbbPsYpVsr6sUgCHFxy3BNsQXTCT9TiYBFpUetE6qdtcqhuHurpEzXvc3Uzj9KMGSY3Za9XnSGyMkBSB9MFm24zyvmAthkcc8vnEA1nSFf3zZXKH3QAJkUwCctxNaEN24E3UAFshAJFFy3yzwzPNyyou7537WVqyTqip8H7TNUGHc6hsLjm2JSucmzz8BKLBhzqtv4a5zwSBPXDBmtrCUpnrfedxFc8w4MWyTPqQBKCjxqEtMYNmsyD9xC7DhZSDAyG5HLFAANr6Ynxo3ouj2sRnHSH2uM1e7f4R8KNametB4eMBAKU7jsoHCi5vQDq'
    'http://trk.account.stripchat.com/902a2a3b61ec72e5/644Di25DRvShUhjU8ZnJo9VcimqL6D7SX4cotvhGhy4GW2zRcXW1fvj5tzzfuFiWHeCxvJ96o7q7fGsszkRRJyYpRZ7smGBPR6JvtTYhLmFWRS5qFfNvUW36Utv5sHHHJuSsZCprbtG3mDUZDwPYdPg9zCmWCqWxUmy2scGE5nFqkc1ixFvpq1bqJPZPDzP1toipxi1L1svsiBtSjarPVpRfiD6knagJyV6B8ZBnTVSsSD9JPra8V1gyxbM1pK6hJzo5LxBumBV4XXRWHBFPBtuP2nV6ZYLKFDEG98DDb6amjWahGdQytgxA9YovxBQhTABxgwp2ND25PbFB4962eQfeNP7PjUS6WxPXRRx1GVa47fGeRox7HCHTmEzhAm5iHhu1goQLrRuMA8kwxhwaLPUZSUSGpKJqRwUe5T2DdFAnAgco9ffxUwduEztD3Xf3EUtvhK1tBLTWuywKQjVscUVzyj2gaML9gcyf5621Jpfff7QsS2qzni72smyGoC9WtcSG4rKw845jSRjTTwTHa1Udhyf2LNzqg47'
    sleep(10)
    for i in range(2):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']
            title = ('Email Verification','noreply@account.stripchat.com')
            pattern = r'.*?Confirm Your Email.*?(http://trk.account.stripchat.com/.*?)By clicking on the link you give us'
            url_link = emaillink.get_email(name,pwd,title,pattern,True,debug)
            sleep(5)
            if 'http://trk.account.stripchat.com' in url_link :
                break            
            title = ('Email Verification','noreply@email.stripchat.com')
            pattern = r'.*?Confirm Your Email.*?(http://trk.account.stripchat.com/.*?)By clicking on the'
            url_link = emaillink.get_email(name,pwd,title,pattern,True,debug)
            if 'http://trk.account.stripchat.com' in url_link :
                break                            
        except Exception as e:
            print(str(e))
            print('===')
            pass
        sleep(30)
    return url_link

def activate(submit,chrome_driver):
    # https://www.cam4.com/
    chrome_driver.get('https://stripchat.com')
    cookies = json.loads(submit['Cookie'])
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry']) 
        chrome_driver.add_cookie(cookie)    
    chrome_driver.get('http://stripchat.com')
    # sleep(1000)
    randtime = random.randint(3,5)
    sleep(randtime)
    time_num =random.randint(1,4)
    flag = 1
    for i in range(time_num):
        num = random.randint(1,20)
        try:
            chrome_driver.get('http://stripchat.com')
            #directoryDiv > div:nth-child(7) > div > a.clearfix > img
            #directoryDiv > div:nth-child(16) > div > a.clearfix > img
            #chrome_driver.find_element_by_xpath('//*[@id="directoryDiv"]/div['+str(num)+']/div/a[2]').click()
            #chrome_driver.find_element_by_css_selector('directoryDiv > div:nth-child(16) > div > a.clearfix > img')
            a = '//*[@id="app"]/div/div/div[2]/div/div/div[3]/div['+str(num)+']/div/a'
            # a = '//*[@id="app"]/div/div/div[2]/div/div/div[3]/div[2]/div/a/div/span'
            # a = '//*[@id="app"]/div/div/div[2]/div/div[3]/div['+str(num)+']/div/a/div/span'
            chrome_driver.find_element_by_xpath(a).click()
            print('==================')
            cookies = chrome_driver.get_cookies()
            print(type(cookies))
            cookie_str = json.dumps(cookies)
            submit['Cookie'] = cookie_str
            # submit['Cookie'] = chrome_driver.get_cookies()                 
            db.update_cookie(submit)
        except Exception as e:
            print(str(e))
            # chrome_driver.get('http://stripchat.com')
            print('no vedio find')
        sleep_time = random.randint(1,3)
        print('sleep',sleep_time,'minutes')
        sleep(sleep_time*60)
    return 1
def charge():
    chrome_driver.get('https://stripchat.com')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    cookie = '[{"domain": "stripchat.com", "expiry": 1600716196, "httpOnly": false, "name": "baseAmpl", "path": "/", "secure": false, "value": "%7B%22platform%22%3A%22Web%22%2C%22device_id%22%3A%225949384b-41ac-42e8-a445-418bb76ce912R%22%2C%22session_id%22%3A1569180105643%2C%22up%22%3A%7B%22page%22%3A%22view%22%2C%22navigationParams%22%3A%7B%22limit%22%3A60%2C%22offset%22%3A0%7D%7D%7D"}, {"domain": "stripchat.com", "expiry": 1569180243, "httpOnly": false, "name": "_gat", "path": "/", "secure": false, "value": "1"}, {"domain": "stripchat.com", "expiry": 1600716185, "httpOnly": false, "name": "guestWatchHistoryIds", "path": "/", "secure": false, "value": ""}, {"domain": "stripchat.com", "expiry": 1600716124.14764, "httpOnly": true, "name": "stripchat_com_ABTest_recommended_key", "path": "/", "secure": false, "value": "B"}, {"domain": "stripchat.com", "expiry": 1569266581, "httpOnly": false, "name": "_gid", "path": "/", "secure": false, "value": "GA1.2.572702782.1569180106"}, {"domain": "stripchat.com", "expiry": 1632252181, "httpOnly": false, "name": "_ga", "path": "/", "secure": false, "value": "GA1.2.54903429.1569180106"}, {"domain": "stripchat.com", "expiry": 1571772198.044346, "httpOnly": true, "name": "stripchat_com_sessionRemember", "path": "/", "secure": true, "value": "1"}, {"domain": "stripchat.com", "expiry": 1571772198.044113, "httpOnly": true, "name": "stripchat_com_sessionId", "path": "/", "secure": true, "value": "f97a85844eae195aa598cc7c9134a5e6a19a64e139be5f0c2e1e8a78404a"}, {"domain": "stripchat.com", "expiry": 1600716105, "httpOnly": false, "name": "alreadyVisited", "path": "/", "secure": false, "value": "1"}, {"domain": "stripchat.com", "expiry": 1600716185, "httpOnly": false, "name": "isVisitorsAgreementAccepted", "path": "/", "secure": false, "value": "1"}, {"domain": "stripchat.com", "expiry": 1600716198, "httpOnly": false, "name": "guestSubscriptionIds", "path": "/", "secure": false, "value": ""}, {"domain": "stripchat.com", "expiry": 253402257600, "httpOnly": false, "name": "G_ENABLED_IDPS", "path": "/", "secure": false, "value": "google"}, {"domain": "stripchat.com", "expiry": 1884540186, "httpOnly": false, "name": "amplitude_id_19a23394adaadec51c3aeee36622058dstripchat.com", "path": "/", "secure": false, "value": "eyJkZXZpY2VJZCI6IjU5NDkzODRiLTQxYWMtNDJlOC1hNDQ1LTQxOGJiNzZjZTkxMlIiLCJ1c2VySWQiOiIyMTIyNjU5MCIsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU2OTE4MDEwNTY0MywibGFzdEV2ZW50VGltZSI6MTU2OTE4MDE4NjA1MywiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6OSwic2VxdWVuY2VOdW1iZXIiOjl9"}, {"domain": "stripchat.com", "expiry": 1600716125.042566, "httpOnly": true, "name": "stripchat_com_modelLandingNamespace", "path": "/", "secure": false, "value": "none"}, {"domain": "stripchat.com", "expiry": 1576956185.479051, "httpOnly": true, "name": "stripchat_com_affiliateId", "path": "/", "secure": false, "value": "1240cbd3455450b5c499e77219039717203959411ca4f7e1d644be59ffb037fc"}]'
    cookies = json.loads(submit['Cookie'])
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry']) 
        chrome_driver.add_cookie(cookie)    
    chrome_driver.get('http://stripchat.com')
    sleep(3000)


def test_p():
    name = name_get.gen_one_word_digit()
    # print(name)
    a_name = ['a','b','c','d','e','f','g','h','i','j','k','l','a','b','c','d','e','f','g','h','i','j','k','l']
    num_name = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9]
    num_insert = random.randint(2,len(name))
    # print(name[0:num_insert] )
    name_3 = random.randint(0,10)
    first_insert = a_name[name_3]+str(num_name[name_3])
    name = name[0:num_insert]+ first_insert+ str(num_name[num_insert])+name[num_insert:-1]+a_name[num_insert]
    print(name)

def test_email():
    link = '''
    ["Receive Your Password and Confirm&nbsp;Your&nbsp;Email\ntSkAodxI1b\n\nConfirm Your Emailhttp://trk.account.stripchat.com/89438ec23c551e86/5v5QRb5xWptcRfSPRAuYAj5P9wQfwyK85VDj4sCZPVmwFKZaLgRTHbBo6eTJerNSGNKaRbcarJCrpmjmGBXS4S2XXcJkEdQfkZrs9Yz9mXEKVHYaDrt9EGWEeen7Evu7LRzHkQDrGyUa1bDYyMUA9TbtwZuv9fsUvvy6TrdSRzvaYVfBNEkY2A79APgFJ9rNMUQzafcQyBcBhCPufXjEFx4vgbFDmwHBZtbebnGiKqRCzuuqQfhC8fcGWMAj2dC2kn83d9sYGTYxprRxtQWP5buP4qyt1cug2iaA8g6Q11jwb9rSA9sctmcxXKZfuNW5j46E9PbaGJjj3KrYroUcsuMDajiV4KmG72PemEKGXTYXWEq22G5S3HS7udxh76oAZNKZJU1Du7Q4ybmuAqvDbBy clicking on the link you give us the confirmation of your registration and that you are at least 18 yo (21 for the USA). You`ll be automatically subscribed to the system and promotional newsletters from Stripchat. You can unsubscribe at any time and we'll never share your details.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n--\nUnsubscribe: http://trk.account.stripchat.com/6e734b4cda54bfe5/T1AjZnnAUdbBPrcQKQDZmWjXDm6atzpezFeMvQBfy1d7aXTeGs5JUAa4Wv6TmKSaYGbxGjTwytSKeNNMEvDKg4eomZLGoUKHigC48vYgAbocTjaM2u3BGoaKUJYWYy1RVn89ihyBpWEfdAgp5eV2Vb3gZh4EPZZ9f8M55S8vRcAd3DAQcz9fjUQw66gZxaUic8zs5WZgXS1d57K8Vjw3DsVuk4tmdHKtTPMEAA2fRsi8ChyNxinh1mbTQvL5gkiZfbRaPAZrvvuaaM68cqD5f65neXD1CyR2UNRQKGqXp2Sz7CL7VaZrPtxmg8szY", '<!DOCTYPE html>\n<html>\n<head>\n    <title>Email Verification</title>\n    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <meta http-equiv="X-UA-Compatible" content="IE=edge" />\n    <style type="text/css">\n        @media screen {\n            @font-face {\n                font-family: \'Lato\';\n                font-style: normal;\n                font-weight: 400;\n                src: local(\'Lato Regular\'), local(\'Lato-Regular\'), url(https://fonts.gstatic.com/s/lato/v11/qIIYRU-oROkIk8vfvxw6QvesZW2xOQ-xsNqO47m55DA.woff) format(\'woff\');\n            }\n\n            @font-face {\n                font-family: \'Lato\';\n                font-style: normal;\n                font-weight: 700;\n                src: local(\'Lato Bold\'), local(\'Lato-Bold\'), url(https://fonts.gstatic.com/s/lato/v11/qdgUG4U09HnJwhYI-uK18wLUuEpTyoUstqEm5AMlJo4.woff) format(\'woff\');\n            }\n\n            @font-face {\n                font-family: \'Lato\';\n                font-style: italic;\n                font-weight: 400;\n                src: local(\'Lato Italic\'), local(\'Lato-Italic\'), url(https://fonts.gstatic.com/s/lato/v11/RYyZNoeFgb0l7W3Vu1aSWOvvDin1pK8aKteLpeZ5c0A.woff) format(\'woff\');\n            }\n\n            @font-face {\n                font-family: \'Lato\';\n                font-style: italic;\n                font-weight: 700;\n                src: local(\'Lato Bold Italic\'), local(\'Lato-BoldItalic\'), url(https://fonts.gstatic.com/s/lato/v11/HkF_qI1x_noxlxhrhMQYELO3LdcAZYWl9Si6vvxL-qU.woff) format(\'woff\');\n            }\n        }\n\n        body,\n        table,\n        td,\n        a {\n            -webkit-text-size-adjust: 100%;\n            -ms-text-size-adjust: 100%;\n        }\n        table,\n        td {\n            mso-table-lspace: 0pt;\n            mso-table-rspace: 0pt;\n        }\n        img {\n            -ms-interpolation-mode: bicubic;\n        }\n        img {\n            border: 0;\n            height: auto;\n            line-height: 100%;\n            outline: none;\n            text-decoration: none;\n        }\n\n        table {\n            border-collapse: collapse !important;\n        }\n\n        body {\n            height: 100% !important;\n            margin: 0 !important;\n            padding: 0 !important;\n            width: 100% !important;\n        }\n        a[x-apple-data-detectors] {\n            color: inherit !important;\n            text-decoration: none !important;\n            font-size: inherit !important;\n            font-family: inherit !important;\n            font-weight: inherit !important;\n            line-height: inherit !important;\n        }\n        @media screen and (max-width:600px) {\n            h1 {\n                font-size: 32px !important;\n                line-height: 32px !important;\n            }\n        }\n        div[style*="margin: 16px 0;"] {\n            margin: 0 !important;\n        }\n    </style>\n</head>\n<body style="background-color: #e5e5e5; margin: 0 !important; padding: 0 !important;">\n    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: \'Lato\', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">\n        \n\n\n\n\n\n\n    </div>\n    <table border="0" cellpadding="0" cellspacing="0" width="100%">\n        <tr>\n            <td bgcolor="#e5e5e5" align="center">\n                <!--[if (gte mso 9)|(IE)]>\n                <table align="center" border="0" cellspacing="0" cellpadding="0" width="600">\n                <tr>\n                <td align="center" valign="top" width="600">\n                <![endif]-->\n                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">\n                        <tr>\n                            <td align="center" valign="top" style="padding: 40px 10px 40px 10px;">\n                                <a href="http://trk.account.stripchat.com/c71595161ed98b00/ZfYTnFMY8ojwJgVKaBWZuVbdpRE1nt1JSPKv7nKa5bZH72wveSUcGxaJyi7vn8N7cGQiXM32scsjgk5hgQCUVbYFoHvvf5tcm2jp67Ukr7vTB1h1HYGiSbj3VYsZDUAfA6eAVfm2uFvASAHLc2LG3j3GJZmemyXuC4mDay2hmhsJzFiaXUdo44mRfNvmJjYxqWtfNvMd1GAsW8hYkvXqJ7a8rFCHRfDeWeGXoDKGoFCrD7R1gAyVkBPKrqvEwkbtusXyPaHCB5XVZMTwJZnbRsoJoS7Ktamq6BemwCATSa78UgE5fxFUQ2HxvW5K9zQEqmea9JsN5K6voBeahfabwhKYMDxk5CP4fC4RHWg4fwxHtW8Kf2iCrMfHaX7YT7upRigycF6LS42bTpPuUropYZoFoH72p6sjLgV1XA8cMMNrx4kiqj7nx2gZpP3MUcs8zXFKeYgFG34" target="_blank" name="link1"><img alt="Stripchat" src="http://trk.account.stripchat.com/75d410c07/6e5f406d367d52cc/4CzNCizeHEWyhYUm4wFeNUkHZt5H6gomnmZ8TfPfvYLKPrGmS57w1U88y2iPCxgqHnnWgjBNV1UhJY1onv8jseifwsA1d554fhhXL1x5j6dmj5sWtArb2hhbW" width="156" height="30" style="display: block; width: 156px; max-width: 156px; min-width: 156px; font-family: \'Lato\', Helvetica, Arial, sans-serif; color: #ffffff; font-size: 18px;" border="0"></a>\n                            </td>\n                        </tr>\n                    </table>\n                <!--[if (gte mso 9)|(IE)]>\n                </td>\n                </tr>\n                </table>\n                <![endif]-->\n            </td>\n        </tr>\n        <tr>\n            <td bgcolor="#e5e5e5" align="center" style="padding: 0px 10px 0px 10px;">\n                <!--[if (gte mso 9)|(IE)]>\n                <table align="center" border="0" cellspacing="0" cellpadding="0" width="600">\n                <tr>\n                <td align="center" valign="top" width="600">\n                <![endif]-->\n                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">\n                        <tr>\n                            <td bgcolor="#ffffff" align="center" valign="top" style="padding: 40px 20px 20px 20px; border-radius: 4px 4px 0px 0px; color: #414141; font-family: \'Lato\', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; line-height: 36px;">\n                                <img alt="" src="http://trk.account.stripchat.com/75d410c07/41c58d491c96fbb8/5VeWYberfAwR33Gi9WEZoMjvSKw5rYRFF5RqFFLrJpgA2MSfdDYjmJu1FtgfrMdx3vdLtPaNHxw5V1U93qds1sXzJEEVpbqFj57kCdrmT4S37v" width="80" height="97" style="display: block; border: 0px;" />\n                                <br>\n                                <h2 style="font-size: 30px; font-weight: 600; line-height: 36px; margin: 0;">\n                                    \n                                        \n                                            Receive Your Password and Confirm&nbsp;Your&nbsp;Email\n                                        \n                                    \n                                </h2>\n                            </td>\n                        </tr>\n                    </table>\n                <!--[if (gte mso 9)|(IE)]>\n                </td>\n                </tr>\n                </table>\n                <![endif]-->\n            </td>\n        </tr>\n        <tr>\n            <td bgcolor="#e5e5e5" align="center" style="padding: 0px 10px 0px 10px;">\n                <!--[if (gte mso 9)|(IE)]>\n                <table align="center" border="0" cellspacing="0" cellpadding="0" width="600">\n                <tr>\n                <td align="center" valign="top" width="600">\n                <![endif]-->\n                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">\n                        <tr>\n                            <td bgcolor="#ffffff" align="center" style="padding: 20px 30px 20px 30px; color: #414141; font-family: \'Lato\', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">\n                                <p style="margin: 0;">\n                                    \n    \n        Good news, you are ready to explore Stripchat. Please see your auto-generated password below. For security reasons we recommend changing your password in <a style="color: #69a8e0 !important; text-decoration: underline;" href="http://trk.account.stripchat.com/1bfe6f99e2d54f2a/JgL9sQaeZ59E8zKo2Vo5Rjk9F9pcdxUAcpVqfz1cdzbkwm6s117NaNg9Y3oiXzZXGq7j6ruvdfGtUaZykAtNjb2gSndpWnCCxqTPH3YEUtqZZuFHdhabEg6wwZuecxbGDuFDZGkzG4qoZZxY3x5QmYYuuPyzqrQt6sZkqL5XvJF2Khj6rcnoM6o9Tx7D3Ccu1iytPpiL8edHCZa8Q7FgU3zMScykaMSW6WWQ29pojCedZwipT1YepXYdcHVto9WwL26Twuahgdg7ogMY5cxHJ1LdPNoWdWiyRCrtjtRffaPbWxQFwqpkJ1xpBQaX5vUVZ7NiQgh2DXWdymBht8isA7gSxvMnQ5kkEfU3pyKJ8jiSBPiM7ScE95uzxyK7Ztx42sJxS5F3No1pF4bkUvmUCN2AyuGZYWZAtYtAetxmUuYwx7S7H9GbCPFBTUPkAV1JjtCuwmvwdMGaN9vNKJv8rR">Settings and Privacy</a>.\n    \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n                                </p>\n                              \t<br>\n                                <span style="background-color: #f6f6f6; border: 1px solid #dfdfdf; display: block; font-size: 24px; padding: 10px 20px;">\n                                    tSkAodxI1b\n                                </span>\n                              \t\n                                    \n                                        <br>\n                                        <p style="margin: 0;">\n                                        Please confirm your email by clicking on the button below.\n                                        </p>\n                                    \n                                \n                            </td>\n                        </tr>\n                      \t\n                            \n                            <tr>\n                                <td bgcolor="#ffffff" align="left">\n                                    <table width="100%" border="0" cellspacing="0" cellpadding="0">\n                                        <tr>\n                                            <td bgcolor="#ffffff" align="center" style="padding: 0px 30px 40px 30px;">\n                                                <table border="0" cellspacing="0" cellpadding="0">\n                                                    <tr>\n                                                        <td align="center" style="border-radius: 50px;" bgcolor="#f8494e"><a href="http://trk.account.stripchat.com/4d719bd97e91b3c6/644Di25DRvShQLjbzBvF4av9S98kfesa7jM5NB1uqi1hFu4WaTH62HBXXeuor2UiyCKmh3bKGEChRMFBPfrhGLbhufLVGsEw1H8jmocjkADja8tGKi4sgAXBew51xKgWXKGHp4xRGpGiZs8gohHFPykkoEK6uJf1MhRaP2knDQFTQXiZ2ukR5ZV1BcRwKgoPrTujM6PiKdSqagQ1xSrcBoxkDaEau5qVA9EpzH3Z15NGam8Gia9VVa1TdANDtEqZnYvJocMg5acATFGTi9a9b25QqUUgXqMqWQhPEzP6HBgmnGZnZiqT3Vk4HUSFQC9FdVnU1rqpFvM8nuXbVrinrNG2wi3SySoqxaLF1AvbbaDhNBvZgP15pKz1xgKQyh8kHenC6nxnYaKXZXtsmsE1WENmaebUB5YoV5EBFsyyPdHaVNw9C76Yk5H1drwZx8wu9QhtMxstRucecSWL8NKeytFc59zYb7gAcHT6x8bacid4Wp59DJB4co5NZoKQVrVNjjZ3hT2cANMGmEySZvzDeBnHcZXfQchYH39" target="_blank" style="font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 50px; border: 1px solid #f34a4d; display: inline-block;" name="link2">Confirm Your Email</a></td>\n                                                    </tr>\n                                                </table>\n                                            </td>\n                                        </tr>\n                                    </table>\n                                </td>\n                            </tr>\n                            \n                        \n                    </table>\n                <!--[if (gte mso 9)|(IE)]>\n                </td>\n                </tr>\n                </table>\n                <![endif]-->\n            </td>\n        </tr>\n        <tr>\n            <td bgcolor="#e5e5e5" align="center" style="padding: 0px 10px 0px 10px;">\n                <!--[if (gte mso 9)|(IE)]>\n                <table align="center" border="0" cellspacing="0" cellpadding="0" width="600">\n                <tr>\n                <td align="center" valign="top" width="600">\n                <![endif]-->\n                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">\n                        <tr>\n                            <td bgcolor="#f2f2f2" align="center" style="padding: 30px 30px 30px 30px; border-radius: 0px 0px 4px 4px; color: #747474; font-family: \'Lato\', Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px;">\n                                <p style="margin: 0;">By clicking on the link you give us the confirmation of your registration and that you are at least 18 yo (21 for the USA). You`ll be automatically subscribed to the system and promotional newsletters from Stripchat. You can unsubscribe at any time and we\'ll never share your details.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n</p>\n                            </td>\n                        </tr>\n                    </table>\n                <!--[if (gte mso 9)|(IE)]>\n                </td>\n                </tr>\n                </table>\n                <![endif]-->\n            </td>\n        </tr>\n        <tr>\n            <td bgcolor="#e5e5e5" align="center" style="padding: 0px 10px 0px 10px;">\n                <!--[if (gte mso 9)|(IE)]>\n                <table align="center" border="0" cellspacing="0" cellpadding="0" width="600">\n                <tr>\n                <td align="center" valign="top" width="600">\n                <![endif]-->\n                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">\n    <tr>\n        <td bgcolor="#e5e5e5" align="center" style="padding: 30px 30px 15px 30px; color: #747474; font-family: \'Lato\', Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px;">\n            <p style="margin: 0;">\n                                    This email was sent to <a href="mailto:nelliehopkinssj@aol.com" style="color: #747474; font-weight: 700;" name="link1">nelliehopkinssj@aol.com</a>.\n                                                                                                                                                                                                                                                                                                \n              \t \n          \n          </p>\n        </td>\n    </tr>\n    <tr>\n        <td bgcolor="#e5e5e5" align="center" style="padding: 0px 30px 15px 30px; color: #747474; font-family: \'Lato\', Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px;">\n            <p style="margin: 0;">\n                                    To ensure that you continue to receive important updates and newsletters, please add <a href="mailto:noreply@account.stripchat.com" style="color: #747474; font-weight: 700;" name="link19_21">noreply@account.stripchat.com</a> to your safe-senders list.\n                                                                                                                                                                                                                                                                                                 \n              \t\n          \n          </p>\n        </td>\n    </tr>\n    <tr>\n        <td bgcolor="#e5e5e5" align="center" style="padding: 0px 30px 30px 30px; color: #747474; font-family: \'Lato\', Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px;">\n            <p style="margin: 0;">\n                                    <a href="http://trk.account.stripchat.com/20ce7e2df82250a3/T1AjZnnAUdbBPrcQKQDZmWjXDm6atzpezFeMvQBfy1d7aXTeGs5JUAa4Wv6TmKSaYGbxGjTwytSKeNNMEvDKg4eomZLGoUKHigC48vYgAbocTjaM2u3BGoaKUJYWYy1RVn89ihyBpWEfdAgp5eV2Vb3gZh4EPZZ9f8M55S8vRcAd3DAQcz9fjUQw66gZxaUic8zs6B35ZKg6nmTrGTyZow2NpKMKKPqNNBZ66TJhpG3fR57b82LZUJBBB8fUTmNM7yzBTZE6cu5wXy8ry4nDFBg5tUmVhbaLT3Qf5HPiumrqVzEJq8NXW4759962D" style="color: #747474; font-weight: 700;" name="link37">Terms of Use</a> | <a href="http://trk.account.stripchat.com/91254a0f7978d497/T1AjZnnAUdbBPrcQKQDZmWjXDm6atzpezFeMvQBfy1d7aXTeGs5JUAa4Wv6TmKSaYGbxGjTwytSKeNNMEvDKg4eomZLGoUKHigC48vYgAbocTjaM2u3BGoaKUJYWYy1RVn89ihyBpWEfdAgp5eV2Vb3gZh4EPZZ9f8M55S8vRcAd3DAQcz9fjUQw66gZxaUic8zs5VwHPjT5jdMcCPmAemYGiF7atqz9Tq8yav1A8uWRVxqc6E1BAWCQjReVymkZvMjGq4SkLqzMqVFbKpTu9a2pxmL3FSXqVs1a9Gv4hsTcnemswkXYR91mXp2X1" target="_blank" style="color: #747474; font-weight: 700;" name="link38"><unsubscribe>Unsubscribe</unsubscribe></a>\n                                                                                                                                                                                                                                                                                                             \n          \t\t\n          </p>\n        </td>\n    </tr>\n</table>\n                    <!--<a href="http://trk.account.stripchat.com/0f67179622019239/T1AjZnnAUdbBPrcQKQDZmWjXDm6atzpezFeMvQBfy1d7aXTeGs5JUAa4Wv6TmKSaYGbxGjTwytSKeNNMEvDKg4eomZLGoUKHigC48vYgAbocTjaM2u3BGoaKUJYWYy1RVn89ihyBpWEfdAgp5eV2Vb3gZh4EPZZ9f8M55S8vRcAd3DAQcz9fjUQw66gZxaUic8zs6xEs1q5hHGxJacqgURvdk212VznZFvSCp3tmsVu6CrmS1gJnrwq94DfiBmWkM4kc8MeGNfNNhTt96M92rGFAkPxz55TfQzZPvKnarPQSyRJao77HJv2EkUgp1" target="_blank" style="color: #747474; font-weight: 700;" name="link3"><unsubscribe>Unsubscribe</unsubscribe></a>-->\n                <!--[if (gte mso 9)|(IE)]>\n                </td>\n                </tr>\n                </table>\n                <![endif]-->\n            </td>\n        </tr>\n    </table>\n    <img alt="" src="http://trk.account.stripchat.com/75d410c07/0a6a40734f303495/pq2txs8xHA2oSejwqcw8CsRWmsLXERVxapHfJqr8qS5cJbL7nSWMdp3kbrHqA4yHBsFhqzXjeGehnBHoUMvsUbYb4d3uymbX7nAopKbtNZ8p84pbFf3QFrQGzyNpVnQ46BS6pLhKg5bpquqD55cNirmt8nWKw5M78PErwio46CZwthKymZvsGsZiQntTrkxjPWr3XYS3i991LdLDw5SSW1vQvETbP7oknoj9NCGTW8Hxv7d8aosK13L3gQmGC2CHfHGTzYfUvzWhMr7bFvFaufd6V5eTewYh4A62JvcV4svGRcpzG5AA6p7vbfAAqWh2pUdhT8Khop48XgLKRfa2JGVsDST1d9gAkefK4kyZxvyAQ4oyRKUU3eegs4FY36YPTzUempMNxAJMsSk9T8mHaCoNvVDC6ejbZTLpLEWCGdL1qfGr6ZEhc4RYrkX85jXwMd51gjgSUR9pmAvVYy5nG5V3FS4XvSasz2j88mDMSRVf" width="4" height="4" border="0" />\n    <img alt="" src="http://trk.account.stripchat.com/75d410c07/0926edc4898a3194/2QLfSLk37iyomu3sRujakf6YbGYPakzQAHbeUNBPiDkt6zs8SHQ4zAdPzcA1WfgXzeDPr8G3SRvPWGxpPoXM7nh3M52f99XUMRBQYjxBD2LL6Pxms3GjokB9d3JxE7nqRGJMWm2NUyVpHa2WXvhvyNLs7LPaEFjhUKschkqpmi1JmT1UAksFmGoD1B3K6x9niJRGMLWJH4Rc8XcjVGrhFzDJguEDisdHpMTKviv763bpH8NZXY26ayqXiPdLeoz8DtMRysC8VaWhatvgQZ9S2R5vFmNpufRyeDrVMedomjo7PB3E4hgdAmG8Rcb1Auu4pq1PCqTyKmFcU5qUGKMt6JYkqUoQU3non2ibLwhQD6Ce4rFWwgu3cWpFYvySX4ZTJnGsHAihCJnYsm9oCLopKuU98Wkvwjz83gg2BJbyhq7YnPyWLn76cs" width="4" height="4" border="0" />\n</body>\n</html>'])]    
    '''
    # link = 'Receive Your Password and Confirm Your Email\nAUXE8zwGQ$\n\nConfirm Your Email\nhttp://trk.email.supportlivecam.com/f52f4d8f0f996609/3XQcGTqXZ2Td6ed6H58qxomrVUnb3CaPDoYJUx2jgiKHxN7xaA51u9Vyq6q3U2vcTx2nB4PioyyTHHGGB6D49B1PH2r8NL4g1UDVWHAQNNVUHubEatipXXwFES9NR3WdGz4ER5nemvtCFL4KJpW6QkYXZFgoqMefQ46VMmeSZqwpv91hatjsqU554AMFQzP7f4Qbq2YWV15hh3XXMeCSpUuaX6tWianZvvi5DLeZU17zQADbXJD7SkHceUtKQ1r5kyMeNtbSBGoCarzM4fjrcPVriVV3FBmAbbARTyvxjgLB4cjcLTZPGvEMvQ5KxLPyL6iKXZ9zdpXUBu4EAsw3gn7m8rru7wUMpdp4D2nBsGS529vBDkEUwpq8Ka5bGRTS1vLdTXCt3CBDQSqLzW5EpxuhS7jUjiHA\n\nBy clicking on the link you give us the confirmation of your registration and that you are at least 18 yo (21 for the USA). You`ll be automatically subscribed to the system and promotional newsletters from superchatlive. You can unsubscribe at any time and we'
    pattern = r'.*?Confirm Your Email.*?(http://trk.account.stripchat.com/[0-9a-zA-Z]{1,30}/[0-9a-zA-Z]{1,1000})By clicking on the link'
    # pattern = r'.*?Confirm Your Email.*?(http://trk.account.stripchat.com/[0-9a-zA-Z]{1,30}/)By clicking on the link'

    # pattern = r'.*?(http://trk.email.supportlivecam.com/[0-9a-zA-Z]{1,30}/[0-9a-zA-Z]{1,1000})'    
    link2=re.compile(pattern)
    link = link2.findall(link)
    print(link)

def active_test():
    plans = db.read_plans(-1)
    submits = db.get_cookie(plans[0])
    submit = submits[0]
    submit['Email'] = {}
    submit['Email']['Email_Id']= submit['Email_Id']    
    chrome_driver = Chrome_driver.get_chrome(submit)
    print(submits[0])
    activate(submit,chrome_driver)

if __name__=='__main__':
    charge()


