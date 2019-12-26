import Dadao
from selenium import webdriver
from selenium.webdriver import ActionChains
import json
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
import db
import selenium_funcs
import Submit_handle
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


'''
GETAROUND
Auto
'''



def web_submit(submit,chrome_driver,debug=0):
    # test
    # https://www.cam4.com/
    # cookies = get_account(submit)
    # chrome_driver.get('https://www.google.com')
    # sleep(1)
    # print('stop')
    # while True:
    #     url = chrome_driver.current_url 
    #     print(url)
    #     if 'account.blizzard.com' in url :
    #         chrome_driver.execute_script("window.stop();") 
    #         print('stop')
    #         break
    #     else:
    #         sleep(0.5)
    # chrome_driver.delete_all_cookies()
    # for cookie in cookies:
    #     if 'expiry' in cookie:
    #         cookie['expiry'] = int(cookie['expiry']) +86400
    #     chrome_driver.add_cookie(cookie)  
    # print('After add cookie') 
    # cookies = chrome_driver.get_cookies()    
    # print('cookies',cookies)    
    # chrome_driver.get('https://account.blizzard.com/')  
    sleep(3)   
    xpath_payment = '//*[@id="app"]/main/section[1]/div/ul/li[7]/a'    
    print(xpath_payment)
    try:
        chrome_driver.find_element_by_xpath(xpath_payment)
    except:
        chrome_driver.refresh()
    flag_info = 0
    while True:
        chrome_driver.switch_to.default_content()
        for j in range(10):
            sleep(3)   
            chrome_driver.find_element_by_xpath(xpath_payment).click()
            print('click payment method')        
            for i in range(10):
                try:
                    a = chrome_driver.find_element_by_class_name('mt-card-top')
                    print(a)
                    element = a.find_element_by_tag_name('a')
                    print(element)
                    element.click()
                    print('find and click add a new payment method')
                    break
                except Exception as e:
                    print(str(e))
                    print('find not add a new payment method')                    
                    sleep(3)
            sleep(5)
            for i in range(10):
                try:
                    chrome_driver.find_element_by_class_name('btn-primary').click()
                    print('find and click continue button')
                    break
                except:
                    print('find not continue button')                    
                    sleep(3)
            for i in range(5):
                try:
                    chrome_driver.switch_to_frame('wallet-app-iframe')
                    element = chrome_driver.find_element_by_xpath('//*[@id="firstName"]')
                    flag_info = 1
                    print('Find info page')
                    break
                except Exception as e:
                    print(str(e))
                    print('Does not find info page,',i)
                    sleep(3)
            if flag_info !=1:
                print('Does not Find info page')
                chrome_driver.refresh()
                break
            else:
                print('Find info page')                
                break
        if flag_info != 1:
            print('Does not find info page !!!!!!!!!!')
            continue
            # chrome_driver.close()
            # chrome_driver.quit()
            # return
        info = []
        for i in range(6):
            a = get_info()
            info.append(a)
        print(info)
        chrome_driver.find_element_by_xpath('//*[@id="firstName"]').send_keys(info[0])        
        chrome_driver.find_element_by_xpath('//*[@id="lastName"]').send_keys(info[1])
        chrome_driver.find_element_by_xpath('//*[@id="addressLine1"]').send_keys(info[2])
        chrome_driver.find_element_by_xpath('//*[@id="city"]').send_keys(info[3])
        chrome_driver.find_element_by_xpath('//*[@id="region"]').send_keys(info[4])
        chrome_driver.find_element_by_xpath('//*[@id="postalCode"]').send_keys(info[5])
        sleep(2)
        chrome_driver.find_element_by_xpath('/html/body/app-root/div/div/app-address-selection/div/app-actions-with-cancel/div/button[1]').click()
        sleep(5)  
        # detect heads up flag
        try:
            path_flag = '/html/body/app-root/div/div/app-init-token-error/div/div[2]/h5'                                                    
            chrome_driver.switch_to.default_content() 
            chrome_driver.switch_to_frame('wallet-app-iframe')                
            if account_ban_info in chrome_driver.page_source:
                print('Find account ban text')                        
                flag_account_ban = 1
                chrome_driver.quit()
                chrome_driver.close()
                return
            else:
                print('Find not account ban text')  
        except:
            pass      
        # chrome_driver.switch_to.default_content()
        flag_card = 0
        for i in range(6):
            try:
                # element = chrome_driver.find_element_by_class_name('js-iframe')
                # chrome_driver.switch_to_frame(element)
                chrome_driver.find_element_by_xpath('/html/body/app-root/div/div/app-collect-payment-adyen/div/div/form/div[2]/h4')
                print('Find card info to input after send info')
                flag_card = 1
                break
            except:
                print('No card info to input after send info')
                sleep(3)                
        if flag_card == 0:
            chrome_driver.refresh()
            continue
            # print('No card info to input after send info')
            # chrome_driver.close()
            # chrome_driver.quit()
            # return
        while True:
            submit,path,workbook = get_data()
            submit['status'] = 'badname'
            for i in submit['badname']:
                submit['row'] = i
                Dadao.write_status(path,workbook,submit,'badname')              
            card = submit['card_number'].replace('\t','').split('.')[0]
            card = str(card)
            month = submit['month'].replace('\t','').split('.')[0]
            month = str(month)
            year = submit['year'].replace('\t','').split('.')[0]
            year = str(year)            
            cvv = submit['cvv'].replace('\t','').split('.')[0]
            cvv = str(cvv)
            if len(month) == 1:
                month = '0' + month
            if len(year) != 2:
                year = year[-2:]
            month = month+year
            if len(cvv) == 1:
                cvv = '00'+ cvv
            elif len(cvv) == 2:
                cvv = '0' + cvv
            flag_visa = 0
            try:
                path_cardtype = '//*[@id="paymentoptionslist"]/li[3]/form/button'
                chrome_driver.switch_to.default_content() 
                chrome_driver.switch_to_frame('wallet-app-iframe')                
                chrome_driver.switch_to_frame('token-payment-iframe')                 
                chrome_driver.find_element_by_xpath(path_cardtype).click()
                flag_visa = 1
                print('Find visa select button')
            except:
                print('Find not visa select button')
            for i in range(60): 
                flag_wait = 0               
                chrome_driver.switch_to.default_content()
                chrome_driver.switch_to_frame('wallet-app-iframe')
                if flag_visa == 1:
                    chrome_driver.switch_to_frame('token-payment-iframe')                 
                if 'Card Number' in chrome_driver.page_source:
                    if 'Please wait while we take care of some business.' not in chrome_driver.page_source:
                        flag_wait = -1
                        path_card = '//*[@id="encryptedCardNumber"]'
                        path_day = '//*[@id="encryptedExpiryDate"]'
                        path_cvv = '//*[@id="encryptedSecurityCode"]'
                        path_button = '/html/body/app-root/div/div/app-collect-payment-adyen/div/div/form/div[2]/div/app-actions-with-cancel/div/button[1]'
                        print('Find card Number')  
                        sleep(5)                  
                        try:
                            xpath = path_card
                            if flag_visa == 0:
                                elements_iframe = switch_iframe_(chrome_driver,xpath) 
                            else:
                                elements_iframe = switch_iframe_visa(chrome_driver,xpath)
                            element = chrome_driver.find_element_by_xpath(path_card)
                            element.clear()
                            element.send_keys(card)
                            break
                        except Exception as  e:                                                   
                            print(str(e))
                            path_card = '//*[@id="cardNumber"]'
                            path_day = '//*[@id="expiryDate"]'
                            path_cvv = '//*[@id="cvv"]'
                            path_button = '//*[@id="primaryButton"]' 
                            card_name = '//*[@id="cardholderName"]'                  
                            xpath = path_card   
                            try:             
                                if flag_visa == 0:
                                    elements_iframe = switch_iframe_(chrome_driver,xpath) 
                                else:
                                    elements_iframe = switch_iframe_visa(chrome_driver,xpath)
                                element = chrome_driver.find_element_by_xpath(path_card)
                                element.clear()
                                element.send_keys(card)
                                break
                            except:
                                pass
                    else:
                        flag_wait += 1
                        sleep(3)
                        if flag_wait >= 10:
                            break
                else:
                    print('Find not card Number')
                    sleep(3)
            if flag_wait != -1:
                chrome_driver.refresh()
                break
            # expiryDate
            chrome_driver.switch_to.parent_frame()
            chrome_driver.switch_to_frame(elements_iframe[1])
            # switch_iframe(chrome_driver,path_day)              
            element = chrome_driver.find_element_by_xpath(path_day)
            element.clear()
            for num in month:
                element.send_keys(int(num))
            #cvv
            chrome_driver.switch_to.parent_frame()
            chrome_driver.switch_to_frame(elements_iframe[2])            
            # switch_iframe(chrome_driver,path_cvv)              
            element = chrome_driver.find_element_by_xpath(path_cvv)
            element.clear()
            element.send_keys(cvv)
            name = submit['firstname'] + ' ' + submit['lastname']
            try:
                switch_iframe(chrome_driver,card_name)              
                element = chrome_driver.find_element_by_xpath(card_name)
                element.clear()
                element.send_keys(name)
            except:
                sleep(1)            
            sleep(2)
            # button
            chrome_driver.switch_to.parent_frame()
            # chrome_driver.switch_to_frame(elements[1])            
            # switch_iframe(chrome_driver,path_button)   
            chrome_driver.find_element_by_xpath(path_button).click() 
            # writelog(chrome_driver,submit)
            flag_error = 0
            flag_success = 0
            flag_account_ban = 0
            error_info = 'An error occurred.'
            success_info = 'Payment method successfully added'
            account_ban_info = 'Heads up!'
            sleep(5)
            # try:
            #     element = chrome_driver.find_element_by_xpath(path_cvv)
            #     print('text in cvv:',element.text)

            # except:
            #     pass
            for i in range(2):
                '''
                fail
                '''
                try:
                # if error_info in chrome_driver.page_source:
                    path_flag = '//*[@id="app"]/main/section[2]/div/div[2]/div[1]/div[2]/ul/li/span'
                    switch_iframe(chrome_driver,path_flag)                          
                    element = chrome_driver.find_element_by_xpath(path_flag)
                    if element.text == error_info:
                        print('Find fail text')
                        flag_error = 1
                # else:
                except:
                    print('Find not fail text')
                sleep(2)
                '''
                success
                '''
                try:
                # if success_info in chrome_driver.page_source: 
                    chrome_driver.switch_to.default_content()
                    element = chrome_driver.find_element_by_class_name('success-title')
                    print(element.text)
                    print('Find success text')                        
                    flag_success = 1
                    flag_error = 0
                    break
                # else:
                except:
                    print('Find not success text')
                '''
                ban
                '''
                try:
                    # if account_ban_info in chrome_driver.page_source:    
                    path_flag = '/html/body/app-root/div/div/app-init-token-error/div/div[2]/h5'                                                    
                    chrome_driver.switch_to.default_content() 
                    chrome_driver.switch_to_frame('wallet-app-iframe')                
                        # switch_iframe(chrome_driver,path_flag)                                                                  
                        # element = chrome_driver.find_element_by_xpath(path_flag)
                    if account_ban_info in chrome_driver.page_source:
                        print('Find account ban text')                        
                        flag_account_ban = 1
                    else:
                        print('Find not account ban text')
                    if flag_error == 0 and flag_success == 0 and flag_account_ban == 0:
                        print('Find none of success, fail or account ban info')
                        sleep(3)
                    else:
                        break
                except Exception as e:
                    print(str(e))
            if flag_wait != -1:
                continue
            if flag_error == 1:
                '''
                fail
                '''
                print('Find fail info')
                if flag_account_ban == 1:
                    print('Account ban')
                    chrome_driver.close()
                    chrome_driver.quit()
                    return
                Dadao.write_status(path,workbook,submit,error_info)
                # path_card = '//*[@id="encryptedCardNumber"]'
                # path_day = '//*[@id="encryptedExpiryDate"]'
                # path_cvv = '//*[@id="encryptedSecurityCode"]'
                # # path_button = '//*[@id="encryptedSecurityCode"]'

                # try:
                #     sleep(2)
                #     switch_iframe_(chrome_driver,path_card)                                              
                #     chrome_driver.find_element_by_xpath(path_card)
                # except:
                #     print('Does not Find card input xpath')
                #     path_cardtype = '//*[@id="paymentoptionslist"]/li[3]/form/button'
                #     switch_iframe(chrome_driver,path_cardtype)
                #     chrome_driver.find_element_by_xpath(path_cardtype).click()
                #     print('Find visa select button')
                #     path_card = '//*[@id="cardNumber"]'
                #     path_day = '//*[@id="expiryDate"]'
                #     path_cvv = '//*[@id="cvv"]'
                #     path_button = '//*[@id="primaryButton"]'
                #     card_name = '//*[@id="cardholderName"]' 
                #     name = submit['firstname'] + ' ' + submit['lastname']
                #     for i in range(30):
                #         try:
                #             switch_iframe(chrome_driver,card_name)
                #             chrome_driver.find_element_by_xpath(card_name).send_keys(name)
                #             # chrome_driver.switch_to.default_content()
                #             break
                #         except:
                #             sleep(1)
            elif flag_success == 1:
                # success
                print('Find success info')
                Dadao.write_status(path,workbook,submit,success_info)
                break
            elif flag_account_ban == 1:
                # account ban
                print('Find account ban info!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                chrome_driver.close()
                chrome_driver.quit()
                return
            else:
                Dadao.write_status(path,workbook,submit,'No flag found')                
                print('Find none of success, fail or account ban info')
                break

def writelog(chrome_driver,submit):
    '''
    writelog and
    '''
    path = r'..\log'        
    makedir_account(path)        
    path_ = r'..\log\pics'        
    makedir_account(path_)
    pic_name = str(submit['Mission_Id'])+'_'+str(random.randint(0,100000))+'.png'
    pic = os.path.join(path_,pic_name)
    print(pic)
    try:
        chrome_driver.save_screenshot(pic)
        print('pic saved success')
    except Exception as e:
        print(str(e))


def change_iframe(iframe):
    if iframe == 'token-payment-iframe':
        iframe = 'wallet-app-iframe'
    else:
        iframe = 'token-payment-iframe'
    return iframe

def switch_iframe(chrome_driver,xpath):
    chrome_driver.switch_to.default_content()    
    try:
        chrome_driver.find_element_by_xpath(xpath)
        print('In default_content')        
        return chrome_driver
    except:
        print('Not In default_content')
        pass
    try:
        chrome_driver.switch_to_frame('wallet-app-iframe')            
        chrome_driver.find_element_by_xpath(xpath)
        print('In wallet-app-iframe')        
        return
    except:
        print('Not In wallet-app-iframe')
    elements = chrome_driver.find_elements_by_class_name('js-iframe')
    print(elements)
    for element in elements:
        chrome_driver.switch_to_frame(element)    
        try:
            chrome_driver.find_element_by_xpath(xpath)
            print('In iframe :',element)            
            return elements
        except:
            chrome_driver.switch_to.parent_frame()
            print('Not In iframe :',element)

def switch_iframe_(chrome_driver,xpath):
    chrome_driver.switch_to.default_content()    
    try:
        chrome_driver.switch_to_frame('wallet-app-iframe')            
        elements = chrome_driver.find_elements_by_class_name('js-iframe') 
        print(len(elements),'elements')   
        for element in elements:
            chrome_driver.switch_to_frame(element)    
            try:
                chrome_driver.find_element_by_xpath(xpath)
                print('Find iframe In wallet-app-iframe')            
                return elements
            except Exception as e:
                print(str(e))
                chrome_driver.switch_to.parent_frame()
                print('Not In iframe :',element)
    except Exception as e:
        print(str(e))

def switch_iframe_visa(chrome_driver,xpath):
    chrome_driver.switch_to.default_content()    
    try:
        chrome_driver.switch_to_frame('wallet-app-iframe')  
        chrome_driver.switch_to_frame('token-payment-iframe')          
        elements = chrome_driver.find_elements_by_class_name('js-iframe') 
        print(len(elements),'elements')   
        for element in elements:
            chrome_driver.switch_to_frame(element)    
            try:
                chrome_driver.find_element_by_xpath(xpath)
                print('Find iframe In wallet-app-iframe')            
                return elements
            except Exception as e:
                print(str(e))
                chrome_driver.switch_to.parent_frame()
                print('Not In iframe :',element)
    except Exception as e:
        print(str(e))




def get_account(submit):
    path = select_account(submit)
    with open(path,'r') as f:
        cookie_str = f.readlines()
    print(cookie_str)
    cookies = json.loads(cookie_str[0])
    return cookies

def remove_account(file):
    os.remove(file)

def select_account(submit):
    path_country = r'..\res\cookies\US'
    modules = os.listdir(path_country)
    # print(modules)
    modules_path = [os.path.join(path_country,file) for file in modules]
    return modules_path[0]

def get_info():
    a = 'abcdefghijklmnopqrstuvwxyz'
    length = random.randint(4,8)
    b = []
    for i in range(length):
        c = random.randint(0,len(a)-1)
        b.append(a[c])
    print(b)
    d = ''
    for i in b:
        d += i
    print(d)
    return d

def test1():
    with open('1.txt','r') as f:
        cookie_str = f.readlines() 
    print(cookie_str[0])
    return cookie_str[0]    

def test(chrome_driver):
    submit = get_data()[0]
    print(submit)
    print(type(submit))
    submit['Mission_Id'] = 11002
    submit['Country'] = 'US'
    # submit['ua'] = data['ua']
    # chrome_driver = Chrome_driver.get_chrome(submit,pic=1)
    web_submit(submit,chrome_driver)

def get_data():
    path = r'..\res\Dadao.xlsx' 
    sheet,workbook = Dadao.get_excel(path)   
    Mission_Id = 11001 
    submit = Dadao.get_one_data(sheet,Mission_Id)
    print(submit)
    submit['Mission_Id'] = Mission_Id
    return submit,path,workbook    

if __name__=='__main__':
    test()
