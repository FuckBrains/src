from selenium import webdriver
import sys
sys.path.append("..")
from time import sleep
import random

def get_chrome(user_data_dir,submit=None):
    options = webdriver.ChromeOptions()
    # (?# __browser_url = r'C:\Users\xixi\AppData\Local\Google\Chrome\Application')
    
    options.add_argument('--user-data-dir='+user_data_dir)
    # options.binary_location=__browser_url
    prefs = {"download.default_directory": 'c:\\',
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "safebrowsing.enabled": True,
             "credentials_enable_service":False,
             "password_manager_enabled":True
             }    
    # prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'c:\\emu_download'}
    # options.add_experimental_option('prefs', prefs)
    extension_path = '../tools/extension/1.1.0_0.crx'  
    options.add_extension(extension_path) 
    extension_path = '../tools/extension/1.0.14_0.crx'       
    options.add_extension(extension_path) 
    extension_path = '../tools/extension/8.6.0.0_0.crx'       
    options.add_extension(extension_path) 
    
    
    # prefs = {
    # 'profile.default_content_setting_values': {
    # # "User-Agent": ua, # 更换UA
    # # 0 为屏蔽弹窗，1 为开启弹窗
    # 'profile.default_content_settings.popups': 0,
    # } 
    # }   
    # options.add_argument('user-agent=' + ua) 
    # options.add_argument('--single-process')
    # options.add_argument('--process-per-tab')    
    
    # options.add_argument('--disable-gpu')        
    # options.add_argument("--disable-automation")
    options.add_argument("--disable-automation")
    # options.add_experimental_option("excludeSwitches" , ["enable-automation","load-extension"])
    options.add_experimental_option("prefs", prefs) 
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.set_page_load_timeout(300)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒    
    return chrome_driver

def Alliance_login(dir_account,url_lists):
    chrome_driver = get_chrome(dir_account)
    # chrome_driver.get(url_lists[0])
    # while True:
    for url in url_lists:
        print(url)
        chrome_driver.get(url)
        newwindow='window.open("' + url + '");'
        chrome_driver.execute_script(newwindow)   	
    while True:
    	sleep(3000)



def main():
    dir_account = r'C:\alliance\account1'
    url_lists = [
    'http://adsmain.affise.com/',
    'https://adpump.com',
    'http://partners.adgaem.com',
    'https://affiliate.adgtracker.com'
    ]
    # user_data_dir = r'C:\Users\xixi\AppData\Local\Google\Chrome\User Data'
    Alliance_login(dir_account,url_lists)
    # sleep(3000)

if __name__ == '__main__':
    main()
