from selenium import webdriver
import sys
sys.path.append("..")
from time import sleep
import random

def get_ua_all():
    uas = []
    with open(r'../res/ua.txt') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip('\n') != '':
                if 'Windows' not in line:
                    continue 
                if 'Chrome' in line:
                    uas.append(line.strip('"').strip("'").strip('\n'))

    # for ua in uas.split('/n'):
        # print(ua)
    return uas

def get_ua_random(uas):
    num = random.randint(0,len(uas)-1)
    # print(uas[num])
    return uas[num]


def get_chrome(submit = None):
    uas = get_ua_all()
    ua = get_ua_random(uas)
    print(ua)
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": 'c:\\',
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "safebrowsing.enabled": True
             }    
    # prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'c:\\'}
    # options.add_experimental_option('prefs', prefs)
    # extension_path = '../tools/extension/1.1.0_0.crx'   
    # options.add_extension(extension_path) 
    # prefs = {
    # 'profile.default_content_setting_values': {
    # # "User-Agent": ua, # 更换UA
    # # 0 为屏蔽弹窗，1 为开启弹窗
    # 'profile.default_content_settings.popups': 0,
    # } 
    # }   
    options.add_argument('user-agent=' + ua) 
    options.add_argument("--disable-automation")
    options.add_experimental_option("excludeSwitches" , ["enable-automation","load-extension"])
    options.add_experimental_option("prefs", prefs) 
    chrome_driver = webdriver.Chrome(chrome_options=options)
    # chrome_driver.set_page_load_timeout(120)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒    
    return chrome_driver

if __name__ == '__main__':
    chrome_driver = get_chrome()
    chrome_driver.get('http://www.baidu.com')
    print('ppppppppp')
    sleep(20)
    chrome_driver.quit()
    # sleep(20)
    # uas = get_ua_all()
    # for ua in uas:
    #     print(ua)
    # print(uas[0:30])
    # print(len(uas))