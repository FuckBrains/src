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
import Submit_handle


'''
flirtforfree(Done)
'''


def web_submit(submit,debug=0):
    if debug == 1:
        # site = 'http://track.meanclick.com/im/click.php?c=9&key=4ld1iyw2l4iwy1u0k4n8hn1c'
        site = 'https://track.advendor.net/click?pid=27543&offer_id=852'
        submit['Site'] = site   
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    # sleep(2000)
    name = name_get.gen_one_word_digit(lowercase=False)      
    pwd = Submit_handle.password_get()
    chrome_driver.find_element_by_xpath('//*[@id="cemail"]').send_keys(submit['Email']['Email_emu'])
    chrome_driver.find_element_by_xpath('//*[@id="nick_name"]').send_keys(name)
    chrome_driver.find_element_by_xpath('//*[@id="new_password"]').send_keys(pwd)
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="term_and_cond"]').click()
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="registration_form"]/div/input').click()
    sleep(2000)






    # chrome_driver.maximize_window()
    # chrome_driver.refresh()    
    # sleep(2000)  
    # 'https://creative.strpjmp.com/LPExperience/?action=signUpModalDirectLinkInteractive&campaignId=66a29c1c25bce64b38c92f4bcf56b4e21e619817ab1aab514ce8203143a60a47&creativeId=703743f02fd260bf1c2309c89b9ebf898145c006091f4ce79fe9822a73fddf22&domain=stripchat&exitPages=LPSierra%2CLPSierra%2CLPAkira&memberId=D-602781-1564542573-bjuOIMY723549&modelName=EvyDream&shouldRedirectMember=1&sourceId=&userId=32976296468dd516e6deecdb98dd5a54eee16e2ef856a243a1eb8e54921f0f03'
    if 'creative.strpjmp.com' in chrome_driver.current_url:
        try:
            chrome_driver.find_element_by_xpath('/html/body/div/div[2]/header/div/div/nav[1]/div[1]/a').click()
        except:
            pass
    chrome_driver.find_element_by_xpath('//*[@id="body"]/div/div/header/div/div/nav[2]/div[3]/a[2]').click()
    sleep(5)
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
    sleep(10)
    try:
        chrome_driver.find_element_by_xpath('//*[@id="body"]/div/div/div[1]/span')
    except:
        a_name = ['a','b','c','d','e','f','g','h','i','j','k','l','a','b','c','d','e','f','g','h','i','j','k','l']
        num_name = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9]
        num_insert = random.randint(2,len(name))
        # print(name[0:num_insert] )
        name_3 = random.randint(0,10)
        first_insert = a_name[name_3]+str(num_name[name_3])
        name = name[0:num_insert]+ first_insert+ str(num_name[num_insert])+name[num_insert:-1]+a_name[num_insert]
        print(name)
        chrome_driver.find_element_by_xpath('//*[@id="sign_up_input_login"]').send_keys(name)
        sleep(2)
        chrome_driver.find_element_by_class_name('btn-login').click()
        print('Jump2')

    # try:
    #     chrome_driver.find_element_by_css_selector('#sign_up_input_email')
    #     print('get site but fail to register',str(e))
    #     chrome_driver.close()
    #     chrome_driver.quit()  
    #     return 0       
    # except Exception as e:
    #     print('regester success')
        
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
        sleep(50)        
    else:
        chrome_driver.close()
        chrome_driver.quit()
        return         
    handles=chrome_driver.window_handles   
    try:
        for i in handles:
            if i != handle:
                chrome_driver.switch_to.window(i)
                if 'Email successfully confirmed' not in chrome_driver.page_source:
                    chrome_driver.refresh()
                else:
                    try:
                        chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(submit['Email']['Email_emu_pwd'])
                        sleep(2)
                        chrome_driver.find_element_by_xpath('//*[@id="confirmPassword"]').send_keys(submit['Email']['Email_emu_pwd'])
                        sleep(2)
                        chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/form/div[4]/button').click()
                        sleep(5)
                    except Exception as e:
                        print('',str(e))
                        chrome_driver.close()
                        chrome_driver.quit()    
                        return                          
    except Exception as e:
        print('',str(e))
        chrome_driver.close()
        chrome_driver.quit()    
        return  
    if 'Password was updated successfully' in chrome_driver.page_source:
        try:
            chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/a').click()
        except:
            chrome_driver.close()
            chrome_driver.quit()    
            return              
    sleep(5)
    try:
        chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/div[3]/div[7]/div/a').click()
    except:
        chrome_driver.close()
        chrome_driver.quit()
        return
    sleep(30)        
    chrome_driver.close()
    chrome_driver.quit()
    return 

def email_confirm(submit):
    print('----------')
    for i in range(1):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']
            title = ('Complete Your Sign Up Process','confirm@vs3.com')
            pattern = r'.*?Confirm Your Account.*?(https://u10352769.ct.sendgrid.net/wf/click\?upn=.*?)">Please Confirm Your Account'
            url_link = emaillink.get_email(name,pwd,title,pattern,True,debug = 0)
            if 'http' in url_link :
                break            
        except Exception as e:
            print(str(e))
            print('===')
            pass
    return url_link

def activate():
    # site_url = 'https://stripchat.com'
    site_url = 'https://cpx24.net/dashboard/campaigns'
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get(site_url)
    print('stripchat....................')
    sleep(3000)
    




    

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



if __name__=='__main__':
    submit = {'Email': {'Email_Id': '6f89149b-aa34-11e9-aecd-0003b7e49bfc', 'Email_emu': 'KentSawyer1v@outlook.com', 'Email_emu_pwd': 'NhG0punx', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}    
    # submit = db.get_one_info()
    # print(submit)
    # web_submit(submit,1)
    link = email_confirm(submit)
    print('=============')
    print(link)
    # submit ={'Email': {'Email_Id': '702d538c-aa34-11e9-b468-0003b7e49bfc', 'Email_emu': 'SextonJoyners3@aol.com', 'Email_emu_pwd': 'QgyTOY0y', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}
    # submit= {'Email': {'Email_Id': '6fdec625-aa34-11e9-9489-0003b7e49bfc', 'Email_emu': 'CarrieBrookso7@aol.com', 'Email_emu_pwd': 'Bh9ZbPOR', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}
    # submit = {'Email': {'Email_Id': '6faf2a9d-aa34-11e9-b0fa-0003b7e49bfc', 'Email_emu': 'AnnieBestKw@aol.com', 'Email_emu_pwd': 'BBI2C6Tq', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}
    # submit = {'Email': {'Email_Id': '702fb4ec-aa34-11e9-a0a1-0003b7e49bfc', 'Email_emu': 'FredaHarlanaVmQyE@yahoo.com', 'Email_emu_pwd': 'uCPQ22t41', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}
    # url_link=email_confirm(submit)
    # print(url_link)
    # test_email()