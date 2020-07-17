import requests
import json
import db
# import test
# import ssn_detect
import Chrome_driver
from time import sleep
# import urllib2
import re
import threadpool
import threading  
import Submit_handle as st

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
    import luminati_main

    luminati_main.change_update_file()

def test_22(submit):
    url = 'https://weibo.com/u/5818390567/home?wvr=5&sudaref=graph.qq.com'
    chrome_driver = Chrome_driver.get_chrome() 
    chrome_driver.get(url)
    xpath_name = '//*[@id="loginname"]'
    xpath_pwd = '//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input'
    xpath_captcha = '//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input'

    name = submit['name']
    pwd = submit['pwd']
    # code
    # chrome_driver.find_element_by_xpath()

def test22():
    import Submit_handle
    for i in range(1000):
        course = Submit_handle.get_courses(1)
        print(course)


def test23():
    import traffic as tf
    tf.main(i)


def test24():
    import db
    excel = 'Us_pd_native2'
    tx = r'..\\res\routings.txt'
    # with open(tx) as f:
    #     lines = f.readlines()
    # routing = []
    # for line in lines:
    #     rout = line.split('----')
    #     rout[1] = rout[1].replace('\n','')
    #     routing.append(rout)
    routing = db.get_routing(excel)
    print(routing)
    # content = ''
    # for rout in routing:
    #     content+=rout['BasicInfo_Id']+'----'+rout['routing_number']+'\n'
    # with open(r'..\\res\routings.txt','w') as f:
    #     f.write(content)
    # return
    import ssn_detect as st

    sql_contents = []
    for rout in routing[0:10]:
        # flag = st.validate_routing_123(rout[1])
        flag = st.validate_routing_123(rout['routing_number'])

        # sql_content = "UPDATE BasicInfo SET routing_alive = '%d' WHERE Basicinfo_Id = '%s'" % (flag,rout[0])
        sql_content = "UPDATE BasicInfo SET routing_alive = '%d' WHERE Basicinfo_Id = '%s'" % (flag,rout['BasicInfo_Id'])

        # print(sql_content)
        sql_contents.append(sql_content)
    db.Execute_sql([sql_content])

def test25():
    sql_content = "SELECT * FROM mission WHERE TO_DAYS( NOW( ) ) - TO_DAYS(Create_time) <= 2;"
    res = db.Execute_sql_single([sql_content])
    print(len(res))
    # print(res[0][0:3])
    mission_dict = {}
    for res_content in res[0]:
        if str(res_content[0]) not in mission_dict:
            mission_dict[str(res_content[0])] = 1
        else:
            mission_dict[str(res_content[0])] += 1
    print(mission_dict)

def makedir_state(path=r'D:\\'):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)

def test26():
    import Chrome_driver
    import json
    import re
    submit = {}
    # submit['Mission_dir_flag'] = 1
    submit['Mission_Id'] = 10002
    # submit['Mission_dir'] = r'c:\\EMU\\test'
    # makedir_state(submit['Mission_dir'])
    submit['port_lpm'] = 24002
    submit['ip_lpm'] = '192.168.0.1' 
    submit['traffic'] = 1
    # chrome_driver = Chrome_driver.get_chrome_test(submit)
    url = 'http://aleadstrack.go2cloud.org/aff_c?offer_id=142&aff_id=1629'
    # url = 'http://zh.moneymethods.net/click.php?c=55&key=q67c1kcvg42g19r5w83690tg'
    chrome_driver = Chrome_driver.get_chrome(submit,pic=0)        

    # url = 'https://www.baidu.com'
    chrome_driver.get(url)
    for i in range(60):
        if 'https://www.123cashnow.com/' in chrome_driver.current_url:
            break
        else:
            sleep(1)
    cookies = chrome_driver.get_cookies()
    print(type(cookies))
    cookie_str = json.dumps(cookies)  
    print(cookie_str)
    chrome_driver.close()
    chrome_driver.quit()    
    return  
    chrome_driver.delete_all_cookies()        
    url2 = 'http://gm.ad3game.com/click.php?c=38&key=29tdur732878n465zf3p8ym0'


    chrome_driver = Chrome_driver.get_chrome(submit,pic=1)    
    chrome_driver.get(url2)



def test27():
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.107'
    }
    s = requests.session()
    url = 'http://zh.moneymethods.net/click.php?c=55&key=q67c1kcvg42g19r5w83690tg'
    res = s.get(url,headers=headers)
    sleep(10)
    cookies = res.cookies.get_dict()
    print(cookies)
    s.close()

def test28():
    cookies = json.loads(submit['Cookie'])
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry']) 
        chrome_driver.add_cookie(cookie)    
    chrome_driver.get('http://stripchat.com')

def test29():
    import luminati
    url = 'http://aleadstrack.go2cloud.org/aff_c?offer_id=142&aff_id=1629'
    port =24002
    luminati.get_lpm_cookie(port,url)


def test30():
    chrome_driver = Chrome_driver.get_chrome_remote() 
    # js = 'return navigator;'
    js = '''
    var myArray=new Array();
    var i = 0;
    for (prop in navigator)
    {
        myArray[i] = prop;
        i = i+1;
    # document.write("属性 '" + prop + "' 为 " + navigator[prop]);
    };
    return myArray;
    '''
    # print(js)
    # js = "return console.log('user changed navigator.userAgent,real one:',navigator.plugins)"
    chrome_driver.get('https://www.baidu.com')
    num = chrome_driver.execute_script(js)
    print(num)

def test31():
    import luminati
    blacklist = luminati.read_blacklist()
    # print(blacklist)
    # for key in data_proxy_config['jia10']['rules']:
    #     print(key,':',data_proxy_config['jia10']['rules'][key]) 
        # for item in 
    proxy_config_name = 'jia10'
    Mission_Id = '10002'
    data = {}
    data_proxy_config = luminati.read_proxy_config()
    data_proxy_config[proxy_config_name]['rules'] = data_proxy_config['jia10']['rules']
    # print(data_proxy_config)
    if str(Mission_Id) in blacklist:
        # {'type':mission[1],'url_key':mission[2]}
        if blacklist[Mission_Id]['type'] != '':
            print(data_proxy_config[proxy_config_name]['rules'])
            data_proxy_config[proxy_config_name]['rules'][0]['url'] = data_proxy_config[proxy_config_name]['rules'][0]['url'].replace(')',blacklist[Mission_Id]['type']+')')
        if blacklist[Mission_Id]['url_key'] != '':
            data_proxy_config[proxy_config_name]['rules'][1]['url'] = blacklist[Mission_Id]['url_key']
        else:
            data_proxy_config[proxy_config_name]['rules'].pop(1)
    else:
        data_proxy_config[proxy_config_name]['rules'].pop(1)
    data['proxy'] = data_proxy_config[proxy_config_name]
    print('preparing to add proxy config:',data_proxy_config[proxy_config_name])    

    # [{"action": {"null_response": true},"action_type": "null_response","trigger_type": "url","url": "\\.(mp3|jpg|jpeg|png|mp4|gif|ico|google|zoho)"},{"action": {"null_response": true},"action_type": "null_response","trigger_type": "url","url": "lr-ingest.io|testimonialtree.com"}],    

def test32():
    import Auto_update
    Auto_update.clean_ports()

def test33():
    import luminati
    port = 24855
    for i in range(3):
        try:
            luminati.delete_port_s(port)            
        except:
            pass
        # port_new = luminati.get_port_random()
        # print('port_new:',port_new)
        # db.update_port(4965,port_new)
        # print('update port success')
        # # print(port_new)
        # try:
        #     # proxy_config_name_list = ['jia1','jia2'] 
        #     # num_proxy = random.randint(0,1)
        #     luminati.add_proxy(port_new,country='us',proxy_config_name='jia10',ip_lpm='192.168.188.141',Mission_Id='10104')
        # except Exception as e:
        #     a = traceback.format_exc()
        #     print(a)    
        # port = port_new

def test34():
    import Submit_handle as sb
    day = sb.get_next_payday_mm_signum('')
    print(day)


def test36():
    import db
    excel = 'Us_pd_native2'
    tx = r'..\\res\routings.txt'
    # with open(tx) as f:
    #     lines = f.readlines()
    # routing = []
    # for line in lines:
    #     rout = line.split('----')
    #     rout[1] = rout[1].replace('\n','')
    #     routing.append(rout)
    routing = db.get_routing(excel)
    # print(routing)
    # content = ''
    # for rout in routing:
    #     content+=rout['BasicInfo_Id']+'----'+rout['routing_number']+'\n'
    # with open(r'..\\res\routings.txt','w') as f:
    #     f.write(content)
    # return
    import ssn_detect as st
    import Submit_handle as sb

    sql_contents = []
    submit = {}
    for rout in routing[0:100]:
        # flag = st.validate_routing_123(rout[1])
        submit['routing_number'] = rout['routing_number']
        routing = sb.get_routing_number_verify(submit)
        # print(rout,routing_number)
        continue
        # sql_content = "UPDATE BasicInfo SET routing_alive = '%d' WHERE Basicinfo_Id = '%s'" % (flag,rout[0])
        sql_content = "UPDATE BasicInfo SET routing_alive = '%d' WHERE Basicinfo_Id = '%s'" % (flag,rout['BasicInfo_Id'])

        # print(sql_content)
        sql_contents.append(sql_content)
    # db.Execute_sql([sql_content])

def test35():
    import ssn_detect
    routing = '751929126'
    ssn_detect.validate_routing_10104(routing)    

def test37():
    import emaillink
    content = '''
    Error time: 03/07/2020 4:36pm
    plan_id:3
    Mission_id:10000,10001
    Error:      Sending traffic errot,luminati can't open port,need check 
    '''
    emaillink.email_alert(content)

pool = threadpool.ThreadPool(10)

def test38():
  
    import de_gen
    plans = [i for i in range(19,500)]
    requests = threadpool.makeRequests(de_gen.main, plans)
    [pool.putRequest(req) for req in requests]
    pool.wait()     

def test39():
    import datetime
    now = datetime.datetime.now()
    t = now.strftime('%c')   
    print(t)
    error = 'traffic error'
    plan_id  = '3'
    content = '''
    Error time: %s
    plan_id:%s
    Mission_id:10000,10001
    Error:      Sending traffic errot,luminati can't open port,need check 
    '''%(str(t),plan_id)
    print(content)


def test40():
    import luminati
    config = luminati.read_proxy_config()
    print(config)

def test41():
    submit = {}
    submit['email'] = 'asd@gmx.de'
    submit['name'] = 'F?rster Heinz'
    submit['dateofbirth'] = '02.03.1995'
    email = st.get_email(submit)
    print(email)

def test42():
    submit = {}
    submit['id_number'] = '4810690468<<D<<9602120<2702124<<<<<<<8'
    id_number = st.get_id_number(submit)
    print(id_number)

def test43():
    import de_gen
    import re
    zipcode = 11111
    content = de_gen.get_city(zipcode)
    reg_contents_pattern = r'<tr><td >'+str(zipcode)+r'</td><td >(.*?)</td><td >(.*?)</td><td >'
    reg_contents= re.findall(reg_contents_pattern,content,re.S)
    print(reg_contents)
    # reg_contents = [reg.strip() for reg in reg_contents]   

def test44():
    submit = {}
    submit['city'] = 1
    submit['zipcode'] = 1
    Submit_handle.get_city(submit)

def test45(submit):
    # citys = citys[0:5]
    city,state = st.get_city(submit)
    print(city,state,'is ready to upload')
    # if submit['city_byzip']!=''and submit['city_byzip'] != None:
    #     continue
    sql_content = 'UPDATE Basicinfo SET city_byzip = "%s" , state = "%s" WHERE BasicInfo_Id = "%s"'%(city,state,submit['BasicInfo_Id'])
    # sql_contents.append(sql_content)
    db.Execute_sql([sql_content])

# pool = threadpool.ThreadPool(7)

def test46():
    citys = db.handele_city()
    print(citys[0])
    citys = [submit for submit in citys if submit['state'] == '']
    print(citys)
    requests = threadpool.makeRequests(test45, citys)
    [pool.putRequest(req) for req in requests]
    pool.wait()             

def combine_deinfo():
    pass

def test47():
    import de_gen
    phones = db.get_phones_de()
    for phone in phones[:100]:
        phone_ = phone['phone'].replace('(','').replace(')','').replace('-','').replace(' ','')
        url = 'https://www.congstar.de/checkout/api/area-code/%s'%(phone_[:5])
        content = de_gen.pickup(url)
        print(phone_[:5],'----',content)



if __name__ == '__main__':
    test47()

