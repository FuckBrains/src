import db
from selenium import webdriver
import os
import sys
sys.path.append("..")
from time import sleep
import random
import ip_test
import tools


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
    j = 0
    chrome_driver.get('https://whoer.net')
    handle = chrome_driver.current_window_handle
    for url in url_lists:
        if  j >= 5:
            j = 0
            a = input('input:')
            handles=chrome_driver.window_handles
            for i in handles:
                if i != handle:
                    try:
                        chrome_driver.switch_to.window(i)            
                        chrome_driver.close()
                    except:
                        pass
            # chrome_driver.quit()
            # chrome_driver = get_chrome(dir_account)
        print('Opening alliance site:',url,'.........................')
        chrome_driver.switch_to.window(handle)
        newwindow='window.open("' + url + '");'
        chrome_driver.execute_script(newwindow) 
        # chrome_driver.get(url)  
        j+=1	
    while True:
    	sleep(3000)

def makedir_account(path=r'c:\emu_download'):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)

def Get_Alliance_name():
    path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    dir_alliance = os.path.join(path,r'alliance\Alliance_name.xlsx')    
    sheet = db.get_sheet(dir_alliance)
    Alliance = sheet.col_values(0)
    Alliance.remove('Alliance')
    print(Alliance)
    site = sheet.col_values(1)
    site.remove('site')
    print(site)
    Alliance_dict = dict(zip(Alliance,site))  # 列表表达式把数据组装起来    
    print(Alliance_dict)
    return Alliance,site,Alliance_dict



def Get_roboform_account():
    path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    dir_roboform = os.path.join(path,r'alliance\roboform.txt')        
    accounts = []
    with open(dir_roboform) as f:
        lines = f.readlines()
        for line in lines:
            if line.strip('\n') == '':
                continue
            else:
                roboform_account = {}
                account = line.strip('\n').split(',')
                roboform_account['Country'] = account[1]
                roboform_account['state'] = account[2]
                roboform_account['city'] = account[3]                
                roboform_account['name_roboform'] = account[4]
                roboform_account['pwd_roboform'] = account[5]
                accounts.append(roboform_account)
    return accounts



def main(i):
    # tools.killpid()
    roboform_account = Get_roboform_account()
    # city = 'Not found'
    # for j in range(10):
        # city = ip_test.ip_Test(city=roboform_account[i-1]['city'],state=roboform_account[i-1]['state'],country=roboform_account[i-1]['Country'])
        # if  city != 'Not found':
            # break    
    path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    dir_account = os.path.join(path,r'alliance\account'+str(i))
    # dir_account = r'..\alliance\account1'
    Alliance,url_lists,Alliance_dict = Get_Alliance_name()
    makedir_account(dir_account)
    # user_data_dir = r'C:\Users\xixi\AppData\Local\Google\Chrome\User Data'
    Alliance_login(dir_account,url_lists)
    # sleep(3000)

if __name__ == '__main__':
    paras=sys.argv
    # test    
    # paras = [0,1,2,3,4]
    i = int(paras[1])
    main(i)