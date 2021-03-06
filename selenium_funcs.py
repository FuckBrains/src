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
    path_res = r'..\res\cookies\US'
    tools.makedir_account(path_res)    
    filename = str(random.randint(100000,999999999))+'.txt'
    path_cookie = os.path.join(path_res,filename)
    with open (path_cookie,'w') as f:
        f.write(cookie)

def get_action(chrome_driver,data,submit):
    # print('Keys in submit:',submit)
    if 'Dadao' in submit:
        key_excel = 'Dadao'
    else:
        if 'Email' in submit:
            key_excel = 'Email'
        else:            
            for key in submit:
                # print(key)
                if type(submit[key]) == type({}):
                    if 'BasicInfo_Id' in submit[key]:
                        key_excel = key
                        break
    print(data)
    action_func = data['Action']
    data['Step_config'] = json.loads(data['Step_config']) 
    # data['General'] = json.loads(data['General'])
    print(action_func)

    if action_func == 'Change_page':
        handles=chrome_driver.window_handles   
        for i in handles:
            if i != submit['handle']:        
                chrome_driver.switch_to.window(i)  
                return  submit  
    if action_func == 'Set_Status':
        db.update_plan_status(1,submit['ID']) 
        return submit
    if action_func == 'Js':
        if 'content' not in data['Step_config']:
            chrome_driver.execute_script(data['Step_config']['js_remove'])
            date = Submit_handle.get_next_payday_all()
            js_set_value = data['Step_config']['js_set_value']+date+'"'
            chrome_driver.execute_script(js_set_value)   
        else:
            print('Js content:',data['Step_config']['content'])
            if data['Step_config']['content'] == 'bi_week':
                chrome_driver.execute_script(data['Step_config']['js_remove'])
                date = Submit_handle.get_next_payday_all()
                js_set_value = data['Step_config']['js_set_value']+date+'"'
                chrome_driver.execute_script(js_set_value)                   
            else:
                chrome_driver.execute_script(data['Step_config']['js_remove'])
                date = Submit_handle.get_next_payday2_all()
                js_set_value = data['Step_config']['js_set_value']+date+'"'
                chrome_driver.execute_script(js_set_value)                  
        return submit  
    if action_func == 'Alert':
        dig_alert = chrome_driver.switch_to.alert
        sleep(1)
        print(dig_alert.text)
        dig_alert.accept()
        sleep(1)
        return submit            
    if action_func == 'Set_Cookie':
        cookies = chrome_driver.get_cookies()
        cookie_str = json.dumps(cookies)
        submit['Cookie'] = cookie_str
        submit['BasicInfo_Id'] = submit[key_excel]['BasicInfo_Id']
        write_cookie(cookie_str,submit['Country'])
        # db.upload_accounts(submit) 
        return submit
    if action_func == 'Set_Sleep':
        time_ = int(data['Step_config']['sleep'])
        try:
            print('sleep:',time_)
            sleep(time_)
        except Exception as e:
            print('sleep fail:',str(e))
        return submit
    # if data['General']['iframe'] != '':
    #     chrome_driver.switch_to_frame(data['General']['iframe'])
    # print("data['General']['iframe']",data['General']['iframe'])

    sleep(1)
    print('====================')
    # print("data['General']['scroll']",data['General']['scroll'])   
    element = ''
    if data['General']['try'] == 'True':
        try:
            if 'father_type' in data['General']:
                element = get_element(chrome_driver,data)
                print('Element get before action_func:',element)   
            if data['General']['scroll'] == 'True':
                try:
                    print('ready to scroll and find element')
                    # js="var q=document.documentElement.scrollTop=10000"
                    # chrome_driver.execute_script(js)             
                    # print('scroll success')
                    # sleep(3)
                    # js="var q=document.documentElement.scrollTop=-10000"
                    # chrome_driver.execute_script(js)     
                    # sleep(3)  
                    if 'top' in  data['General']:
                        top = data['General']['scroll']
                    else:
                        top = 'true'
                    scroll_and_find(chrome_driver,element,top)       
                except Exception as e:
                    print('scroll failed')
                    scroll_and_move(chrome_driver)            
                    print(str(e))                         
            if action_func == 'Input':
                submit[key_excel] = eval(action_func)(chrome_driver,data,submit[key_excel],element)
            else:
                eval(action_func)(chrome_driver,data,submit[key_excel],element)
        except Exception as e:
            a = traceback_ = traceback.format_exc()
            print(a)
    else:
        if 'father_type' in data['General']:
            element = get_element(chrome_driver,data)
            print('Element get before action_func:',element)   
        if data['General']['scroll'] == 'True':
            try:
                print('ready to scroll and find element')
                # js="var q=document.documentElement.scrollTop=10000"
                # chrome_driver.execute_script(js)             
                # print('scroll success')
                # sleep(3)
                # js="var q=document.documentElement.scrollTop=-10000"
                # chrome_driver.execute_script(js)     
                # sleep(3)  
                if 'top' in  data['General']:
                    top = data['General']['scroll']
                else:
                    top = 'true'
                scroll_and_find(chrome_driver,element,top)       
            except Exception as e:
                print('scroll failed')
                scroll_and_move(chrome_driver)            
                print(str(e))    
        if action_func == 'Input':
            submit[key_excel] = eval(action_func)(chrome_driver,data,submit[key_excel],element)
        else:
            eval(action_func)(chrome_driver,data,submit[key_excel],element)
    return submit

def get_element(chrome_driver,data):
    father_elem = ''
    if data['General']['father_type'] != 'False':
        if data['General']['father_content'] != '':
            #find father elem with xpath or class
            content_father = data['General']['father_content']
            method_father = data['General']['father_type']
            father_elem = get_elem_part(chrome_driver,method_father,content_father)
            print('find father elem with xpath or class')
    if father_elem != '':
        # find child elem from father elem
        elem = father_elem
        print('find child elem from father elem')
    else:
        # find elem without father elem
        elem = chrome_driver
        print('find elem without father elem')
    content_child = data['General']['child_content']
    method_child = data['General']['child_type']        
    element = get_elem_part(elem,method_child,content_child)
    return element

def get_elem_part(elem,method,content):
    if ',' in content:
        contents = content.split(',')
        num = len(contents)
        num_ = random.randint(0,num-1)
        content = contents[num_]
    element = ''
    print('get_elem_part:content-->',content)
    if method == 'Xpath':
        print('by xpath')
        if ':' in content:
            content_ = content.split(':')
            num_xpath = int(content_[1])
            content = content_[0]
            elements = elem.find_elements_by_xpath(content)
            print('total %d elems found of class %s'%(len(elements),content))
            print('num_class:%d'%num_xpath)
            element = elements[num_xpath]            
        else:            
            element = elem.find_element_by_xpath(content)
    elif method == 'Class':
        print('by class')
        if ':' in content:
            content_ = content.split(':')
            num_class = int(content_[1])
            content = content_[0]
            elements = elem.find_elements_by_class_name(content)
            print('total %d elems found of class %s'%(len(elements),content))
            print('num_class:%d'%num_class)
            element = elements[num_class]
        else:
            element = elem.find_element_by_class_name(content)
            print('find elem by class %s'%content)
    elif method == 'Tag':
        print('by tag name')
        if ':' in content:
            tag_content = content.split(':') 
            content = tag_content[0]
            num = int(tag_content[1])
            elements = elem.find_elements_by_tag_name(content)
        else:
            elements = elem.find_elements_by_tag_name(content)
            num = random.randint(0,len(elements)-1)
        element = elements[num]
    else:
        pass
    return element

def scroll_and_find(chrome_driver,target,top='true'):
    # js="var q=document.documentElement.scrollTop=10000"
    # chrome_driver.execute_script(js)     
    # print('go down 10000 meters')
    # target = chrome_driver.find_element_by_xpath(element) 
    chrome_driver.execute_script("arguments[0].scrollIntoView(%s);"%top, target)
    print('find target to move finished')
    # js="var q=document.documentElement.scrollTop=-50"
    # chrome_driver.execute_script(js) 
    sleep(3)
    return target

def scroll_action(chrome_driver,element):
    ActionChains(chrome_driver).move_to_element(element).perform()  
    sleep(2)  

def scroll_and_move(chrome_driver,num=300):
    # js="var q=document.documentElement.scrollTop=10000"
    # chrome_driver.execute_script(js)     
    # print('go down 10000 meters')
    # target = chrome_driver.find_element_by_xpath(element) 
    # chrome_driver.execute_script("arguments[0].scrollIntoView();", target)
    print('find target to move in scroll and move ')
    js="var q=document.documentElement.scrollTop=%s"%str(num)
    chrome_driver.execute_script(js) 
    sleep(3)
    return 

def scroll_and_find_up(chrome_driver,element):
    target = chrome_driver.find_elements_by_xpath(element) 
    chrome_driver.execute_script("arguments[0].scrollIntoView();", target[0])
    # js="var q=document.documentElement.scrollTop=-300"
    # chrome_driver.execute_script(js) 
    sleep(3)
    return target[0]

def overlay_click(chrome_driver,element):
    js = 'arguments[0].click();'
    chrome_driver.execute_script(js) 

def clear_deep(element):
    element.send_keys(Keys.CONTROL,'a')
    element.send_keys(Keys.BACK_SPACE)
    sleep(1)

def Slide(chrome_driver,data,submit,element_new=''):
    # ??????????????????
    # brightnessLine.get_attribute("title")#??????title????????????????????????
    brightnessSlider = element_new
    #??????????????????
    move_num = random.randint(10,300)
    print('Move',move_num)
    ActionChains(chrome_driver).click_and_hold(brightnessSlider).move_by_offset(move_num,7).release().perform()#??????move_by_offset()???????????????-6????????????????????????????????????6????????????7????????????????????????????????????7?????????    

def Select(chrome_driver,data,submit,element_new=''):
    '''
    select_type:
        1.select_by_index
        2.select_by_value
    1 deselect_all             # ???????????????????????????
    2 deselect_by_index        # ???????????????????????????
    3 deselect_by_value        # ??????????????????value???
    4 deselect_by_visible_text # ???????????????????????????
    1 options                  # ??????select???????????????options
    2 all_selected_options     # ??????select?????????????????????????????????
    3 first_selected_options   # ??????select?????????????????????????????????        
    '''
    # if data['General']['hidden_xpath'] != '':
    #     print("data['General']['hidden_xpath']:",data['General']['hidden_xpath'])
    #     element = chrome_driver.find_element_by_xpath(data['General']['hidden_xpath'])
    if element_new != '':
        element = element_new
    else:
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
                    a = traceback.print_exc()
                    print(a)
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
        item_list = data['Step_config']['select_index'].split(',')
        key = data['Step_config']['select_value']
        value = str(submit[key]).split('.')[0]
        if key == 'year':
            if len(value) >2:
                value = value[2:] 
        index_ = item_list.index(int(value))       
        s1.select_by_index(index_)  
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
            content = eval('Submit_handle.'+data['Step_config']['select_func'])(submit)
            content = str(content)
            print('Slect-->>select_func-->>content:',content)            
        else:                  
            content = submit[data['Step_config']['select_value']]
            content = str(content)            
            print('Slect-->>select_value-->>content:',content)            
        print('values:',values)            
        if content in values:
            print('content in values')            
            s1.select_by_value(content)    
            return      
        else:
            print('content not in values,select random')                        
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
        if type(data['Step_config']['select_value_content']) == type([]):
            contents = data['Step_config']['select_value_content']
        else:
            contents = data['Step_config']['select_value_content'].split('\n')
            contents = [content for content in contents if content in values]
        if len(contents) != 0:
            num = random.randint(0,len(contents)-1)
            s1.select_by_value(str(contents[num]))   
        else:
            num = random.randint(1,len(options)-1)
            s1.select_by_value(str(values[num]))
        return

        # if len(data['Step_config']['select_value_list']) != 0:
        #     num = random.randint(0,len(data['Step_config']['select_value_list'])-1)
        #     s1.select_by_value(str(data['Step_config']['select_value_list'][num]))            

def Input(chrome_driver,data,submit,element_new=''):
    # print('submit in INput:',submit)
    # print('data:',data)
    # print('city:',submit['City'])
    element = Click(chrome_driver,data,submit,element_new)
    print('after click')
    # if 'input_clear' in  data['Step_config']:
    #     if data['Step_config']['input_clear'] == 'True':
    #         clear_deep(element)
    # else:
    clear_deep(element)
    print('after clear_deep')
    if data['Step_config']['input_key'] != 'False':
        if data['Step_config']['input_func'] != 'False' :
            content = eval('Submit_handle.'+data['Step_config']['input_func'])(submit)
            print(content)            
        else:
            content = submit[data['Step_config']['input_key']]
            print(content)
    elif data['Step_config']['input_generate'] != 'False':
        if data['Step_config']['input_func'] != 'False' :
            content = eval('Submit_handle.'+data['Step_config']['input_func'])(submit)
            submit[data['Step_config']['input_generate']] = content
            print('content:',content)
        else:
            content = submit[data['Step_config']['input_generate']]
    else:
        content = data['Step_config']['input_content']
    test_list = ['id_number','iban']
    if data['Step_config']['input_key'] in test_list:
        print(data['Step_config']['input_key'])
        element.send_keys(content)
    if 'input_method' in data['Step_config']:
        if data['Step_config']['input_method'] == 'Js_value':
            js =  "arguments[0].value='" + content + "';"
            chrome_driver.execute_script(js, element)
            return submit
        elif data['Step_config']['input_method'] == 'together':
            element.send_keys(content)
            return submit
        elif data['Step_config']['input_method'] == 'Js_innertext':
            js =  "arguments[0].innerText='" + content + "';"
            chrome_driver.execute_script(js, element)
            return submit            
        else:
            for item in str(content):
                element.send_keys(item)  
            return submit        
    for item in str(content):
        # if item in '0123456789':
        #     item = int(item)
        #     sleep(1)
        element.send_keys(item)
    return submit

def Click(chrome_driver,data,submit,element_new=''):
    if element_new != '':
        element = element_new
    else:
        if 'class_name' in data['General']:
            if data['General']['class_name'] != '':
                try:
                    element = chrome_driver.find_element_by_class_name(data['General']['class_name'])
                    element.click()
                except:
                    pass
                return element
        else:
            WebDriverWait(chrome_driver,120).until(EC.element_to_be_clickable((By.XPATH,data['General']['xpath'])))    
        if data['General']['hidden_xpath'] != '':
            xpath = data['General']['hidden_xpath']
        else:
            if ',' in data['General']['xpath']:
                xpaths = data['General']['xpath'].split(',')
                num = len(xpaths)
                num_ = random.randint(0,num-1)
                xpath = xpaths[num_] 
            else:       
                xpath = data['General']['xpath'] 
        element = chrome_driver.find_element_by_xpath(xpath)  
    if 'click' in data['Step_config']:
        print('Click method:',data['Step_config']['click'])        
        if data['Step_config']['click'] == 'Click':
            print('ready to click')
            element.click()
            print('after click')
            return element
        elif data['Step_config']['click'] == 'Simulate':
            actions = ActionChains(chrome_driver)
            actions.move_to_element_with_offset(element,3,3).click().perform()  
            return element
        else:
            chrome_driver.execute_script("arguments[0].click()", element)
            return element     
    return element


