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



def web_submit(submit,debug=0):
    if debug == 1:
        site = 'http://im.datingwithlili.com/im/click.php?c=17&key=u1gl040n0ryvgu3ql04305kz'
        submit['Site'] = site   
    chrome_driver = Chrome_driver.get_chrome(submit)
    chrome_driver.get(submit['Site'])
    chrome_driver.maximize_window()
    chrome_driver.refresh()    
    name = name_get.gen_one_word_digit(lowercase=False)  
    # sleep(2000)  
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
    except Exception as e:
        print('',str(e))
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
            title = ('Email Verification', 'noreply@email.stripchat.com')
            pattern = r'.*?(http://trk.account.stripchat.com/[0-9a-zA-Z]{1,30}/[0-9a-zA-Z]{1,500})'
            url_link = emaillink.get_email(name,pwd,title,pattern)
            # if 'Bad' in url_link:
            #     print('Get duplicated email')
            #     url_link = emaillink.get_email(name,pwd,title,pattern,True)
            if 'http' in url_link :
                break
        except Exception as e:
            print(str(e))
            print('===')
            pass
    return url_link






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
    a = 'http://trk.account.stripchat.com/3ac6bd6b8910fb48/5v5QRb5xWpteoMiYXE3qKpiJXFcswUA2hrABRv9u4ToQ4f2t8iDA95RCkrh1yCp1kndGZwetmgrNsjyrUo2TvnKR9dicfHBaqhrFttW8emLX88BhbjKuMVcdU1k48NeaRvN5Qf3HiVuBvsTdLtwMPbPKu2iaqdYc5HhmmzJgGaz8uia9g3m22ugt7f6k28pt64Z1DUxdaWNteVLY9d6YvWjCVCCNVJCEGDwMTKwPhdmxNd4RucA8SmAGQVRoNHSXA7zn22f7gxSPHnCw1zGsQQCAXshEUiPGcECGqMXovysgFfhPe2FsLJeXg8XjENHeHXhsGq4jnJd3MMk8KTdTNJpqoaTpw12iUifJrU7vAsRCxANCeeiKk8DCUfhyrNv5u55nsfoNKTJLckkoKgoRrBy'
    b = 'http://trk.account.stripchat.com/2c5e55d17926b533/4JmKxRwf8JeRbb6yw8XDwxPZjXMu4mkQnyod1oiuUiamjtJsU4rou9wbB1X9SBVhjtA3SZciLtB5D7UPK7FRnvZ9MJkZPvvwdr6caAsi5k1TwPLasyrYGAMQ3NdnrtbfV2VoTya4fpDqB5XiULuxCubYbhr6cBBqx8nhQSvRhvEurhKJbsPzUAbdV4osy8XRp5mbh1mwRYNiT1BfoofkwgJn7k4xZjcx1GR7BKu2J3wNM8ANtaM4Azjv3AjSAbGHizQb3Lc6MtkkqtotDdnQd6pa3xcbmvUaQRKrX3J17ymDpD4qmQUx88ezpMoB244DZSsnLWdYiDVy5HMEsVQFPZTavv96BzSysfpnA4J2sF291cqToHgnu6aPa5Snxk7GhgRP7k4BrfQUREGTgZxDPPZNzdpoo4estkWF5wXnt6UZDgjHUpG3hBdzE54AzDqB7R81dbVcAMvJN6j8NiKgwBjQijFTvGG6raosRJAD55H4TQSsHepgMgVD1ZDKDUmmztL1BF5qdFiZXo3v6kzCUvKG4nkbqFpwqX749urWitbc2Z'
    link = b
    print(len(a),'fake')
    print(len(b),'real')
    pattern = r'.*?(http://trk.account.stripchat.com/[0-9a-zA-Z]{1,30}/[0-9a-zA-Z]{500,1000})'
    link2=re.compile(pattern)
    link = link2.findall(link)
    print(link)



if __name__=='__main__':
    # submit = db.get_one_info()
    # print(submit)
    # web_submit(submit,1)
    # submit= {'Email': {'Email_Id': '6fdec625-aa34-11e9-9489-0003b7e49bfc', 'Email_emu': 'CarrieBrookso7@aol.com', 'Email_emu_pwd': 'Bh9ZbPOR', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}

    submit = {'Email': {'Email_Id': '702fb4ec-aa34-11e9-a0a1-0003b7e49bfc', 'Email_emu': 'FredaHarlanaVmQyE@yahoo.com', 'Email_emu_pwd': 'uCPQ22t41', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}
    url_link=email_confirm(submit)
    print(url_link)
    # test_email()