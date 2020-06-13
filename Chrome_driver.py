import winreg
from selenium import webdriver
import os
import sys
sys.path.append("..")
from time import sleep
import random
import zipfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
import luminati
from time import sleep
import globalvar as gl
from win32api import GetFileVersionInfo, LOWORD, HIWORD 



def get_version_number(filename):
    #This is just for windows.
    info = GetFileVersionInfo(filename, "\\")
    #print info
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    # print('Chrome_version:',HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls))
    return HIWORD(ms)

def get_chrome_remote():
    options = webdriver.ChromeOptions()
    options.debugger_address = "127.0.0.1:9222"
    path_driver = get_chromedriver_path()    
    chrome_driver = webdriver.Chrome(chrome_options=options,executable_path=path_driver)    
    return chrome_driver

def get_chromedriver_path():
    path = getInstallBdyAdree()
    path_chrome = path + r'\chrome.exe'
    version = get_version_number(path_chrome)    
    return r'driver/chromedriver_'+str(version)+'.exe'

def getInstallBdyAdree():
    url = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'    
    key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, url)
    data = winreg.QueryValueEx(key, "Path")
    path_chrome = data[0]
    # print('Chrome_path:',path_chrome)
    return path_chrome

def get_ua_all():
    uas = []
    with open(r'ini\ua.txt') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip('\n') != '':
                if 'Windows' not in line:
                    continue 
                # if 'Chrome' in line:
                uas.append(line.strip('"').strip("'").strip('\n'))
    # for ua in uas.split('/n'):
        # print(ua)
    return uas

def get_ua_random(uas):
    num = random.randint(0,len(uas)-1)
    ua = uas[num].replace('"','')    
    # print(uas[num])
    return ua

def get_ua():
    uas = get_ua_all()
    ua = get_ua_random(uas)
    ua = ua.replace('"','')
    return ua


def set_flag(name,value):
    gl.set_value(str(name),value)

def get_flag(name):
    flag = gl.get_value(str(name))
    return flag
def get_gl_():
    flag = gl.get_gl()
    return flag

def get_lan_config(country):
    country_list_code = get_all_country()
    return country_list_code[country]

def get_all_country():
    country_list_code ={
    'US':'en_us',
    'GB':'en_gb',
    'AU':'en_au',
    'FR':'fr',
    'DE':'de',
    'ES':'es',
    'IT':'it',
    'PL':'pl',
    'DK':'dk',
    'NZ':'nz',
    'CA':'ca',
    'CN':'en_us'
    }
    return country_list_code    

def tz_test():
    desired_capabilities = DesiredCapabilities.CHROME # 修改页面加载策略 # none表示将br.get方法改为非阻塞模式，在页面加载过程中也可以给br发送指令，如获取url，pagesource等资源。 desired_capabilities["pageLoadStrategy"] = "none"     
    desired_capabilities = {
        'os' : 'Windows',
        'os_version' : '7',
        'browser' : 'Chrome',
        'browser_version' : '77.0',
        'resolution' : '400x800',
        # 'project' : 'emu_project',
        'build' : 'emu_build',
        # 'name' : 'emu_test',
        # 'browserstack.local' : 'false',
        # 'browserstack.video' : 'false',
        'browserstack.timezone' : 'New_York',
        # 'browserstack.selenium_version' : '3.2.0',
        # 'browserstack.seleniumLogs' : 'false'
    }
    desired_capabilities["pageLoadStrategy"] = "none"            
    path_driver = get_chromedriver_path()    
    chrome_driver = webdriver.Chrome( desired_capabilities=desired_capabilities,executable_path=path_driver)      
    chrome_driver.get('https://www.w3school.com.cn/tiy/t.asp?f=js_date_current')
    sleep(3000)

def get_chrome(submit = None,pic=0,headless=0,time_out=300):
    print('++++++++++++++++++++++++')
    print('++++++++++++++++++++++++')
    print('++++++++++++++++++++++++')
    print('Chrome_driver file version : 1.0')
    # print([key for key in submit])
    # print('++++++++++++++++++++++++')
    # print('++++++++++++++++++++++++')
    # print('++++++++++++++++++++++++')
    
    path_download = get_dir()    
    prefs = {
            "download.default_directory": path_download,
             "download.prompt_for_download": False,
             # "download.directory_upgrade": True,
             # "safebrowsing.enabled": True,
             # 'profile.default_content_settings.popups': 0,
             }   
    # desired_capabilities = DesiredCapabilities.CHROME # 修改页面加载策略 # none表示将br.get方法改为非阻塞模式，在页面加载过程中也可以给br发送指令，如获取url，pagesource等资源。 desired_capabilities["pageLoadStrategy"] = "none"     
                       
    options = webdriver.ChromeOptions() 
    options.add_argument('--disable-gpu')        
    options.add_argument("--disable-automation")
    # options.add_argument('--ignore-certificate-errors') 
    options.add_experimental_option("excludeSwitches" , ["enable-automation","load-extension"])                   
    if headless != 0:
        options.add_argument('--headless')         
    path_driver = get_chromedriver_path()    
    if submit == None:
        uas = get_ua_all()
        ua = get_ua_random(uas)
        # print(ua)
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    else:
        if 'ua' in submit:
            ua = submit['ua']
        else:
            uas = get_ua_all()
            ua = get_ua_random(uas)
            # print(ua)  
         
        # if 'Record' in submit:
        #     print('Cancle record modern')
        #     if submit['Record'] == 3:
        #         desired_capabilities["pageLoadStrategy"] = "none" 
        #         print('Record chrome')                       
        if 'Country' in submit:
            language = get_lan_config(submit['Country'])
            options.add_argument('-lang=' +language )            
        # if 'Mission_Id' in submit:
        #     if submit['Mission_Id'] == '20000':
        #         print('test chrome')
        #     else:
        #         if pic == 0:
        #             prefs["profile.managed_default_content_settings.images"] = 2
        #             prefs["permissions.default.stylesheet"] = 2
        #             print('No pic or css')
        if 'Mission_dir_flag' in submit:
            submit['Mission_dir'] = submit['Mission_dir'].replace('//','\\') 
            print('Selenium in using user-data-dir:',submit['Mission_dir'])
            options.add_argument('--user-data-dir='+submit['Mission_dir'])
        if 'ip_lpm' in submit:
            # print('=======================')
            # print('=======================')    
            # print(submit)            
            account_lpm = luminati.get_account()
            ip = account_lpm['IP_lpm']
            port = submit['port_lpm']
            proxy = 'socks5://%s:%s'%(ip,port)
            options.add_argument('--proxy-server=%s'%proxy)
        if 'traffic' in submit:
            options.add_argument('user-agent=' + ua)
            # options.add_argument('--headless')            
            prefs["profile.managed_default_content_settings.images"] = 2                        
            options.add_experimental_option("prefs", prefs)       
            desired_capabilities = DesiredCapabilities.CHROME # 修改页面加载策略 # none表示将br.get方法改为非阻塞模式，在页面加载过程中也可以给br发送指令，如获取url，pagesource等资源。 desired_capabilities["pageLoadStrategy"] = "none" 
            desired_capabilities["pageLoadStrategy"] = "none"            
            chrome_driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities,executable_path=path_driver)            
            return chrome_driver               
            # print(proxy) 
        # wire_options = ''           
        # if 'oxylab' in submit:
        #     username = 'r782992280'
        #     password = 'nV3nqFtt9S'    
        #     country = submit['oxylab']            
        #     entry = 'customer-%s-cc-%s-sesstime-30:%s@pr.oxylabs.io:7777' %(username, country, password)
        #     wire_options = {
        #         'proxy': {
        #             'http': 'http://'+entry,
        #             'https': 'https://'+entry,
        #             'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
        #         }
        #     }            
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
    # options.add_argument('--single-process')
    # options.add_argument('--process-per-tab') 
    # options.add_argument('–Referer=https://www.facebook.com') 

    options.add_argument('user-agent=' + ua)    
    options.add_experimental_option("prefs", prefs)       
    # print(options)
    # chrome_driver = webdriver.Chrome(desired_capabilities=desired_capabilities,chrome_options=options,executable_path=path_driver)
    # print(path_driver)
    
    # if wire_options == '':
    chrome_driver = webdriver.Chrome(chrome_options=options,executable_path=path_driver)    
    # else:
    #     chrome_driver = webdriver.Chrome(executable_path=path_driver,seleniumwire_options=options)            
    # chrome_driver = webdriver.Chrome(executable_path=path_driver)        
    # chrome_driver = webdriver.Chrome(chrome_options=options,desired_capabilities=desired_capabilities)
    chrome_driver.set_page_load_timeout(time_out)
    # chrome_driver.set_script_timeout(240)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒  
    size = get_size()
    # print('Chrome size:',size)
    chrome_driver.set_window_size(size[0],size[1])
    chrome_driver.maximize_window()  
    chrome_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
        "source":"""
        Object.defineProperty(navigator,'webdriver',{
            get: () => undefined
        })
        """
        })
    sleep(2)  
    return chrome_driver

def get_chrome_test(submit):
    path_download = get_dir()  
    account_lpm = luminati.get_account()
    ip = account_lpm['IP_lpm']
    port = submit['port_lpm']
    PROXY = '%s:%s'%(ip,port)    
    # PROXY = "proxy_host:proxy:port"    
    options = webdriver.ChromeOptions()
    desired_capabilities = options.to_capabilities()
    desired_capabilities['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "noProxy": None,
        "proxyType": "MANUAL",
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    }
    path_driver = get_chromedriver_path()                                        
    chrome_driver = webdriver.Chrome(desired_capabilities = desired_capabilities,executable_path=path_driver)
    time_out = 300
    chrome_driver.set_page_load_timeout(time_out)
    # chrome_driver.set_script_timeout(240)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒      
    # desired_capabilities = DesiredCapabilities.CHROME # 修改页面加载策略 # none表示将br.get方法改为非阻塞模式，在页面加载过程中也可以给br发送指令，如获取url，pagesource等资源。 desired_capabilities["pageLoadStrategy"] = "none"     
    # options.add_argument('--disable-gpu')        
    # options.add_argument("--disable-automation")
    # options.add_argument('--ignore-certificate-errors') 
    # options.add_experimental_option("excludeSwitches" , ["enable-automation","load-extension"])                   
    return chrome_driver    


def get_chrome_normal(submit=''):
    uas = get_ua_all()
    ua = get_ua_random(uas)
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=' + ua)
    account_lpm = luminati.get_account()
    # ip = account_lpm['IP_lpm']
    ip = '51.15.13.163'
    print(ip)
    port = 2380
    proxy = 'https://%s:%s'%(ip,str(port))
    options.add_argument('--proxy-server=%s'%proxy)    
    path_driver = get_chromedriver_path()
    print(path_driver)
    # proxy = r'http://customer-%s-cc-%s-sesstime-30:%s@  :7777' %(username, country, password))    
    chrome_driver = webdriver.Chrome(chrome_options=options,executable_path=path_driver)    
    return chrome_driver

def get_size():
    sizes = [
    [800,600],
    [1024,768],
    [1152,864],
    [1280,720],
    [1280,768],
    [1280,800],
    [1280,960],
    [1280,1024],  
    [1360,768],
    [1366,768],
    [1440,900],
    [1600,900],
    [1600,1024],
    [1680,1050],
    [1920,1080]
    ]
    size_rand_num = random.randint(0,len(sizes)-1)
    size_rand = sizes[size_rand_num] 
    return size_rand

def get_dir():
    path = os.getcwd()
    # print(path)
    path_up = path[:-3] 
    # print(path_up)
    path_download = os.path.join(path_up,'download')
    # print(path_download)
    return path_download

def clean_download():
    path_download = get_dir()
    misc_init(path_download)
    return 

def download_status():
    path_download = get_dir()
    modules = os.listdir(path_download)
    # print(mo)
    return modules

def misc_init(target_folder):
    import os
    import shutil
    import traceback
    # import globalvar    
    # clean the test result folder
    # get the current path
    current_path = target_folder
    # some folder not delete
    # except_folders = globalvar.Except_Folders
    except_folders = ['']
    # get the folder uder current path
    current_filelist = os.listdir(current_path)
    print(current_filelist)
    for f in current_filelist:
    # f should be a absolute path, if python is not run on current path
        if os.path.isdir(os.path.join(current_path,f)):
            print('------')
            if f in except_folders:
                continue
            else:
                print('++++++++++')
                real_folder_path = os.path.join(current_path, f)
                try:
                    for root, dirs, files in os.walk(real_folder_path):
                        for name in files:
                            print(name)
                            # delete the log and test result
                            del_file = os.path.join(root, name)
                            os.remove(del_file)
                            print('remove file[%s] successfully' % del_file)
                    shutil.rmtree(real_folder_path)
                    print('remove foler[%s] successfully' % real_folder_path)
                except Exception as e:
                    # traceback.print_exc()
                    print('===========')
        else:
            os.remove(os.path.join(current_path,f))

def test():
    import luminati
    submit = {}
    submit['Mission_dir'] = r'C:\EMU\emu_chromes\10000,1'
    submit['ip_lpm'] = '192.168.30.130'
    submit['port_lpm'] = 27486
    submit['Site'] = 'http://dategd.com/index.html'
    submit['Mission_Id'] = '10005'
    # luminati.refresh_proxy(submit['ip_lpm'],submit['port_lpm'])    
    chrome_driver = get_chrome_normal(submit)
    return chrome_driver
    # chrome_driver.get(submit['Site']) 
    # sleep(3000)

def test_meituan():
    url = 'https://www.google.com'
    submit = {'health': {'BasicInfo_Id': '9ba2a35e-d262-11e9-83eb-0009b6e2541a', 'country': '', 'firstname': 'Rob', 'lastname': 'Arnett', 'address': '1627 farhills ave.', 'city': 'Dayton', 'state': 'OH', 'zip': '45419.0', 'homephone': '9372567324.0', 'workphone': None, 'email': '_arnett13@peoplepc.com', 'dateofbirth': 'null', 'maritalstatus': None, 'gender': 'null', 'education': None, 'occupation': None, 'yearsatemployer': None, 'residencetype': None, 'yearatresidence': None, 'leadtype': None, 'validation': None, 'licensestate': None, 'licenseeversuspendedrevoked': None, 'abs': None, 'airbags': None, 'alarm': None, 'multivehicle': None, 'insurancecompany': None, 'coveragetype': None, 'bodilyinjury': None, 'propertydamage': None, 'collisiondeductible': None, 'comphrensivedeductible': None, 'annualmiles': None, 'year': None, 'make': None, 'model': None, 'submodel': None, 'primaryuse': None, 'ipaddress': None, 'sourceid': None, 'first_name': None, 'last_name': None, 'home_phone': None, 'work_phone': None, 'best_time_to_call': None, 'requested_loan_amount': None, 'ssn': None, 'date_of_birth': None, 'drivers_license': None, 'drivers_license_state': None, 'own_rent': None, 'years_at_residence': None, 'months_at_residence': None, 'age': None, 'military': None, 'income_type': None, 'is_dependent': None, 'net_monthly_income': None, 'years_employed': None, 'months_employed': None, 'supervisor_phone': None, 'pay_period': None, 'paycheck_type': None, 'employer': None, 'account_type': None, 'bank_name': None, 'routing_number': None, 'account_number': None, 'years_bank_account': None, 'months_bank_account': None, 'ip_address': None, 'dts': None, 'Excel_name': 'health', 'postal_code': None, 'zipcode': None, 'reference1_first_name': None, 'reference1_last_name': None, 'reference1_relationship': None, 'phone_reference1': None, 'reference2_first_name': None, 'reference2_last_name': None, 'reference2_relationship': None, 'phone_reference2': None, 'ip': None, 'title': None, 'emailaddress': None, 'phone': None, 'flag_use': 0, 'tzid': None, 'windows': None}, 'ip_lpm': '192.168.89.130', 'port_lpm': '24716', 'state_': 'OH', 'Mission_Id': '10002', 'Country': 'US', 'Site': 'https://adpgtrack.com/click/5d43f1a4a03594103a75da46/146827/233486/subaccount\n', 'Excels_dup': ['health', ''], 'Alliance': 'Adpump', 'Account': '1', 'Offer': 'GETAROUND(Done)', 'ID': 507, 'sleep_flag': 0, 'Mission_dir': 'C:\\EMU\\emu_chromes\\10002,1', 'ua': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'tz': [{'windows': 'Central Standard Time', 'tzid': 'America/Chicago'}, {'windows': 'Central Standard Time', 'tzid': 'America/Chicago America/Indiana/Knox America/Indiana/Tell_City America/Menominee America/North_Dakota/Beulah America/North_Dakota/Center America/North_Dakota/New_Salem'}]}
    # submit = {}
    submit.pop('ip_lpm')
    submit['Mission_Id'] = '10001'
    print(submit)
    return
    chrome_driver = get_chrome(submit)
    chrome_driver.get(url)
    # handle = chrome_driver.current_window_handle    
    # chrome_driver.find_element_by_xpath('//*[@id="react"]/div/div/div[1]/div[1]/div/div[2]/ul/li[7]/span/span[1]/a').click()
    sleep(3)
    # handles=chrome_driver.window_handles   
    # try:
    #     for i in handles:
    #         if i != handle:
    #             chrome_driver.switch_to.window(i)
    #             print(i)
    # except Exception as e:
    #     print(str(e))    
    sleep(3000)


def test2():
    chrome_driver = get_chrome_normal()
    chrome_driver.get('https://whoer.net')
    sleep(3000)


if __name__ == '__main__':
    test2()