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
    # chrome_driver.maximize_window()
    # chrome_driver.refresh()    
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
    for i in range(5):
        url_link = ''
        try:
            name = submit['Email']['Email_emu']
            pwd = submit['Email']['Email_emu_pwd']
            title = 'Please confirm your email'
            pattern = r'.*?(http://trk.email.supportlivecam.com/[0-9a-zA-Z]{1,30}/(\w){50,500})'
            url_link = emaillink.get_email(name,pwd,title,pattern)
            if 'Bad' in url_link:
                print('Get duplicated email')
                url_link = emaillink.get_email(name,pwd,title,pattern,True)
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
    link = 'asdhttp://trk.email.supportlivecam.com/de239e235c9a09b4/T3zEfBzZgDSLKMFQMzsantBEMVhNYTsVETtyVFR9mMv73NmNt2vVaLRGJ8DFVdzhZw9oRYX9DvCEfQGp3Tc3aA9HKd7JzbW9vNyHmq6hx67UacaSwi9fh6FW1XZojU1PN6p1evLt3hodSiwYQ9AhpzXHe57pU6evqoufP6GgA6qEBYCFs3QVuTfZu1CZndxByHwecWDLQSdVNjvT2ySkbcLxdETHxoMVpfaRFM8pmfxq39ruZFMRZ1j6Xds7vPtyoThK8vvef5THB1h2MCDob4eHWNwt6a4neKxRb7htYGEVkAR6zWUWXwz9x1pRrRNe3wcSDeWG8myaUaVcChB9HAxzKsyiD91JN4Es8v926jyCnvU4fsZVZXKre6b56aXiSeNnNdXpwWFG1VNpzfAzenzMwgojT5Cg5trvPLRAWL6fF9adSz3LNDDxQX98VbAnTZ4UBiS1dXg"'
    pattern = r'.*?(http://trk.email.supportlivecam.com/[0-9a-zA-Z]{1,30}/(\w){50,500})'
    link2=re.compile(pattern)
    link = link2.findall(link)
    print(link)



if __name__=='__main__':
    submit = db.get_one_info()
    print(submit)
    web_submit(submit,1)
    # submit= {'Email': {'Email_Id': '6fdec625-aa34-11e9-9489-0003b7e49bfc', 'Email_emu': 'CarrieBrookso7@aol.com', 'Email_emu_pwd': 'Bh9ZbPOR', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}

    # submit = {'Email': {'Email_Id': '702fb4ec-aa34-11e9-a0a1-0003b7e49bfc', 'Email_emu': 'RogerZimmerman1@aol.com', 'Email_emu_pwd': 'UbQ8Lxjv', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}}
    # url_link=email_confirm(submit)
    # print(url_link)
    # test_email()