from selenium import webdriver
import sys
sys.path.append("..")
from time import sleep

def get_chrome(submit = None):
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    # extension_path = '../tools/extension/1.1.0_0.crx'   
    # options.add_extension(extension_path) 
    if submit != None:
        if submit['Ua'] != '':
    	    ua = submit['Ua']
        else:
            ua = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    else:
    	ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    prefs = {
    
    'profile.default_content_setting_values': {
    
    # "User-Agent": ua, # 更换UA
    # 0 为屏蔽弹窗，1 为开启弹窗
    'profile.default_content_settings.popups': 0,
    
    }
    
    }   
    options.add_argument('user-agent=' + ua) 
    options.add_experimental_option("prefs", prefs) 
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒	
    return chrome_driver

if __name__ == '__main__':
	chrome_driver = get_chrome()
	chrome_driver.get('http://www.baidu.com')
	sleep(20)