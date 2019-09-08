import xlrd
import db
from selenium import webdriver
import os
import sys
sys.path.append("..")
from time import sleep
import random
import ip_test
import tools


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

def get_chrome(user_data_dir,submit=None):
    options = webdriver.ChromeOptions()
    # (?# __browser_url = r'C:\Users\xixi\AppData\Local\Google\Chrome\Application')
    uas = get_ua_all()
    ua = get_ua_random(uas)
    print(ua)    
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
    options.add_argument('user-agent=' + ua) 
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
    # cookies = chrome_driver.get_cookies()  
    # print(cookies)
    # chrome_driver.delete_all_cookies()    
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
    workbooks = xlrd.open_workbook(dir_alliance)
    names = workbooks.sheet_names()
    # print(names)
    Alliance_dict = {}
    for name in names:
        if name == 'Sites':
            sheet = workbooks.sheet_by_name('Sites')
            Alliance = sheet.col_values(0)
            Alliance.remove('Alliance')
            # print(Alliance)
            site = sheet.col_values(1)
            site.remove('site')
            # print(site)
            Alliance_dict_sites = dict(zip(Alliance,site))  # 列表表达式把数据组装起来    
            # print(Alliance_dict_sites)
            Alliance_dict[name] = Alliance_dict_sites
        else:
            sheet = workbooks.sheet_by_name(name)
            keys = sheet.row_values(0)
            ncols = sheet.ncols
            accounts = {}
            for i in range(ncols):
                if i == 0:
                    print(i)
                    print(keys[i])
                    alliance_list = sheet.col_values(i)
                    alliance_list.remove(keys[i])
                    print('alliance_list:',alliance_list)
                else:
                    print(i)
                    account_list = sheet.col_values(i)
                    # account_list = [str(name) for name in account_list if type(name) != type('1')]
                    # account_list = [name.split(',') for name in account_list if ',' in name]
                    account_list.remove(keys[i]) 
                    print('account_list:',account_list)
                    accounts[keys[i]] = dict(zip(alliance_list,account_list))
            Alliance_dict[name] = accounts            
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


def cookies_test():
    i = 1
    path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    dir_account = os.path.join(path,r'alliance\account'+str(i))    
    chrome_driver = get_chrome(dir_account)   
    url_test = 'http://lub.lubetadating.com/c/13556/0?'
    chrome_driver.get(url_test) 
    cookies = chrome_driver.get_cookies()
    print(cookies)          
    chrome_driver.delete_all_cookies() 
    print('===================')
    cookies = chrome_driver.get_cookies()
    print(cookies)    
    chrome_driver.get(url_test)     
    print('+++++++++++++++++++++++++')
    cookies = chrome_driver.get_cookies()
    print(cookies)    
    sleep(3000)  



def main(i):
    tools.killpid()
    roboform_account = Get_roboform_account()
    city = 'Not found'
    for j in range(10):
        city = ip_test.ip_Test(city=roboform_account[i-1]['city'],state=roboform_account[i-1]['state'],country=roboform_account[i-1]['Country'])
        if  city != 'Not found':
            break    
    path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    dir_account = os.path.join(path,r'alliance\account'+str(i))
    # dir_account = r'..\alliance\account1'
    Alliance,url_lists,Alliance_dict = Get_Alliance_name()
    makedir_account(dir_account)
    # user_data_dir = r'C:\Users\xixi\AppData\Local\Google\Chrome\User Data'
    Alliance_login(dir_account,url_lists)
    # sleep(3000)

if __name__ == '__main__':
    # paras=sys.argv
    # # test    
    # paras = [0,1,2,3,4]
    # i = int(paras[1])
    # main(i)
    main(1)