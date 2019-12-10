from time import sleep 
from selenium.webdriver.common.keys import Keys
import traceback
import Input_Config
import Submit_handle
import json
from selenium.webdriver.support.ui import Select as Select_
import random


def get_action(chrome_driver,data,submit):
    print(data)
    action_func = data['Action']
    data['Step_config'] = json.loads(data['Step_config']) 
    data['General'] = json.loads(data['General'])     
    print(action_func)
    if data['General']['iframe'] != '':
        chrome_driver.switch_to_frame(data['General']['iframe'])
    print("data['General']['iframe']",data['General']['iframe'])
    if data['General']['scroll'] == 'True':
        scroll_and_find_up(chrome_driver,data['General']['xpath'])    
    print("data['General']['scroll']",data['General']['scroll'])        
    if data['General']['try'] == 'True':
        try:    
            eval(action_func)(chrome_driver,data,submit)
        except Exception as e:
            traceback_ = traceback.format_exc()
    else:
        eval(action_func)(chrome_driver,data,submit)

def scroll_and_find(chrome_driver,element):
    target = chrome_driver.find_element_by_xpath(element) 
    chrome_driver.execute_script("arguments[0].scrollIntoView();", target)
    js="var q=document.documentElement.scrollTop=-300"
    chrome_driver.execute_script(js) 
    sleep(3)
    return target

def scroll_and_find_up(chrome_driver,element):
    target = chrome_driver.find_element_by_xpath(element) 
    chrome_driver.execute_script("arguments[0].scrollIntoView();", target)
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
    element = chrome_driver.find_element_by_xpath(data['General']['xpath'])    
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
    # if data['Step_config']['selected_css'] != '':
    #     pass
    if data['Step_config']['select_index'] != '':        
        s1.select_by_index(int(data['Step_config']['select_index']))  
        return      
    if data['Step_config']['select_index_rand'] == 'True':
        num = random.randint(1,len(options)-1)
        s1.select_by_index(num)
        return              
    if data['Step_config']['select_value'] != '':
        if submit[data['Step_config']['select_value']] in values:
            s1.select_by_value(submit[data['Step_config']['select_value']])    
            return      
        else:
            num = random.randint(1,len(options)-1)
            s1.select_by_value(str(values[num]))
            return      
    if len(data['Step_config']['select_value_range']) != 0:
        value_num = random.randint(int(data['Step_config']['select_value_range'][0]),int(data['Step_config']['select_value_range'][1]))
        s1.select_by_value(str(value_num))   
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
    input_key = data['Step_config']['input_key']
    if input_key == 'False':
        content = data['content']
    else:
        key = data['Step_config']['input_func']
        input_func = Input_Config.get_input_config(key)
        if len(input_func) != 0:
            content = eval('Submit_handle.'+input_func)(chrome_driver,data,submit)
        else:
            content = submit[input_key]
    element.send_keys(content)

def Click(chrome_driver,data,submit):
    if data['General']['scroll'] == True:
        element = scroll_and_find_up(chrome_driver,data['General']['xpath'])
    element = chrome_driver.find_element_by_xpath(data['General']['xpath'])
    element.click()
    return element


