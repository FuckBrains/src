# 调用格式
# ip_Test(city),city可用指定，也可以为空，为空则全美随机
import sys
sys.path.append("..")
from selenium import webdriver
from time import sleep
import re
import os
import Restart_911 as R9






def ip_new(city,state = 'All',country = 'US'):
    print('Changing Ip')
    if city == '':
        arg = ' -changeproxy/'+ country + '/' + state 
    else:
        arg = ' -changeproxy/' + country + '/' + state + '/' + city
    print('changing ip ....')
    print(arg)
    a = os.system(r'..\tools\911S5\ProxyTool\AutoProxyTool.exe%s' % (arg))
    # os.system('/../../911S5/ProxyTool/1.py')
    #os.system('D:/项目/911S5/ProxyTool/AutoProxyTool.exe%s' % (arg))
    print(a)
    if a == 0 :
        print('change ip  success') 
    else:
        print('change ip failed')



def whoer_get(city =None):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('https://whoer.net')
    chrome_driver.get('https://whoer.net')
    i = 0
    while i <=2:
        try:
            str_1=chrome_driver.find_element_by_xpath('//*[@id="hidden_rating_link"]/span').text
            break
        except:
            print('fail to get whoer ,try %d time'%i)
            chrome_driver.get('https://whoer.net')
            # sleep(5)
            i = i + 1            
    try:
        str_2=chrome_driver.find_element_by_xpath('//*[@id="main"]/section[5]/div/div/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[3]/div[2]/span').text
        if '.' in str_1:
            a = str_1.find('.')
            str_1 = str_1[0:a]
        totalCount = int(re.sub("\D", "", str_1))
        city = str_2
        sleep(3)
        chrome_driver.close()
        chrome_driver.quit()
        # print(str_1)
        # print(str_2)
        print('当前ip匿名度是：'+str(totalCount))
    except:
        print("can't connet to whoer,change ip...")        
        chrome_driver.close()
        chrome_driver.quit()
        return city,-1
    chrome_driver.find_element_by_xpath().text
    return city,totalCount



# 测试ip
# city如果是'',则从us全国获取ip,否则用指定的city去获取ip
def ip_Test(city = None,state = 'All',country='US'):
    totalCount = -1
    i = 0
    flag = 0
    R9.restart911() 
    print('restart 911 end')      
    sleep(20)
    # return
    ip_new(city,state,country)
    sleep(10)
    # city,totalCount = whoer_get(city)
    # print(city,totalCount)
    # if totalCount == -1:
    #     city = 'Not found'
    return city
       
    # path='C:/cam4/driver'
    # executable_path=path
    # ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'    
    # ua = submit['ua']
    # print(ua)
    # ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
       





if __name__=='__main__':
    city = ''
    # ip_Test(city)
    whoer_get('')



