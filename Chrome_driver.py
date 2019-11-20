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


def get_chromedriver_path():
    return r'driver/chromedriver_77.exe'

def get_ua_all():
    uas = []
    with open(r'../res/ua.txt') as f:
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
    # print(uas[num])
    return uas[num]

def set_flag(name,value):
    gl.set_value(str(name),value)

def get_flag(name):
    flag = gl.get_value(str(name))
    return flag

def get_lan_config(country):
    country_list_code ={
    'US':'en_us',
    'GB':'en_gb',
    'AU':'en_au',
    'FR':'fr',
    'DE':'de',
    'ES':'es',
    'IT':'it',
    'PL':'pl',
    'DK':'dk'
    }
    return country_list_code[country]

def tz_test():
    c = DesiredCapabilities.CHROME # 修改页面加载策略 # none表示将br.get方法改为非阻塞模式，在页面加载过程中也可以给br发送指令，如获取url，pagesource等资源。 desired_capabilities["pageLoadStrategy"] = "none"     
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

def get_chrome(submit = None,pic=0):
    if submit == None:
        uas = get_ua_all()
        ua = get_ua_random(uas)
        print(ua)
    else:
        if 'traffic' in submit:
            desired_capabilities = DesiredCapabilities.CHROME # 修改页面加载策略 # none表示将br.get方法改为非阻塞模式，在页面加载过程中也可以给br发送指令，如获取url，pagesource等资源。 desired_capabilities["pageLoadStrategy"] = "none" 
            desired_capabilities["pageLoadStrategy"] = "none"            
            chrome_driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=desired_capabilities,executable_path=path_driver)            
            return chrome_driver
        if 'ua' in submit:
            ua = submit['ua']
        else:
            uas = get_ua_all()
            ua = get_ua_random(uas)
            print(ua)            
    options = webdriver.ChromeOptions()
    path_download = get_dir()
    prefs = {
            "download.default_directory": path_download,
             "download.prompt_for_download": False,
             # "download.directory_upgrade": True,
             # "safebrowsing.enabled": True,
             # 'profile.default_content_settings.popups': 0,
             }    
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
    if type(submit) != type(None):
        if 'Country' in submit:
            language = get_lan_config(submit['Country'])
            options.add_argument('-lang=' +language )
    if type(submit) != type(None):
        if submit['Mission_Id'] == '20000':
            print('test chrome')
        else:
            if pic == 0:
                prefs["profile.managed_default_content_settings.images"] = 2
        if 'Mission_dir' in submit:
            submit['Mission_dir'] = submit['Mission_dir'].replace('//','\\') 
            print('Selenium in using user-data-dir:',submit['Mission_dir'])
            # options.add_argument('--user-data-dir='+submit['Mission_dir'])
        if 'ip_lpm' in submit:
            account_lpm = luminati.get_account()
            ip = account_lpm['IP_lpm']
            port = submit['port_lpm']
            proxy = 'socks5://%s:%s'%(ip,port)
            options.add_argument('--proxy-server=%s'%proxy)
            print(proxy)
    # options.add_argument('--single-process')
    # options.add_argument('--process-per-tab') 
    # options.add_argument('–Referer=https://www.facebook.com') 
    options.add_experimental_option("prefs", prefs)       
    options.add_argument('--disable-gpu')        
    options.add_argument("--disable-automation")
    options.add_experimental_option("excludeSwitches" , ["enable-automation","load-extension"])
    path_driver = get_chromedriver_path()
    chrome_driver = webdriver.Chrome(chrome_options=options,executable_path=path_driver)
    # chrome_driver = webdriver.Chrome(chrome_options=options,desired_capabilities=desired_capabilities)
    chrome_driver.set_page_load_timeout(300)
    # chrome_driver.set_script_timeout(240)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒  
    size = get_size()
    print('Chrome size:',size)
    chrome_driver.set_window_size(size[0],size[1])
    chrome_driver.maximize_window()    
    return chrome_driver

def get_chrome_normal(submit):
    uas = get_ua_all()
    ua = get_ua_random(uas)
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=' + ua)
    account_lpm = luminati.get_account()
    ip = account_lpm['IP_lpm']
    port = submit['port_lpm']
    proxy = 'socks5://%s:%s'%(ip,port)
    options.add_argument('--proxy-server=%s'%proxy)    
    path_driver = get_chromedriver_path()
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
    submit['ip_lpm'] = '192.168.30.131'
    submit['port_lpm'] = 24000
    submit['Site'] = 'http://dategd.com/index.html'
    submit['Mission_Id'] = '10005'
    # luminati.refresh_proxy(submit['ip_lpm'],submit['port_lpm'])    
    chrome_driver = get_chrome_normal(submit)
    chrome_driver.get(submit['Site']) 
    sleep(3000)

def test_meituan():
    url = 'https://hz.meituan.com'
    path_driver = get_chromedriver_path()
    chrome_driver = webdriver.Chrome(executable_path=path_driver)
    chrome_driver.get(url)
    handle = chrome_driver.current_window_handle    
    chrome_driver.find_element_by_xpath('//*[@id="react"]/div/div/div[1]/div[1]/div/div[2]/ul/li[7]/span/span[1]/a').click()
    sleep(3)
    handles=chrome_driver.window_handles   
    try:
        for i in handles:
            if i != handle:
                chrome_driver.switch_to.window(i)
                print(i)
    except Exception as e:
        print(str(e))    
    sleep(3000)



if __name__ == '__main__':
    tz_test()