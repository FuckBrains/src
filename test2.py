import db
# import test
# import ssn_detect
import Chrome_driver
from time import sleep
# import random
# from selenium import webdriver
# import Submit_handle

# def test_1():
#     Mission_Id =10095
#     pages = db.get_page_flag(Mission_Id)
#     print(pages)

# def test_10088():
#     email = 'ag_1977@live.com'    
#     ssn_detect.validate_10088_email(email)

# def test_2():
#     chrome_driver = Chrome_driver.get_chrome()
#     url = 'http://falbk.top/click.php?c=5&key=yift22rta15kfnq9upqfowq9'
#     chrome_driver.get(url)
#     sleep(1000)

# def test_3():
#     sql_content = 'Select Basicinfo_Id,home_phone,work_phone from Basicinfo where Excel_name="Us_pd_native"'
#     response = db.Execute_sql_single([sql_content])    
#     # print(response)
#     excels = [[key[0],key[1]] for key in response[0] if key[1]==key[2]]
#     print(excels)
#     print(len(excels))
#     sql_contents = []
#     for key in excels: 
#         phone = key[1]
#         for i in range(15):
#             num = random.randint(0,9) 
#             if int(phone[-3])!= num:
#                 print(phone[-3],num)
#                 phone = phone[:-3]+str(num)+phone[-2:]
#                 print(phone)
#                 break
#         sql_content = "UPDATE Basicinfo SET work_phone = %s WHERE Basicinfo_Id = '%s'" % (phone,key[0])
#         sql_contents.append(sql_content)
#     db.Execute_sql(sql_contents)    
#     # print(excels)
#     # sql_contents = []
#     # for excel in excels:
#     #     sql_content = 'SELECT * from BasicInfo  WHERE Excel_name = "%s"'%excel
        
#     #     response = db.Execute_sql_single(sql_content)

# def test_4():
#     info = {'Alliance_name': 'Convert2Media', 'Number of Offers': '4000+', 'Commission Type': 'CPA, CPL, CPI, Pay per call', 'Minimum Payment': '$100', 'Payment Frequency': 'Net-15,Weekly', 'Payment Method': 'Check,PayPal,Wire,Payoneer,Direct Deposit', 'Referral Commission': 'N/A', 'Tracking Software': 'CAKE', 'Tracking Link': 'http://clickztrax.com/?a=', 'Skypes': 'publishers@convert2media.com,1-800-689-1260', 'alliance_url': 'http://www.convert2media.com/'}    
#     print(info)
#     keys_detect = ['Alliance_name','Skypes','Number of Offers','Commission Type','Minimum Payment','Payment Frequency','Payment Method','Referral Commission','Tracking Software','Tracking Link']
#     for key in keys_detect:
#         if key not in info:
#             print(key,'of info not in keys of database')
#             info[key] = ''
#     Alliance_name = info['Alliance_name']
#     print(Alliance_name)    
#     sql_contents = ['use emu','show tables','INSERT IGNORE INTO alliances(Alliance_name,Skypes,NumberofOffers)values("%s","%s","%s")'%("test",'111','222')]
#     db.Execute_sql(sql_contents)
#     # infos = [info]
#     # db.upload_alliance_info(infos) 

# def test_oxylabs():
#     import urllib.request
#     import random
#     username = 'r782992280'
#     password = 'nV3nqFtt9S'
#     country = 'us'
#     session = random.random()
#     entry = ('http://customer-%s-cc-%s-sesstime-30:%s@pr.oxylabs.io:7777' %
#         (username, country, password))
#     query = urllib.request.ProxyHandler({
#         'http': entry,
#         'https': entry,
#     })
#     execute = urllib.request.build_opener(query)
#     for i in range(3000):
#         print(i+1)
#         print(execute.open('https://ipinfo.io').read())
#         sleep(5)

# def test_chrome():
#     from selenium.webdriver.common.proxy import ProxyType, Proxy

#     options = webdriver.ChromeOptions()
#     # options.add_argument('user-agent=' + ua)
#     # account_lpm = luminati.get_account()
#     # ip = account_lpm['IP_lpm']
#     # print(ip)
#     # port = submit['port_lpm']
#     # proxy = 'socks5://%s:%s'%(ip,str(port))
#     path_driver = Chrome_driver.get_chromedriver_path()
#     print(path_driver)
#     username = 'r782992280'
#     password = 'nV3nqFtt9S'
#     country = 'us'    
#     # proxy = 'http://customer-%s-cc-%s-sesstime-30:%s@pr.oxylabs.io:7777'%(username, country, password)   
#     super_proxy_url = 'http://customer-%s-cc-%s-sesstime-30:%s@pr.oxylabs.io:7777'%(username, country, password)  
#     # proxy = 'http://lum-customer-%s-zone-%s-session-%s:%s@zproxy.superproxy.io:22225'%(username,zone_name,session_id,password,port)
#     print(super_proxy_url)
#     proxy = Proxy({
#         'proxyType': ProxyType.MANUAL,
#         'httpProxy': super_proxy_url,
#         'ftpProxy': super_proxy_url,
#         'sslProxy': super_proxy_url,
#         'noProxy': ''  # set this value as desired
#     })    
#     options.add_argument('--proxy-server=%s'%proxy)    
#     chrome_driver = webdriver.Chrome(chrome_options=options,executable_path=path_driver)    
#     return chrome_driver    


# def test_chrome_proxy():
#     from seleniumwire import webdriver
#     url = 'https://whoer.net'
#     url = 'http://nc.fclitloan.com/click.php?c=7&key=m3rtj910vwn88z4er5rnaksa'
#     # url = 'http://lumtest.com/myip.json'
#     country = 'us'
#     username = 'r782992280'
#     password = 'nV3nqFtt9S'    
#     entry = 'customer-%s-cc-%s-sesstime-30-sessid-abcde143345:%s@us-pr.oxylabs.io:10000' %(username, country, password)
#     wire_options = {
#         'proxy': {
#             'http': 'http://'+entry,
#             'https': 'https://'+entry,
#             'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
#         },
#         # 'port': 12345,
#         # 'verify_ssl': False
#     }      
#     path_driver = Chrome_driver.get_chromedriver_path()    
#     chrome_driver = webdriver.Chrome(seleniumwire_options=wire_options,executable_path=path_driver)
#     chrome_driver.get(url)
#     sleep(3000)

import os
import zipfile
from selenium import webdriver
PROXY_HOST = 'pr.oxylabs.io'  # rotating proxy or host
PROXY_PORT = 8080 # port
PROXY_USER = 'customer-r782992280-cc-us-sesstime-30-sessid-ae1243345' # username
PROXY_PASS = 'nV3nqFtt9S' # password
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""
background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    path_driver = Chrome_driver.get_chromedriver_path()    
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=path_driver)        
    # driver = webdriver.Chrome(
    #     os.path.join(path, 'chromedriver'),
    #     chrome_options=chrome_options)
    return driver

def main():
    driver = get_chromedriver(use_proxy=True)
    #driver.get('https://www.google.com/search?q=my+ip+address')
    url = 'http://nc.fclitloan.com/click.php?c=7&key=m3rtj910vwn88z4er5rnaksa'
    driver.get('https://httpbin.org/ip')
    sleep(3000)

def test_email_10088():
    import ssn_detect as dt
    email = '123@hotmail.com'
    dt.validate_10088_email3(email)

def version_test():
    files = os.listdir('.')
    print(files)
    if 'Auto_update2.pyc' in files:
        # print(modules)
        file = os.path.join(os.getcwd(),'Auto_update.pyc')
        file2 = os.path.join(os.getcwd(),'Auto_update2.pyc')
        os.remove(file)
        os.rename(file2,file)
    # modules_path = [os.path.join(path,file) for file in modules]    

def compile_test():
    import Compile
    modules_path = Compile.get_modules()
    print(modules_path)

    # delete them all
    [os.remove(file) for file in modules_path]
    sleep(1)

    # compile the src dir
    os.system('python -m compileall')
    sleep(2)

    # get all compiled file abs path in dir'__pycache__'/    
    modules_path = Compile.get_modules()    
    # remove mission files
    [os.remove(file) for file in modules_path if 'Mission' in file]
    sleep(1)

    # get all file names in dir '__pycache__'/
    modules = os.listdir('__pycache__/')
    # rename all these files so that they can run everywhere
    print(modules)
    [Compile.rename_file(module) for module in modules]    

def test12():
    Mission_Id = 10123
    db.read_pic(Mission_Id)    

def test13():
    account = db.get_account()
    # print(account)
    conn,cursor = db.login_sql(account)
    sql_content = 'DELETE FROM Log LIMIT 100;'

    for i in range(70):
        # print('\n\n\n')
        # print(sql_content)

        try:
            res = cursor.execute(sql_content)
            # response = cursor.fetchall()
            # print(response)
        except Exception as e:
            print(str(e))
            pass
        # print(response)
    db.login_out_sql(conn,cursor)    

def test14():
    import Submit_handle
    date_ = Submit_handle.get_next_payday_bi_str()
    print(date_)

def test15():
    import datetime
    starttime = datetime.datetime.utcnow() 
    time_now = str(starttime).split('.')[0].replace(' ','').replace(':','')     
    print(time_now)

def test16():
    zip_= '95370.0'
    state = db.get_state_byzip(zip_)
    print(state)

def test17():
    import Chrome_driver
    from selenium.webdriver.support import expected_conditions as EC
    url = 'https://healthinsurance.net/hi_wizard/?token=191046011-QwVV9kxT_XLPVN2czFoszebaou87yzqHoCMMs1TfxY8znCDwe1Tq2jqYsvi5kwgg#health/Cover_Spouse'
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get(url)
    xpath = '//*[@id="plate-content"]/div[1]'
    element = chrome_driver.find_element_by_xpath(xpath)
    text = 'Are you looking to include your spouse in your Health Insurance plan?'
    # print(element.getText())    
    # print(element.innerHTML)
    # print(element.text)
    # if text in chrome_driver.page_source:                
        # print(page,'find text:',element.text)
    xpath2 = '//*[@id="plate-content"]/div[2]/div[2]/button'
    element2 = chrome_driver.find_element_by_xpath(xpath2)
    element2.click()
    # print(page,'find text:',element.text)
    while True:
        # element2 = chrome_driver.find_element_by_xpath(xpath2)
        try:
            if element.text == text:
            # if EC.text_to_be_present_in_element(element,text):
                print("%s still in chrome_driver.page_source,page not changed"%text)            
                sleep(2)
            else:
                print("page['Flag_text'] not visibile in page,page changed!!!!!!!!!!!")                
                break
        except Exception as e:
            print("page['Flag_text'] not visibile in page,page changed!!!!!!!!!!!")                
            break



    sleep(1000)




def test18():
    import Auto_update    
    modules = Chrome_driver.download_status()
    names = ['emu_multi-src-master.zip','emu_multi-src-src-master.zip']
    module_name = ''
    for module in modules:
        if module in names:
            module_name = module
            print('Find zip src')
            sleep(3)
            flag = 1
            break
        else:
            pass
    Auto_update.test_zip(module_name)

def test19():
    import Auto_update
    info = Auto_update.get_updateinfo()
    print(info)

def test20():
    submit = {}
    submit['work_phone'] = '123456789'
    import Submit_handle
    phone = Submit_handle.get_workphone_unique(submit)
    print(phone)

def test21():
    a = 150/50
    print(int(a))

if __name__ == '__main__':
    test21()    

    

# def get_employer():
#     submit = {
#         'employer':'aaaa'
#     }
#     employer = Submit_handle.get_employer_info(submit)
#     return employer
#     # employer = [key[0] for key in res]
#     # print(len(employer))
#     # print('first 10')
#     # print(employer[:10])
#     # print('last time')
#     # print(employer[-10:])


# def main():
#     # test_10088()
#     # test.test_write()
#     email = 'ricdevin@yahoo.com'
#     # email=''
#     # ssn_detect.validate_10088_email(email)
#     routing = '2857880817'
#     ssn_detect.validate_routing(routing)
#     # Address = '237 BURNING TREE DRIVE'
#     # ZipCode = 95119
#     # ssn_detect.validate_address(Address,ZipCode)

# if __name__ == '__main__':
#     test_chrome_proxy()