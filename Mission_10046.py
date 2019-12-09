# https://www.roblox.com/?v=rc&rbx_source=3&rbx_medium=cpa&rbx_campaign=1820
# roblox
'''
Adsmain
roblox
Auto
'''

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
import db
import selenium_funcs
import Submit_handle
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json



def web_submit(submit,chrome_driver,debug=0):
    # predefine Mission
    Excel_tag = 'Auto'    
    num_html = 1
    Mission_Id = 10046

    if debug == 1:
        site = 'http://tracking.axad.com/aff_c?offer_id=181&aff_id=2138'
        submit['Site'] = site
    chrome_driver.get(submit['Site'])
    print('Load finish')
    old_page = chrome_driver.find_element_by_tag_name('html')
    print(old_page.id)

    # chrome_driver.maximize_window()    
    # chrome_driver.refresh()
    while True:
        page = get_page_by_flag(chrome_driver)
        if 'almost' in page:
            db.update_plan_status(1,submit['ID'])
        if 'finish' in page:
            db.update_plan_status(2,submit['ID'])
        print('Find target_page:',page['name'])
        if debug == 1:
            save_html(chrome_driver,Mission_Id,page)    
        eval(page['name'])(chrome_driver,submit)
        page_change(chrome_driver,page)




    sleep(3000)


    # Vehicle Year
    year = submit[Excel_tag]['year']
    if '1' in year or '2' in year:
        year = year.split('.')[0]
    else:
        year = str(random.randint(1991,2010))
    elem = '//*[@id="dropdown_vehicle_year"]'    
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,elem)))        
    sleep(2)        
    s1 = Select(chrome_driver.find_element_by_xpath(elem))
    s1.select_by_value(year)    
    sleep(3)  
    # button
    chrome_driver.find_element_by_xpath('//*[@id="vehicle_button"]').click()
    # sleep(5)

    # make
    elem_ = '//*[@id="dropdown_vehicle_make"]'    
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,elem_)))    
    sleep(2)        
    elem = chrome_driver.find_element_by_xpath(elem_)
    vehicle_row = submit[Excel_tag]['make']
    vehicle = vehicle_select(elem,vehicle_row)
    s1 = Select(elem)
    s1.select_by_value(vehicle)    
    sleep(3)
    # button
    chrome_driver.find_element_by_xpath('//*[@id="vehicle_make_button"]').click()
    # sleep(5)

    # Vehicle Model
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="dropdown_vehicle_model"]')))        
    sleep(2)        
    elem = chrome_driver.find_element_by_xpath('//*[@id="dropdown_vehicle_model"]')
    options = elem.find_elements_by_tag_name('option')
    num_model = random.randint(1,len(options)-1)
    s1 = Select(elem)
    s1.select_by_index(num_model)
    sleep(3)
    # button
    chrome_driver.find_element_by_xpath('//*[@id="vehicle_model_button"]').click()

    # # your vehicle57
    # chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/div[3]/div[1]/button').click()
    # sleep(3)

    try:
        # Trim
        WebDriverWait(chrome_driver,15).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="dropdown_vehicle_submodel"]')))
        sleep(2)    
        elem = chrome_driver.find_element_by_xpath('//*[@id="dropdown_vehicle_submodel"]')
        options = elem.find_elements_by_tag_name('option')
        num_model = random.randint(1,len(options)-1)
        s1 = Select(elem)
        s1.select_by_index(num_model)
        sleep(3)
        # button
        chrome_driver.find_element_by_xpath('//*[@id="vehicle_submodel_button"]').click()
        sleep(3)
    except:
        pass

    # your vehicle
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="plate-content"]/div[3]/div[1]/button')))    
    sleep(2)    
    chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/div[3]/div[1]/button').click()

    # No
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="plate-content"]/div[2]/div[1]/button')))    
    sleep(2)        
    chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/div[2]/div[1]/button').click()

    # No
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="plate-content"]/div[2]/div[1]/button')))        
    sleep(2)    
    chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/div[2]/div[1]/button').click()

    # 70%
    choice_list = ['//*[@id="plate-content"]/div[2]/div[1]/button','//*[@id="plate-content"]/div[2]/div[2]/button','//*[@id="plate-content"]/div[2]/div[3]/button']
    num_choice = random.randint(0,2)
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,choice_list[num_choice])))            
    sleep(2)        
    chrome_driver.find_element_by_xpath(choice_list[num_choice]).click()

    # 73%what is your credit rating
    credit_list = ['//*[@id="plate-content"]/div[2]/div[2]/button','//*[@id="plate-content"]/div[2]/div[3]/button','//*[@id="plate-content"]/div[2]/div[4]/button']
    num_choice = random.randint(0,2)
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,credit_list[num_choice])))    
    sleep(2)        
    chrome_driver.find_element_by_xpath(credit_list[num_choice]).click()
    sleep(10)

    # 76% are you currently married
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="plate-content"]/div[2]/div[1]/button')))        
    sleep(2)        
    num_choice = random.randint(0,1)
    if num_choice == 1:
        chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/div[2]/div[1]/button').click()
    else:
        chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/div[2]/div[2]/button').click()
    sleep(5)

    # 78%Aer you a homeowner
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="plate-content"]/h3')))        
    sleep(2)        
    chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/div[2]/div[2]/button').click()
    sleep(5)

    # 81 home insurance
    WebDriverWait(chrome_driver,60).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="plate-content"]/h3')))            
    sleep(2)        
    chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/div[2]/div[2]/button').click()


    # 83%What is your gender
    # text_to_be_present_in_element 
    WebDriverWait(chrome_driver,60).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="plate-content"]/div[1]'),'What is your gender?'))
    sleep(2)
    gender = ['//*[@id="plate-content"]/div[2]/div[1]/button','//*[@id="plate-content"]/div[2]/div[2]/button']
    num_choice = random.randint(0,1)
    chrome_driver.find_element_by_xpath(gender[num_choice]).click()

    # 85%What is your date of birth?
    birthday = Submit_handle.get_auto_birthday(submit['Auto']['dateofbirth'])
    mm = birthday[0]
    day = birthday[1]
    year = birthday[2]   
    WebDriverWait(chrome_driver,60).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="plate-content"]/div/div[1]'),'What is your date of birth?'))
    sleep(2)
    elem_month = '//*[@id="hinet-birth_month"]' 
    elem_day = '//*[@id="hinet-birth_day"]'
    elem_year = '//*[@id="hinet-birth_year"]'
    button = '//*[@id="plate-content"]/div/div[4]/div[1]/button'
    # mm
    s1 = Select(chrome_driver.find_element_by_xpath(elem_month))
    s1.select_by_value(str(mm)) 
    sleep(2)   
    # day
    chrome_driver.find_element_by_xpath(elem_day).send_keys(day)
    sleep(2)
    # year
    chrome_driver.find_element_by_xpath(elem_year).send_keys(year)
    sleep(2)
    # button
    chrome_driver.find_element_by_xpath(button).click()
    sleep(5)

    # 87%
    # text = ''
    # WebDriverWait(chrome_driver,60).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="plate-content"]/div/div[1]'),'What is your date of birth?'))
    elem = chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/h3')
    print('87% text')
    print(elem.text)
    chrome_driver,find_element_by_xpath('//*[@id="plate-content"]/div[2]/div[1]/button').click()

    # 89What is your current home address?
    flag = '//*[@id="plate-content"]/div[1]'
    text = 'What is your current home address?'
    elem_address = '//*[@id="hinet-autocomplete"]'
    elem_apt = '//*[@id="hinet-subpremise"]'
    elem_button = '//*[@id="plate-content"]/div[3]/div[1]/button'
    address = submit['Auto']['address']
    apt = Submit_handle.apt_get(address)
    WebDriverWait(chrome_driver,60).until(EC.text_to_be_present_in_element((By.XPATH,flag),text))
    sleep(2)
    chrome_driver.find_element_by_xpath(elem_address).send_keys(address)
    sleep(2)
    chrome_driver.find_element_by_xpath(elem_apt).send_keys(apt)
    sleep(1)
    chrome_driver.find_element_by_xpath(elem_button).click()

    # %91What is your name?
    # flag
    flag = '//*[@id="plate-content"]/div[1]'
    text = 'What is your name?'
    # elements
    elem_firstname = '//*[@id="hinet-fname"]'
    elem_lastname = '//*[@id="hinet-lname"]'
    elem_button = '//*[@id="plate-content"]/div[2]/div[3]/button'
    # data
    firstname = submit[Excel_tag]['firstname']
    lastname = submit[Excel_tag]['lastname']
    # execute
    WebDriverWait(chrome_driver,60).until(EC.text_to_be_present_in_element((By.XPATH,flag),text))
    sleep(2)    
    chrome_driver.find_element_by_xpath(elem_firstname).send_keys(firstname)
    sleep(2)
    chrome_driver.find_element_by_xpath(elem_lastname).send_keys(lastname)
    sleep(2)
    chrome_driver.find_element_by_xpath(elem_button).click()

    # %93What is your email?
    # flag
    flag = '//*[@id="plate-content"]/div[1]'
    text = 'What is your email?'
    # elements
    elem_email = '//*[@id="hinet-email"]'
    elem_button = '//*[@id="plate-content"]/div[2]/div[3]/button'
    # data
    email = submit[Excel_tag]['email']
    # execute
    WebDriverWait(chrome_driver,60).until(EC.text_to_be_present_in_element((By.XPATH,flag),text))
    sleep(2)    
    chrome_driver.find_element_by_xpath(elem_email).send_keys(email)
    sleep(2)
    chrome_driver.find_element_by_xpath(elem_button).click()

    # %93What is your email?
    # flag
    flag = '//*[@id="plate-content"]/div[1]'
    text = 'What is your email?'
    # elements
    elem_email = '//*[@id="hinet-email"]'
    elem_button = '//*[@id="plate-content"]/div[2]/div[3]/button'
    # data
    email = submit[Excel_tag]['email']
    # execute
    WebDriverWait(chrome_driver,60).until(EC.text_to_be_present_in_element((By.XPATH,flag),text))
    sleep(2)    
    chrome_driver.find_element_by_xpath(elem_email).send_keys(email)
    sleep(2)
    chrome_driver.find_element_by_xpath(elem_button).click()
    db.update_plan_status(1,submit['ID'])





    sleep(3000)  

def insurer_select(insurer):
    insurer_list = ['Allstate','Farmers','GEICO','LibertyMutual','Nationwide','Progressive','State Form','Travelers','USAA','Other']
    dir_list = ['//*[@id="plate-content"]/div[2]/div[1]/button','//*[@id="plate-content"]/div[2]/div[2]/button','//*[@id="plate-content"]/div[2]/div[3]/button']
    for i in range(len(insurer_list)):
        pass
    if insurer in insurer_list:
        num = insurer_list.index(insurer)
        dir_ = '//*[@id="plate-content"]/div[2]/div['+str(num+1)+']/button'
    else:
        dir_ = '//*[@id="plate-content"]/div[2]/div[10]/button'
    return dir_

def vehicle_select(elem,vehicle):
    vehicle_list = []
    for option in elem.find_elements_by_tag_name('option'):
        text_ = option.get_attribute("value") 
        if text_ != '-- Select Make --' and text_ != '':
            vehicle_list.append(text_)
    print(vehicle_list)
    if vehicle not in vehicle_list:
        num = random.randint(1,len(vehicle_list)-1)
        vehicle = vehicle_list[num]
    print('vehicle is :',vehicle)
    return vehicle

# def get_page_config():
#     Page_config = {
#     'page1':{
#         'flag'  :   {
#             'name'  :   'page1',
#             'xpath' :   '//*[@id="plate-content"]/h3',
#             'text'  :   'Do you have car insurance?'
#         },
#         'Step'  :   {
#             '1' :   {
#                 'Action' : 'Click'            
#                 'Config'   : {
#                     # general setting
#                     'general' :{
#                         'scroll' : True,                
#                         'try' : True,                    
#                         'xpath' : '//*[@id="plate-content"]/div[2]/div[2]/button',
#                     }

#                     'input_setting' : {
#                         'content' : '',
#                         'dynamic' : False,
#                     },
#                     'select_setting' : {
#                         #select general
#                         'selected_css' : '',                    
#                         'select_type' : 1,
#                         #1.select_by_index
#                         # 2.select_by_values
#                         # index_2
#                         'select_index' : 0,
#                         'select_index_rand' : True,
#                         # value_3
#                         'select_value' : 'email',                                        
#                         'select_value_range' : ['10','100'],
#                     },
#                     'slide' : {
#                         'x_move_min' : 10,
#                         'x_move_max' : 200,
#                         'y_move_min' : 0,
#                         'y_move_max' : 0
#                     }
#                 }
#             }
#         }
#     },
#     'page2':{
#         'name'  :   'page2',
#         'xpath' :   '//*[@id="plate-content"]/h3',
#         'text'  :   'How many Drivers do you want to insure?'        
#     },
#     'page3':{
#         'name'  :   'page3',    
#         'xpath' :   '//*[@id="plate-content"]/div[1]/div/h3',
#         'text'  :   'Vehicle Year'    
#     },
#     'page4':{
#         'name'  :   'page4',    
#         'xpath' :   '//*[@id="plate-content"]/div[1]/div/h3',
#         'text'  :   'Vehicle Make'    
#     },
#     'page5':{
#         'name'  :   'page5',    
#         'xpath' :   '//*[@id="plate-content"]/div[1]/div/h3',
#         'text'  :   'Vehicle Model'    
#     },  
#     'page6':{
#         'name'  :   'page6',    
#         'xpath' :   '//*[@id="plate-content"]/div[1]/div/h3',
#         'text'  :   'Vehicle Trim'    
#     },    
#     'page7':{
#         'name'  :   'page7',    
#         'xpath' :   '//*[@id="plate-content"]/div[1]/div/h3',
#         'text'  :   'Your Vehicles'    
#     },          
#     }    
#     return Page_config 

def get_page_by_flag(chrome_driver):
    print('Title:',chrome_driver.title)
    Page_config = get_page_config()
    target_page = None
    for page in Page_config:
        try:
            element = chrome_driver.find_element_by_xpath(Page_config[page]['xpath'])
            print(page,'find text:',element.text)
            if EC.text_to_be_present_in_element(element,Page_config[page]['text']):
                print('find target page:',page)
                target_page = Page_config[page]
                break
        except Exception as e:
            print(str(e))
            print(Page_config[page]['name'],'not found')
    if target_page == None:
        pass
    return target_page

def page_change(chrome_driver,page):
    WebDriverWait(chrome_driver,60).until_not(EC.text_to_be_present_in_element((By.XPATH,page['xpath']),page['text']))

def page1(chrome_driver,submit):   
    chrome_driver.find_element_by_xpath('//*[@id="plate-content"]/div[2]/div[2]/button').click()
    print('\n')

def page2(chrome_driver,submit):
    # insurer
    insurer = submit[Excel_tag]['alarm']
    insurer = insurer_select(insurer)
    print(insurer)
    chrome_driver.find_element_by_xpath(insurer).click()    
    print('\n')

def page3(chrome_driver,submit):
    # How many Drivers do you want to insure?
    elem = '//*[@id="plate-content"]/div[2]/div[1]/button'
    chrome_driver.find_element_by_xpath(elem).click()
    # sleep(10)

def save_html(chrome_driver,Mission_Id,page):
    print('Title',chrome_driver.title)
    print('url',chrome_driver.current_url)    
    path_html = r'..\html'
    file = str(page['name'])+'.html'
    path_folder = os.path.join(path_html,str(Mission_Id))
    Submit_handle.makedir_pic(path_folder)    
    path_file = os.path.join(path_folder,file)
    html=chrome_driver.page_source
    with open(path_file,mode="w",encoding="utf-8") as f:
        f.write(html)  

def test_c():
    page_config = get_page_config()
    content = json.dumps(page_config) 
    print(len(content))
    # print(type(content))
    submit = json.loads(content)
    print(submit)


def test():
    # db.email_test()
    # date_of_birth = Submit_handle.get_auto_birthday('')         
    Mission_list = ['10002']
    excel = 'Auto'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    print(submit)
    # [item for item in submit[excel] if submit[excel][item]!=None and submit[excel][item] !='']

    # [print(item,':',submit[excel][item]) for item in submit[excel] if submit[excel][item]!=None and submit[excel][item] !='']
    # [print(item,':',submit[excel][item]) for item in submit[excel] if item == 'homephone']  
    return
    submit['Mission_Id'] = '10046'
    submit['Country'] = 'US'
    chrome_driver = Chrome_driver.get_chrome(submit)
    web_submit(submit,chrome_driver,1)

def test1():
    num_gender = random.randint(0,1)
    print(num_gender)


if __name__=='__main__':
    test()