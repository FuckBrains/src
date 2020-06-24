from selenium import webdriver
import winreg
from win32api import GetFileVersionInfo, LOWORD, HIWORD 
from time import sleep

def get_version_number(filename):
    #This is just for windows.
    info = GetFileVersionInfo(filename, "\\")
    #print info
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    # print('Chrome_version:',HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls))
    return HIWORD(ms)

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

def get_chrome(submit):
    options = webdriver.ChromeOptions() 
    options.add_argument('--disable-gpu')        
    options.add_argument("--disable-automation")
    options.add_argument('--ignore-certificate-errors') 
    options.add_experimental_option("excludeSwitches" , ["enable-automation","load-extension"])
    path_driver = get_chromedriver_path()  
    print('path_driver:',path_driver)  
    # ua,language,data-dir
    language = get_lan_config(submit['Country'])
    options.add_argument('-lang=' +language )            
    options.add_argument('user-agent=' + submit['ua'])
    options.add_argument('--user-data-dir='+submit['Mission_dir'])
    chrome_driver = webdriver.Chrome(chrome_options=options,executable_path=path_driver)    
    chrome_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
        "source":"""
        Object.defineProperty(navigator,'webdriver',{
            get: () => undefined
        })
        """
        })
    sleep(2)  
    return chrome_driver

def get_config():
    submit = {}
    with open('1.txt') as f:
        content = f.readlines()
    return submit

def read_country_config():
    accounts = {}
    with open('Account.ini') as f:
        lines = f.readlines()        
        for line in lines:
            if ',' in line:
                config = line.split(',')
                if config[0].upper() in accounts:
                    accounts[config[0].upper()][str(config[1])] = {}
                    accounts[config[0].upper()][str(config[1])]['ua'] = config[2] 
                else:
                    accounts[config[0].upper()] = {}
                    accounts[config[0].upper()][str(config[1])] = {}                    
                    accounts[config[0].upper()][str(config[1])]['ua'] = config[2] 

    # print(accounts)
    return accounts

def main():
    while True:
        countrys = get_all_country()
        keys = list(countrys.keys())
        for i in range(len(keys)):
            print(i+1,':',keys[i])
        for j in range(1000):
            country_number = input('please choose country number:\n') 
            if int(country_number)>len(keys):
                print('please choose right country number')
                continue
            country = keys[int(country_number)-1]
            config = read_country_config()
            # nums = config['us'].keys()
            if country in config:
                nums = list(config[country].keys())
                print('accounts in %s:'%country)
                [print(num) for num in nums]
                country_num = input('please choose account number:\n') 
                if str(country_num) not in nums:
                    print('please choose right account num')
                else:                
                    break
            else:
                print(country,'not in Account.ini,please choose again')

        submit = {}
        submit['Country'] = country
        submit['ua'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        submit['Mission_dir'] = country+str(country_num)
        print(submit)
        chrome_driver = get_chrome(submit)
        a = input('next')
        chrome_driver.close()
        chrome_driver.quit()
        # sleep(1000)    


def test():
    from faker import Factory
    for i in range(1000):
        f = Factory.create()
        ua = f.user_agent()    
        print(ua)

def test2():
    config = read_country_config()
    # nums = config['us'].keys()
    nums = list(config['us'].keys())
    print(nums)

if __name__ == '__main__':
    main()
