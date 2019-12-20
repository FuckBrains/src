from selenium.webdriver import ActionChains
from time import sleep 
from selenium.webdriver.common.keys import Keys
import traceback
import Input_Config
import Submit_handle
import json
from selenium.webdriver.support.ui import Select as Select_
import random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import db
import tools
import os
import sys
sys.path.append("..")


def write_cookie(cookie,country):
    path_res = r'..\res\cookies'
    tools.makedir_account(path_res)    
    path_country = os.path.join(path_res,country)
    tools.makedir_account(path_country)
    filename = str(random.randint(100000,999999999))+'.txt'
    path_cookie = os.path.join(path_country,filename)
    with open (path_cookie,'w') as f:
        f.write(cookie)

def get_action(chrome_driver,data,submit):
    # print('Keys in submit:',len(submit))
    for key in submit:
        # print(key)
        if 'BasicInfo_Id' in submit[key]:
            key_excel = key
            break
    print(data)
    action_func = data['Action']
    data['Step_config'] = json.loads(data['Step_config']) 
    # data['General'] = json.loads(data['General'])
    print(action_func)
    if action_func == 'Set_Status':
        db.update_plan_status(1,submit['ID']) 
        return
    if action_func == 'Set_Cookie':
        cookies = chrome_driver.get_cookies()
        cookie_str = json.dumps(cookies)
        submit['Cookie'] = cookie_str
        submit['BasicInfo_Id'] = submit[key_excel]['BasicInfo_Id']
        write_cookie(cookie_str)
        # db.upload_accounts(submit) 
        return
    if action_func == 'Set_Sleep':
        time_ = submit[data['Step_config']['sleep']]
        sleep(time_)
        return
    if data['General']['iframe'] != '':
        chrome_driver.switch_to_frame(data['General']['iframe'])
    # print("data['General']['iframe']",data['General']['iframe'])
    # scroll_and_find_up(chrome_driver,data['General']['xpath'])    
    # sleep(1)
    # print("data['General']['scroll']",data['General']['scroll'])        
    if data['General']['try'] == 'True':
        try:    
            eval(action_func)(chrome_driver,data,submit[key_excel])
        except Exception as e:
            traceback_ = traceback.format_exc()
    else:
        eval(action_func)(chrome_driver,data,submit[key_excel])


def scroll_and_find(chrome_driver,element):
    target = chrome_driver.find_element_by_xpath(element) 
    chrome_driver.execute_script("arguments[0].scrollIntoView();", target)
    js="var q=document.documentElement.scrollTop=-300"
    chrome_driver.execute_script(js) 
    sleep(3)
    return target

def scroll_and_find_up(chrome_driver,element):
    target = chrome_driver.find_elements_by_xpath(element) 
    chrome_driver.execute_script("arguments[0].scrollIntoView();", target[0])
    # js="var q=document.documentElement.scrollTop=-300"
    # chrome_driver.execute_script(js) 
    sleep(3)
    return target

def overlay_click(chrome_driver,element):
    js = 'arguments[0].click();'
    chrome_driver.execute_script(js) 

def clear_deep(element):
    element.send_keys(Keys.CONTROL,'a')
    element.send_keys(Keys.BACK_SPACE)

def Select(chrome_driver,data,submit):
    '''
    select_type:
        1.select_by_index
        2.select_by_value
    1 deselect_all             # 取消全部的已选择项
    2 deselect_by_index        # 取消已选中的索引项
    3 deselect_by_value        # 取消已选中的value值
    4 deselect_by_visible_text # 取消已选中的文本值
    1 options                  # 返回select元素所有的options
    2 all_selected_options     # 返回select元素中所有已选中的选项
    3 first_selected_options   # 返回select元素中选中的第一个选项        
    '''
    # if data['General']['hidden_xpath'] != '':
    #     print("data['General']['hidden_xpath']:",data['General']['hidden_xpath'])
    #     element = chrome_driver.find_element_by_xpath(data['General']['hidden_xpath'])    
    if data['General']['tagname'] != '':
        element = chrome_driver.find_element_by_xpath(data['General']['xpath'])
        element.click()
        sleep(2)
        print('Find element of xpath')
        if ',' in data['General']['hidden_xpath'] :
            xpaths_hidden = data['General']['hidden_xpath'].split(',')
            tagnames = data['General']['tagname'].split(',')
            print('xpaths_hidden',xpaths_hidden)
            print('tagnames:',tagnames)
        else:
            xpaths_hidden = [data['General']['hidden_xpath']]
            tagnames = [data['General']['tagname']]
        for xpath_ in xpaths_hidden:
            print('xpath_',xpath_)
            try:
                element_hidden = chrome_driver.find_element_by_xpath(xpath_)
                index_tag = xpaths_hidden.index(xpath_)
                print('index_tag:',index_tag)
                options = element_hidden.find_elements_by_tag_name(tagnames[index_tag])
                num = random.randint(1,len(options)-1)
                sleep(1)
                print(options)
                options[num].click()
                return  
            except:
                traceback.print_exc()
    elif data['General']['hidden_xpath'] != '':
        element = chrome_driver.find_element_by_xpath(data['General']['hidden_xpath'])        
        print('Find element of hidden_xpath')        
    else:
        element = chrome_driver.find_element_by_xpath(data['General']['xpath'])        
        print('also xpath')
    s1 = Select_(element)    
    options = s1.options
    values = []
    for i in range(60):
        if len(options) <= 1:
            sleep(1)
        else:
            break    
    for option in options:
        value = option.get_attribute("value")
        selected = option.get_attribute("selected")        
        if selected == True:
            option.removeAttr('selected')
            # js="$('%s').removeAttr('selected')"%data['Step_config']['selected_css']
            # chrome_driver.execute_script(js)              
        values.append(value)

    '''
    5 ways to select
    '''
    # 1.select_by_index
    if data['Step_config']['select_index'] != '':        
        s1.select_by_index(int(data['Step_config']['select_index']))  
        return      
    # 2.select_by_index and random
    if data['Step_config']['select_index_rand'] == 'True':
        num = random.randint(1,len(options)-1)
        s1.select_by_index(num)
        return              
    # 3.select_by_value
        # use func to handle data if necessary
        # use random if values not in values in page
    if data['Step_config']['select_value'] != 'False':
        if data['Step_config']['select_func'] != 'False':
            content = eval('Submit_handle.'+data['Step_config']['select_func'])(submit[data['Step_config']['select_value']])
        else:                  
            content = submit[data['Step_config']['select_value']]
        if content in values:
            s1.select_by_value(submit[data['Step_config']['select_value']])    
            return      
        else:
            num = random.randint(1,len(options)-1)
            s1.select_by_value(str(values[num]))
            return      
    # 4.select_value_range
    if data['Step_config']['select_value_range'][0] != '':
        value_num = random.randint(int(data['Step_config']['select_value_range'][0]),int(data['Step_config']['select_value_range'][1]))
        s1.select_by_value(str(value_num))   
        return  
    # 5. select by values set and in random
    if data['Step_config']['select_value_content'] != '':
        contents = data['Step_config']['select_value_content'].split('\n')
        contents = [content for content in contents if content in values]
        if len(contents) != 0:
            num = random.randint(0,len(contents))
            s1.select_by_value(str(contents[num]))   
        else:
            num = random.randint(1,len(options)-1)
            s1.select_by_value(str(values[num]))
        return

        # if len(data['Step_config']['select_value_list']) != 0:
        #     num = random.randint(0,len(data['Step_config']['select_value_list'])-1)
        #     s1.select_by_value(str(data['Step_config']['select_value_list'][num]))            

def Slide(chrome_driver,data,submit):
    brightnessSlider=chrome_driver.find_element_by_xpath(data['General']['xpath'])
    #定位到滑动块
    x_move_num = random.randint(data['slide']['x_move_min'],data['slide']['x_move_max'])
    y_move_num = random.randint(data['slide']['y_move_min'],data['slide']['y_move_max'])    
    ActionChains(chrome_driver).click_and_hold(brightnessSlider).move_by_offset(x_move_num,y_move_num).release().perform()#通过move_by_offset()移动滑块，-6表示在水平方向上往左移动6个像素，7表示在垂直方向上往上移动7个像素    

def Input(chrome_driver,data,submit):
    element = Click(chrome_driver,data,submit)
    clear_deep(element)
    if data['Step_config']['input_key'] != 'False':
        if data['Step_config']['input_func'] != 'False' :
            content = eval('Submit_handle.'+data['Step_config']['input_func'])(submit[data['Step_config']['input_key']])
        else:
            content = submit[data['Step_config']['input_key']]
    elif data['Step_config']['input_generate'] != 'False':
        if data['Step_config']['input_func'] != 'False' :
            content = eval('Submit_handle.'+data['Step_config']['input_func'])()
        else:
            content = submit[data['Step_config']['input_generate']]
    else:
        content = submit[data['Step_config']['input_content']]
    element.send_keys(content)

def Click(chrome_driver,data,submit):
    WebDriverWait(chrome_driver,120).until(EC.element_to_be_clickable((By.XPATH,data['General']['xpath'])))    
    if data['General']['hidden_xpath'] != '':
        xpath = data['General']['hidden_xpath']
    else:
        xpath = data['General']['xpath'] 
    try:
        element = chrome_driver.find_element_by_xpath(xpath)
        element.click()
    except:
        element = chrome_driver.find_element_by_xpath(xpath)
        actions = ActionChains(chrome_driver)
        actions.move_to_element_with_offset(element,0,0).click().perform()           
    return element

