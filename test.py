import selenium_funcs
from win32api import GetFileVersionInfo, LOWORD, HIWORD 
import time
import time_related
import socket
import Alliance_login
import os
import json
import threading
import threadpool
import random
pool = threadpool.ThreadPool(5)
Falg_threads = 0
import Chrome_driver
from time import sleep
import psutil
import db
import luminati
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests



def read_ini():
    file = r'Offer_conf.ini'
    submits = []
    with open(file,'r') as f:
        jss = f.readlines()
        # print(jss)
        for js in jss:
            submit = json.loads(js)
            submits.append(submit)
            # print(submit)
    if len(submits) >= 1:
        return submits[-1]
    else:
        return []


def write_ini(content):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    file = r'Offer_conf.ini'
    content = json.dumps(content) 
    with open(file,'w') as f:
        # content += '\n'
        f.write(content)

def add_missiion(Mission_conf):
    Mission_conf[0]

def test_plan_status():
    a = '''
  File \"C:\\EMU\\src\\thread_tokill.py\", line 149, in reg_part
  File \"C:\\EMU\\src\\Mission_10029.py\", line 91, in web_submit
    chrome_driver.find_element_by_xpath(\'//*[@id=\"postcode\"]\').send_keys(postcode)
  File \"C:\\Users\\chao\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\selenium\\webdriver\\remote\\webelement.py\", line 479, in send_keys
    \'value\': keys_to_typing(value)})
  File \"C:\\Users\\chao\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\selenium\\webdriver\\remote\\webelement.py\", line 633, in _execute
    return self._parent.execute(command, params)
  File \"C:\\Users\\chao\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\selenium\\webdriver\\remote\\webdriver.py\", line 321, in execute
    self.error_handler.check_response(response)
  File \"C:\\Users\\chao\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\selenium\\webdriver\\remote\\errorhan    
    '''
    print(len(a))




def main():
    offer_conf = {
    '10000':'',
    '10001':'',
    '10002':'Auto'
}
    write_ini(offer_conf)
    offer_conf = read_ini()
    print(offer_conf)


def multi_test(submit):
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get('http://www.baidu.com')
    print('ppppppppp')
    sleep_time = random.randint(100,300)
    sleep(sleep_time)
    chrome_driver.quit()    
    global Falg_threads
    Falg_threads += 1
    print('Falg_threads:',Falg_threads)


def killpid():
    pids = psutil.pids()
    print(pids)
    for pid in pids:
        try:
            p = psutil.Process(pid)
        except:
            continue
        kill_list = ['chrome.exe','chromedriver.exe','Client.exe','Monitor.exe','MonitorGUI.exe','Socket.exe']
        for key in kill_list:
            if p.name() == key:
                cmd = 'taskkill /F /IM '+key
                try:
                    os.system(cmd)            
                except:
                    pass


def test():
    for i in range(5):
        # global Falg_threads
        Falg_threads=0
        submits = ['','','','']
        requests = threadpool.makeRequests(multi_test, submits)
        [pool.putRequest(req) for req in requests]
        print('1111111111111111')
        pool.wait()   
        flag_next = len(submits) 
        killpid() 
        # while True:
        #     if Falg_threads >= flag_next:
        #         break
        #     else:
        #         print('++++++++++++++++=================')
        #         print('Falg_threads:',Falg_threads)
        #         sleep(10)


def makedir_download(path=r'c:\emu_download'):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)



def clean_download():
    modules = os.listdir(r'c:\emu_download')
    # print(modules)
    path = os.path.join(os.getcwd(),r'c:\emu_download')
    modules_path = [os.path.join(path,file) for file in modules]
    print(modules_path)
    [os.remove(file) for file in modules_path]    
    return 


def test_rest():
    Mission_list = ['10005']
    Excel_name = ['','Email']
    Email_list = ['hotmail.com','aol.com','outlook.com','yahoo.com']
    rest = db.read_rest(Mission_list,Excel_name,Email_list)
    print(rest)


def test_coding():
    import Auto_update
    Auto_update.read_account()

def test_html():
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get('https://trk.hracmp.com/click?pid=190&offer_id=2492')
    sleep(3000)



def test_db():
    plans = db.read_plans(1)
    print(plans)


def test_ip():
    myname = socket.getfqdn(socket.gethostname(  ))
    print(myname)
    myaddr = socket.gethostbyname(myname)
    print(myaddr)

def test_luminati():
    ip = '192.168.30.131'
    port = 24000
    luminati.get_lpm_ip(ip,port)

def test_chrome_luminati():
    import importlib
    plans = db.read_plans(10)
    print(plans)
    # return
    submit = db.get_luminati_submit(plans[0])
    print(submit)
    module = 'Mission_'+submit['Mission_Id']
    Module = importlib.import_module(module)     
    luminati.ip_test(submit['ip_lpm'],submit['port_lpm'],state=submit['state_'] ,country='')             
    Module.web_submit(submit) 

def test_cam4():
    import Mission_10005
    url = Mission_10005.test_url()
    print(url)
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get('https://google.com')
    handle = chrome_driver.current_window_handle    
    url = 'http://www.cam4.com/signup/confirm?uname=Lara382&rcode2=7d73751b-d916-495b-baa8-a8a05bfb9b8e'
    # url = 'https://google.com'
    # url = url.replace('\n','').replace(' ','')
    # print(url)
    try:
        newwindow='window.open("' + url + '");'
        chrome_driver.execute_script(newwindow)
    except Exception as e:
        print(str(e))    
    handles=chrome_driver.window_handles   
    try:
        for i in handles:
            if i != handle:
                chrome_driver.switch_to.window(i)
                cookies = chrome_driver.get_cookies()
                cookie_str = json.dumps(cookies)
                print(cookie_str)
                submit['Cookie'] = cookie_str
                db.update_cookie(submit)
                chrome_driver.refresh() 
                cookies = chrome_driver.get_cookies()
                cookie_str = json.dumps(cookies)
                submit['Cookie'] = cookie_str
                db.update_cookie(submit)  
                sleep(10)   
    except Exception as e:
        print(str(e)) 

    sleep(10)
    # try:
    #     chrome_driver.execute_script(newwindow)   
    #     sleep(20) 
    #     print('======')
    # except Exception  as e:
    #     print(str(e))

def get_uspd():
    print('     Start reading info from sql server...')
    account = db.get_account()
    conn,cursor=db.login_sql(account)
    print('     Login success')    
    Excel_name = 'Uspd'
    res = cursor.execute('SELECT * from BasicInfo WHERE Excel_name="%s"'%Excel_name)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
    return Mission_dict 

pool = threadpool.ThreadPool(5)

import ssn_detect as dt

def test_write():     
    import traceback
    Mission_dict = get_uspd()
    print('Total',len(Mission_dict),'info')
    # account = db.get_account()

    length = len(Mission_dict)
    submits = []
    for j in range(length):
        submit = {}
        submit['Alliance'] = ''
        submit['Account'] = ''
        submit['ua'] = ''        
        submit['num'] = j
        print('Number',j,'sending....')
        submit['Uspd'] = Mission_dict[j]
        submits.append(submit)
    print('Total',len(submits),'infos')
        # try:
        #     flag = dt.validate_10088_email(submit['Uspd']['email'])
        #     print(flag)
        #     if str(flag) not in flags:
        #         flags[str(flag)] = 0
        #     else:
        #         flags[str(flag)] += 1
        #     if flag == 3:
        #         print('used info')
        #         db.write_one_info([str(10088)],submit)
        #     else:
        #         print('good info')
        #     print(flags)                
        # except:
        #     a = traceback.format_exc()
        #     print(a)
        #     continue
    requests = threadpool.makeRequests(Mission_10088_test, submits)
    [pool.putRequest(req) for req in requests]
    pool.wait()

def Mission_10088_test(submit):
    print('Sending',submit['num'],'info')
    try:
        flag = dt.validate_10088_email(submit['Uspd']['email'])
        print(flag)
        if flag == 3:
            print('Number',submit['num'],'is used info')
            db.write_one_info([str(10088)],submit)
        else:
            print('Number',submit['num'],'is good info')
    except:
        pass
        # a = traceback.format_exc()
        # print(a)    

def test_update():
    submit = {}
    a = [{'domain': 'cam4.com', 'expiry': 1630934096, 'httpOnly': False, 'name': '_sp_id.dd07', 'path': '/', 'secure': False, 'value': 'e497019a-0f13-4764-ac43-0b5d98bdf50f.1567861983.1.1567862096.1567861983.4fc0c574-99b2-4a1a-a93b-ce2e4ad4a081'},{'domain': 'cam4.com', 'expiry': 1568466874.109413, 'httpOnly': True, 'name': 'cam4-AH', 'path': '/', 'secure': False, 'value': 'ACED000577C1025485140008416973686139313500A24C427054667A73373844614568457A5376523669614A42476644475645395234575F745F647039716B626971646E54585A494C76645F397637326E6D567A55386B5431502D7542644C38537364554D65434C6772337937365667546B55785949453563756372627A67476548526C4F4A6E74557A5A4D6137415153414E74704575326C5F6347363964326E347A4D426132674C326265566665634E53377264747241000D32342E3136372E34362E323334'}, {'domain': 'cam4.com', 'expiry': 1599397983, 'httpOnly': False, 'name': '_hjid', 'path': '/', 'secure': False, 'value': 'adea4704-9c34-4b8e-88f4-857efa3af2b2'}, {'domain': 'cam4.com', 'expiry': 1575638102, 'httpOnly': False, 'name': '_fbp', 'path': '/', 'secure': False, 'value': 'fb.1.1567861990996.158212413'}, {'domain': 'cam4.com', 'expiry': 1567863896, 'httpOnly': False, 'name': '_sp_ses.dd07', 'path': '/', 'secure': False, 'value': '*'}, {'domain': 'cam4.com', 'expiry': 1630934097, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.2046153849.1567861983'}, {'domain': 'cam4.com', 'expiry': 1599484493, 'httpOnly': False, 'name': '_vwo_uuid_v2', 'path': '/', 'secure': False, 'value': 'D42AD4F73B0A62B717CB0AEBF89B4F951|d9ec1d3187326a4adeb9a5389e5a8963'}, {'domain': 'cam4.com', 'expiry': 1570453979.61263, 'httpOnly': False, 'name': 'cam4-AF', 'path': '/', 'secure': False, 'value': 'hasOffers_102610b212d6b67e781164abeb539c_153_155'}, {'domain': 'cam4.com', 'expiry': 1567948497, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.1238157969.1567861983'}, {'domain': 'www.cam4.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/', 'secure': True, 'value': 'web13-ams~B9D55E2299A5CD372E06113510ACC29C'}, {'domain': 'cam4.com', 'expiry': 1575637978, 'httpOnly': False, 'name': '_gcl_au', 'path': '/', 'secure': False, 'value': '1.1.668160887.1567861979'}, {'domain': 'www.cam4.com', 'httpOnly': False, 'name': 'cam4-tipGetBalanceAction', 'path': '/signup', 'secure': False, 'value': '%257B%2522status%2522%253A%25221%2522%252C%2522userbalance%2522%253A%25220%2522%257D'}, {'domain': 'cam4.com', 'expiry': 1570009558.109669, 'httpOnly':True, 'name': 'UAF', 'path': '/', 'secure': False, 'value': 'f195e19a-5e08-4753-aeb0-6d473f26ad82'}, {'domain': 'cam4.com', 'expiry': 1583413978, 'httpOnly': False, 'name': 'optimizelyEndUserId', 'path': '/', 'secure': False, 'value': 'oeu1567861978439r0.23604464349446697'}, {'domain': 'www.cam4.com', 'httpOnly': False, 'name': 'flash_enable', 'path': '/signup', 'secure': False, 'value': 'false'}, {'domain': 'www.cam4.com', 'httpOnly': False, 'name': 'userWasLoggedIn', 'path': '/signup', 'secure': False, 'value': 'wasLogged'}]
    cookie_str = json.dumps(a)
    print(len(cookie_str))
    submit['Cookie'] = cookie_str
    submit['Mission_Id'] = '10000'
    submit['Email_Id'] = '9f705978-c827-11e9-8c6c-000d7567cc3c'
    db.update_cookie(submit)    

def test_ports():
    plans = db.read_plans(1)
    print(plans)
    ports = [plan['port_lpm'] for plan in plans]
    print(ports)

def test_cookies():
    Config = {}
    Config['Mission_Id'] = '10005'
    Config['Alliance'] = 'highrockads'
    Config['Account'] = '1'
    Mission_dict = db.get_cookie(Config)
    print(Mission_dict)

def test_9_15():
    zone = 'kang_uk_01'
    pwd = 'o9b3zwuy9qko'
    luminati.write_proxy_config(zone,pwd)
    data = luminati.read_proxy_config()
    print(data)
    
def test_port():
    port_add = '24114'
    luminati.add_proxy(port_add,country='us',proxy_config_name='kang_us_1',ip_lpm='192.168.30.131')

def test_check():
    submit = {}
    submit['Mission_Id'] = 10005
    submit['Email_Id'] = 'a5839-8cf9-000d7567cc3c'
    res = db.check_mission_status(submit)
    print(res)
    print(len(res))

def delete():
    luminati.delete_port()  


def mytest():
    import time_related
    try:
        time_related.mytest('starting')
    except Exception as e:
        print(e)

def test_emails():
    import db
    import imap_test
    emails = db.get_all_emails()
    # print(emails[0])
    emails = [email for email in emails if 'hotmail' in email['Email_emu']]
    # print(emails[1])
    # multi_tests(emails[1])
    submits = []
    # for i in range(10):
    #     print(i,'..........')
    #     Mission_list = ['10000']
    #     Excel_name = ['','Email']
    #     Email_list = ['hotmail.com']
    #     submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
    #     submits.append(submit)
    print(len(emails))
    # return
    requests = threadpool.makeRequests(imap_test.multi_tests, emails)
    [pool.putRequest(req) for req in requests]
    pool.wait()        

def get_soi_email():
    Mission = '10021'
    email_list = ['hotmail.com','outlook.com','gmail.com','msn.com']
    db.get_unique_soi_email(Mission,email_list)

def test_activate_status(): 

    import datetime
    submit = {}
    submit['activate2'] = ''
    submit['activate1'] = str(datetime.datetime.now())
    submit['activate3'] = ''
    submit['Cookie'] = ''
    submit['Mission_Id'] = '10009'
    submit['Email_Id'] = 'a3eec680-c827-11e9-b5c0-000d7567cc3c' 
    db.update_activate_status(submit)     


def test_pid():
    import os
    # pid=os.fork() #fork反复拷贝
    if  pid==0:
        print("A",os.getpid(),os.getppid())
    else:
        print("B",os.getpid(),os.getppid())

def print_():
    while True:
        print('1')
        sleep(5)

def test_1009():
    submit = {}
    submit['Mission_Id'] = 10009
    submit['Alliance'] = 'Fireads'
    submit['Account'] = 2
    submit['Email_Id'] = '1111'
    submit['BasicInfo_Id'] = ''
    submit['ua'] = 'aaa'
    submit['Cookie'] = '111'
    db.write_one_info([str(submit['Mission_Id'])],submit)

def shuffle_test():
    x = [i for i in range(10)]
    y = random.shuffle(x)
    print(x)

def test_502():
    ip_lpm = '192.168.30.130'
    port_lpm = '27277'
    flag = luminati.ip_test(ip_lpm,port_lpm,state = '',country='')    
    print(flag)
    # if proxy_info == '':
        # print('=========')


def change_port():
    ip_lpm = '192.168.30.130'    
    port_new = luminati.get_port_random(ip_lpm)
    db.update_port('24097',port_new)

def push_up(weight,num):
    weight = 101
    g = 9.8
    h = 0.25
    energy_push = weight*g*h*2/1000  #kj
    print('pushing_up using %0.1f kj with num %d'%(energy_push*num,num))    
    return energy_push*num

def squat(weight,num):
    energy_squat = weight*9.8*0.3*2/1000
    print('squat using %0.1f kj with num %d'%(energy_squat*num,num))
    return energy_squat*num

def energy_cal():
    weight = 101
    num_push_up = 100
    num_squat = 200
    running = 271*4.18
    print('Running using',running,'kj')
    energy_push = push_up(weight,num_push_up)
    energy_squat = squat(weight,num_squat)
    energy_used = energy_push+energy_squat+running
    return energy_used

def test():
    info = {
    'weight':101, #kg
    'push_up':70, #num
    'squat':100,  #num
    'running':270 #kj
    }    
    class energy():
        def __init__(self,info=None):
            print('=========')
            self.weight = info['weight']
            # self.g = 9.8
            self.push_up = info['push_up']
            self.squat = info['squat']
            self.running = info['running']
            self.energy_used = self.running
            print(self.push_up)
            print(self.energy_used)
    
        def push_up_(self):
            # print(self.push_up)
            print('==========++++')

    energy_ = energy(info)
    print(energy_)
    energy_.push_up_()

def test_html():
    import traffic
    url = 'http://im.datingwithlili.com/im/click.php?c=8&key=0jp93r1877b94stq2u8rd6hd'
    

def test_cam4_fr():
    Mission_list = ['10002']
    Excel_name = ['health','Email']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    start = time_related.Time_start()
    start = str(start)
    print(start)
    after = start.split('.')[0].replace(':','-')
    print(after)    
    return
    submit1 = db.read_one_excel(Mission_list,Excel_name,Email_list) 
    # print(submit1)  
    end = time_related.Time_end()
    time_used = time_related.Time_used(start,end)
    print(time_used,'seconds used for test')

def db_test_remote():
    '''
    Login sql and create EMU db if not exist
    choose emu db
    return the cursor and conn
    '''
    import pymysql
    conn = pymysql.connect(host= 'rm-bp100p7672g0g8z9kjo.mysql.rds.aliyuncs.com',port=3306,user='emu3man_win',passwd='sAz6x4SD8dF1')
    cursor = conn.cursor()
    print(cursor)
    try:
        cursor.execute('show databases;')
        res = cursor.fetchall()
        print(res)
        # cursor.execute('use %s;'%account['db_name'])
    except Exception as e:
        print(e)
    # print('Login db success.')
    # res = cursor.execute('select * from TOKENTABLE;')
    return conn,cursor

def test_lpm_local():
    # db.get_ports_set()
    port = luminati.get_port_random()
    print(port)

def test_info_height():
    pass


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

def get_chromedriver_path():
    return r'driver/chromedriver_77.exe'    

def chrome_get_ext(user_data_dir=None,submit=None,charge=0):
    from selenium import webdriver
    options = webdriver.ChromeOptions() 
    # ip = submit['ip_lpm']
    # port = submit['port_lpm']
    # proxy = 'socks5://%s:%s'%(ip,port)
    # options.add_argument('--proxy-server=%s'%proxy)
    # print(proxy)    
    # if charge==0:
    #     options.add_argument('--user-data-dir='+user_data_dir)
    prefs = {"download.default_directory": 'c:\\',
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "safebrowsing.enabled": True,
             "credentials_enable_service":False,
             "password_manager_enabled":True
             }    
    # prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'c:\\emu_download'}
    # options.add_experimental_option('prefs', prefs)
    uas = get_ua_all()
    ua = get_ua_random(uas)
    print(ua)      
    options.add_argument('user-agent=' + ua)     
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
    # options.add_argument('--single-process')
    # options.add_argument('--process-per-tab')    
    
    # options.add_argument('--disable-gpu')        
    # options.add_argument("--disable-automation")
    # options.add_argument("--disable-automation")
    # options.add_experimental_option("excludeSwitches" , ["enable-automation","load-extension"])
    options.add_experimental_option("prefs", prefs) 
    path_driver = get_chromedriver_path()
    chrome_driver = webdriver.Chrome(chrome_options=options,executable_path=path_driver)
    chrome_driver.set_page_load_timeout(300)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒    
    # cookies = chrome_driver.get_cookies()  
    # print(cookies)
    # chrome_driver.delete_all_cookies()    
    return chrome_driver

def test_cehuo():
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    submit = {}
    chrome_driver = chrome_get_ext()
    wait = WebDriverWait(browser, 120) #等待的最大时间
    sleep(5)
    input = wait.until(
        #判断该元素是否加载完成
        EC.presence_of_element_located((By.CLASS, 'btn-primary'))
    )    
    # chrome_driver.find_element_by_xpath()
    url_battle = 'https://account.blizzard.com'
    chrome_driver.get(url_battle)
    chrome_driver.find_element_by_xpath('//*[@id="562016032"]/div[1]/div/div[2]/a').click()
    sleep(3000)


def port_test_k():
    ports = db.get_ports_set()
    print(ports)

def Write_Ini(file,content):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    content = json.dumps(content) 
    with open(file,'w+') as f:
        # content += '\n'
        f.write(content)

def read_plans_tolog():
    plans = db.read_plans(-1)
    
def test_print():
    import sys
    import traceback
    import datetime
    try:
        db.test111()  
    except:
        file_ = '..\log.txt'
        content = str(datetime.datetime.utcnow())
        with open(file_,'a+') as f:
            content += '\n'
            f.write(content)          
        traceback.print_exc(file=open(file_,'a+'))

def main_():
    test_db_time()

def test_flag_use():
    db.update_flag_use_all()

def soi_test():
    Mission_status_dict = db.get_soi_email()
    print(len(Mission_status_dict))
    names = [info['email'] for info in Mission_status_dict]
    txt_info = ''
    for name in names:
        txt_info += name.split('@')[0] + '\n'

    with open('names.txt','a+') as f:
        f.write(txt_info)

def bat_test():
    command = '..\StartGit.bat'
    os.system(command)      

def test_p():
    import thread_tokill as tt
    import os
    # os.environ['TZ'] = 'Asia/Shanghai'

    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get('https://www.baidu.com')
    submit = {}
    submit['Mission_Id'] = 10099
    xpath = '//*[@id="su"]'
    text = '百度一下'
    # sleep(3000)
    # sleep(5)
    # text_=chrome_driver.find_element_by_xpath(xpath).value
    # print(text_)
    if EC.text_to_be_present_in_element_value((By.XPATH,xpath),text)(chrome_driver):
        print('success')
    else:
        # a+1
        print('fail')
    # except:
        # tt.writelog(chrome_driver,submit)

def test_pp():
    '''
    asdasd

    '''
    import Submit_handle as sh
    a = sh.get_name_real.__doc__
    print('=========')
    print(a)

def test_c():
    pic = '10064_16806.png'
    # fin = open(pic)
    # png = fin.read()    
    with open(pic,'rb') as f:
        png = f.read()    
    print(len(png))
    db.write_log_db(10001,'asssssssss',png)    
    # db.read_pic(100)

    # with open('test.png','wb') as f:
    #     f.write(png)

def file_open():
    os.system('explorer.exe /n, C:\EMU\log\pics')

def testfa():
    Excel_name = 'pl_soi'
    db.test_count(Excel_name)    

def testf():
    import traceback
    try:
        a=b
    except:
        a = traceback.format_exc()
        print(type(a))
        print(len(a))
        print('=========')
        Mission_Id = 20001
        traceback_ = a
        db.write_log_db(Mission_Id,traceback_)

def qt_test():
    import sys
    from PyQt5.QtWidgets import QWidget

    out = sys.stdout
    sys.stdout = open(r'C:\EMU\QWidget.txt','w')
    help(QWidget)
    sys.stdout.close()
    sys.stdout = out

def login_sql():
    '''
    Login sql and create EMU db if not exist
    choose emu db
    return the cursor and conn
    '''
    import pymysql
    ip = '192.168.89.139'
    conn = pymysql.connect(host= ip,port=3306,user='root',passwd='root',charset='utf8mb4',use_unicode=True)
    cursor = conn.cursor()
    try:
        cursor.execute('use %s;'%account['db_name'])
    except:
        pass
    print('Login db success.')
    # res = cursor.execute('select * from TOKENTABLE;')
    return conn,cursor


def test_ff():
    # a = ['<selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="41a8c736-079e-4c17-9741-ccd98af7327e")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="8ec4df17-5fa6-447c-a845-729bba0c6516")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="36fbe04a-28e1-4116-a26a-0d5c1980aeef")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="40274fc9-dd01-4e8d-9a1a-4d39d6065962")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="9a9ade26-025d-4294-8ca3-a613c959b120")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="e6117458-f0d1-469a-ba39-1e42fac791c4")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="b5f9b869-8f6f-4bc8-bc36-51a4ab9eb06f")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="e949bdfe-916b-461d-b23e-3f9e35e02419")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="5829cace-0232-4fdc-be26-92206a1af0ea")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="c8a6f425-3c55-43d1-a300-86cb6a9dd529")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="9cff8291-6841-428a-a33f-ee20d3a70572")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="127d7f63-1fe1-4d81-adfa-a393b2c63538")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="cff48027-806f-413a-a8ab-b370ecdbdf59")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="6c0b26a2-d022-4c90-b9c1-390b9994a2c7")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="a1e6dd1a-1b9e-4ece-bb52-e0fa9e8fc713")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="6f4dad85-e23a-4627-b077-4741b73aa2cb")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="1462ccb4-7361-4400-9225-45cab0927b22")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="7538576d-4913-4b3a-81a8-2648b8b75800")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="3b172738-82b0-4a4b-9b93-d5697ba4031c")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="3640693a-16a9-4222-a769-9ca3778cf975")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="ae0c7889-3864-477c-b4b4-44cfb3903b79")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="839dd37b-941c-485e-9dfb-e5dc5e43f1af")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="de17f083-4c6f-4810-862c-0df5b5f2db2c")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="a88f79c6-650f-464f-9813-1ce14466b261")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="22204f94-0634-4130-88d9-50345d3d12a3")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="5cff94d7-e6cd-4e90-975b-f6d99ac9fb29")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="ccf86ef0-870c-4a8c-be0f-3b8e745554bf")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="558074c0-6b50-470b-a057-6fd2b72cc3a0")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="3b7ab56c-9551-44d2-af48-7e4d605abcf0")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="51649f17-69ec-4274-81c6-411bb1444520")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="8967c974-e180-45bb-96d5-befee3c93607")>, <selenium.webdriver.remote.webelement.WebElement (session="d72a7a2dfbc8f9aba1e215ef859cc227", element="66f9e4c4-4994-47b9-be4b-392ceb8e5761")>]
    Mission_Id = 10047
    # flag = {
    #     'name'  :   'page1',
    #     'xpath' :   '//*[@id="plate-content"]/h3',
    #     'text'  :   'Do you have car insurance?'
    # }
    # db.update_pageflag(Mission_Id,flag)
    # pages = db.get_pageflag(Mission_Id)
    # print(pages)
    step = {
                'Action' : {
                    'Click':True,
                    'Select':False,
                    'Input':False,
                    'Slide':False,
                },                
                'Config'   : {
                    # general setting
                    'scroll' : True,                
                    'try' : True,                    
                    'xpath' : '//*[@id="plate-content"]/div[2]/div[2]/button',
                    'input_setting' : {
                        'content' : '',
                        'dynamic' : False,
                    },
                    'select_setting' : {
                        #select general
                        'selected_css' : '',                    
                        'select_type' : 1,
                        #1.select_by_index
                        # 2.select_by_values
                        # index_2
                        'select_index' : 0,
                        'select_index_rand' : True,
                        # value_3
                        'select_value' : 'email',                                        
                        'select_value_range' : ['10','100'],
                        'select_value_list' : [],
                    },
                    'slide' : {
                        'x_move_min' : 10,
                        'x_move_max' : 200,
                        'y_move_min' : 0,
                        'y_move_max' : 0
                    }  
                } 
            } 

def test_gg():
    Mission_Id = 10000
    flag = {}
    flag['name'] = '1' 
    flag['step'] =  1
    pages = db.get_pageflag(Mission_Id)
    # print(pages)
    pages = pages.sort(key=takeStep)
    print(pages)


def takeStep(elem):
    print(elem['Step'])
    return elem['Step']

def test_44():
    import Dadao
    submit = {}
    content = Dadao.get_write_content(submit)    
    print(content)

def test_kk():
    data = {'Mission_Id': 10002, 'Page': '1', 'Step': 10, 'Action': 'Select', 'General': '{"scroll": "False", "try": "False", "xpath": "//*[@id=\\"list-lead-form\\"]/div[1]/select", "iframe": ""}', 'Step_config': '{"select_index": "", "select_index_rand": "False", "select_value": "False", "select_value_range": ["2000", "2018"]}'}
    data['General'] = json.loads(data['General'])
    if data['General']['iframe'] != '':
        print(111)
    else:
        print(data['General']['scroll'])


def test_class():
    class test():
        def f(self):
            print('aaaaa')
            return 'hello world'        
    func = 'f'
    a = test()
    f = eval('a.'+func)()
    print(f)



def get_version_number(filename):
    #This is just for windows.
    info = GetFileVersionInfo(filename, "\\")
    #print info
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    print(HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls))
    return HIWORD(ms)

def test_version():
    get_version_number(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")    

def test_get_excels():
    sql_content = 'select DISTINCT excel_name from basicinfo'
    response = db.Execute_sql_single(sql_content)    
    # print(response)
    excels = [key[0] for key in response]
    print(excels)
    sql_contents = []
    for excel in excels:
        sql_content = 'SELECT * from BasicInfo  WHERE Excel_name = "%s"'%excel
        
        response = db.Execute_sql_single(sql_content)

def test_sss1():
    values = ['1','a','b','c']
    contents = ['a','b','d','3']
    test = [content for content in contents if content in values]
    print(test)

def test_sss2():
    import sys
    print(sys.path)


def getInstallBdyAdree():
    import os
    print(type(os.environ))    
    print(dict(os.environ))

    # paths = os.environ.split

def test_ddd():
    import win32com.client
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
    # objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")  
    # print(colItems)  
    colItems = objSWbemServices.ExecQuery("Select * from Win32_Product")
    print(objSWbemServices)
    for objItem in colItems:
        print("Caption: ", objItem.Caption)
        # print("Description: ", objItem.Description)
        # print("Identifying Number: ", objItem.IdentifyingNumber)
        # print("Install Date: ", objItem.InstallDate)
        # print("Install Date 2: ", objItem.InstallDate2)
        # print("Install Location: ", objItem.InstallLocation)
        # print("Install State: ", objItem.InstallState)
        # print("Name: ", objItem.Name)
        # print("Package Cache: ", objItem.PackageCache)
        # print("SKU Number: ", objItem.SKUNumber)
        # print("Vendor: ", objItem.Vendor)
        # print("Version: ", objItem.Version)    


def reg_test():
    # url = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\chrome'
    url = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'    
    getInstallBdyAdree(url)

def getInstallBdyAdree(url):
    import winreg
    key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, url)
    # print(key)
    data = winreg.QueryValueEx(key, "Path")
    # print(data)
    path_chrome = data[0]
    print(path_chrome)

def test_account():
    sql_content = 'Update accounts set flag = "%d"'%(0)
    db.Execute_sql([sql_content])
    
def test_cookies_write():
    cookie = '========'
    country = 'US'
    selenium_funcs.write_cookie(cookie,country)

def test_generate():
    # account = luminati.get_account()
    # ip = account['IP_lpm']
    # port = '24041'
    # proxy = 'socks5://%s:%s'%(ip,port)
    uas = Chrome_driver.get_ua_all()
    ua = Chrome_driver.get_ua_random(uas) 
    headers_1 = {
        'user-agent':ua,
        }    
    headers = {
        'user-agent':ua,
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.getaround.com',
        'referer': 'https://www.getaround.com/sharecar?utm_source=impact radius&utm_medium=affiliate&utm_campaign=impact-radius-affiliate-all-market-supply&utm_content=__tkey:Q2FyIExlYWRfSW1wYWN0IFJhZGl1c19Db250ZW50X0FmZmlsaWF0ZV9QYWlkX1Byb3NwZWN0X19BTExfX0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0BAX0BAX0BA&tkey=Q2FyIExlYWRfSW1wYWN0IFJhZGl1c19Db250ZW50X0FmZmlsaWF0ZV9QYWlkX1Byb3NwZWN0X19BTExfX0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0BAX0BAX0BA&affiliate=365723&clickid=3YPUkz2V2xyOTk7wUx0Mo3YQUknUT-xFRzyo2s0&ircid=7962&irgwc=1&sharedid=233486',
    }         
    session = requests.session()
    # session.proxies = {'http': proxy,
    #                    'https': proxy}  
    # print('Approaching:',url)
    # print(proxy)
    year = random.randint(2003,2017)
    Mission_list = ['10002']
    excel = 'health'    
    Excel_name = [excel,'']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit_ = db.read_one_excel(Mission_list,Excel_name,Email_list)
    submit = submit_['health']
    first_name = submit['firstname']
    last_name = submit['lastname']
    zip_ = submit['zip'].split('.')[0]
    phone = submit['homephone'].split('.')[0]
    email = submit['email']
    data = {
    'year': str(year),
    'country': 'US',
    'zipcode': zip_,
    'first_name': first_name,
    'last_name': last_name,
    'email': email,
    'phone': phone,
    'source': 'News Article',
    'source_other': '', 
    'lead_page': 'getaround.com/sharecar' 
    }   
    print(data)
    data_ = json.dumps(data)  
    # url_google = 'https://www.google.com'
    url = 'https://adpgtrack.com/click/5d43f1a4a03594103a75da46/146827/233486/subaccount'
    session.get(url,headers=headers_1)  
    url = 'https://www.getaround.com/ajax/generate-lead'    
    resp=session.post(url,data=data_,headers=headers)  
    # print(headers)
    print(resp.text)
    # print(resp.headers)
    # print(resp.status_code)
    # print(type(resp.status_code))
    url = 'https://www.google.com/pagead/conversion_async.js'
    headers_2 = {
        'user-agent':ua,
        'referer': 'https://www.getaround.com/sharecar?utm_source=impact%20radius&utm_medium=affiliate&utm_campaign=impact-radius-affiliate-all-market-supply&utm_content=__tkey:Q2FyIExlYWRfSW1wYWN0IFJhZGl1c19Db250ZW50X0FmZmlsaWF0ZV9QYWlkX1Byb3NwZWN0X19BTExfX0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0BAX0BAX0BA&tkey=Q2FyIExlYWRfSW1wYWN0IFJhZGl1c19Db250ZW50X0FmZmlsaWF0ZV9QYWlkX1Byb3NwZWN0X19BTExfX0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0BAX0BAX0BA&affiliate=365723&clickid=3YPUkz2V2xyOTk7wUx0Mo3YQUknUT-xFRzyo2s0&ircid=7962&irgwc=1&sharedid=233486'
    } 
    resp=session.get(url,headers=headers_2)  
    print(headers)
    print(resp.text)
    print(resp.headers)
    print(resp.status_code)
    print(type(resp.status_code))       

def conversion():
    account = luminati.get_account()
    ip = account['IP_lpm']
    port = '24041'
    proxy = 'socks5://%s:%s'%(ip,port)
    uas = Chrome_driver.get_ua_all()
    ua = Chrome_driver.get_ua_random(uas) 
    url = 'https://www.google.com/pagead/conversion_async.js'
    # url = 'http://lumtest.com/myip.json'
    headers = {
        'user-agent':ua,
        'referer': 'https://www.getaround.com/sharecar?utm_source=impact%20radius&utm_medium=affiliate&utm_campaign=impact-radius-affiliate-all-market-supply&utm_content=__tkey:Q2FyIExlYWRfSW1wYWN0IFJhZGl1c19Db250ZW50X0FmZmlsaWF0ZV9QYWlkX1Byb3NwZWN0X19BTExfX0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0BAX0BAX0BA&tkey=Q2FyIExlYWRfSW1wYWN0IFJhZGl1c19Db250ZW50X0FmZmlsaWF0ZV9QYWlkX1Byb3NwZWN0X19BTExfX0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0BAX0BAX0BA&affiliate=365723&clickid=QDlRQb2XDxyOU6nwUx0Mo3Q3UknUXjS9522h1g0&ircid=7962&irgwc=1&sharedid=233486'
        # 'https://www.getaround.com/sharecar?utm_source=impact radius&utm_medium=affiliate&utm_campaign=impact-radius-affiliate-all-market-supply&utm_content=__tkey:Q2FyIExlYWRfSW1wYWN0IFJhZGl1c19Db250ZW50X0FmZmlsaWF0ZV9QYWlkX1Byb3NwZWN0X19BTExfX0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0BAX0BAX0BA&tkey=Q2FyIExlYWRfSW1wYWN0IFJhZGl1c19Db250ZW50X0FmZmlsaWF0ZV9QYWlkX1Byb3NwZWN0X19BTExfX0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0ltcGFjdCBSYWRpdXMgQWZmaWxpYXRlIEFsbCBtYXJrZXQgU3VwcGx5X0BAX0BAX0BA&affiliate=365723&clickid=3YPUkz2V2xyOTk7wUx0Mo3YQUknUT-xFRzyo2s0&ircid=7962&irgwc=1&sharedid=233486'
    }
    session = requests.session()
    # session.proxies = {'http': proxy,
    #                    'https': proxy}      
    resp=session.get(url,headers=headers)  
    print(headers)
    print(resp.text)
    print(resp.headers)
    print(resp.status_code)
    print(type(resp.status_code))    


def test_t_t():
    import Mission_11002
    submit,path,workbook = Mission_11002.get_data()
    submit['status'] = 'badname'
    for i in submit['badname']:
        submit['row'] = i
        Mission_11002.write_status(path,workbook,submit,'badname')              
    card = submit['card_number'].replace('\t','')
    month = submit['month'].replace('\t','').split('.')[0]
    year = submit['year'].replace('\t','').split('.')[0]
    year = str(year)            
    cvv = submit['cvv'].replace('\t','').split('.')[0]
    cvv = str(cvv)
    if len(month) == 1:
        month = '0' + month
    if len(year) != 2:
        year = year[-2:]
    if len(cvv) == 1:
        cvv = '00'+ cvv
    elif len(cvv) == 2:
        cvv = '0' + cvv        
    print(cvv,year,month)

def db_test_cc():
    import datetime
    Mission_list = [10002]
    submit = {'health': {'BasicInfo_Id': '354a1e1e-1c15-11ea-b5db-000c73f89c81', 'country': '', 'firstname': 'Anna', 'lastname': 'Avery', 'address': '12183 pulaski pike', 'city': 'Toney', 'state': 'AL', 'zip': '35773.0', 'homephone': '2566835812.0', 'workphone': None, 'email': 'a.avery@mchsi.com', 'dateofbirth': None, 'maritalstatus': None, 'gender': None, 'education': None, 'occupation': None, 'yearsatemployer': None, 'residencetype': None, 'yearatresidence': None, 'leadtype': None, 'validation': None, 'licensestate': None, 'licenseeversuspendedrevoked': None, 'abs': None, 'airbags': None, 'alarm': None, 'multivehicle': None, 'insurancecompany': None, 'coveragetype': None, 'bodilyinjury': None, 'propertydamage': None, 'collisiondeductible': None, 'comphrensivedeductible': None, 'annualmiles': None, 'year': None, 'make': None, 'model': None, 'submodel': None, 'primaryuse': None, 'ipaddress': None, 'sourceid': None, 'first_name': None, 'last_name': None, 'home_phone': None, 'work_phone': None, 'best_time_to_call': None, 'requested_loan_amount': None, 'ssn': None, 'date_of_birth': None, 'drivers_license': None, 'drivers_license_state': None, 'own_rent': None, 'years_at_residence': None, 'months_at_residence': None, 'age': None, 'military': None, 'income_type': None, 'is_dependent': None, 'net_monthly_income': None, 'years_employed': None, 'months_employed': None, 'supervisor_phone': None, 'pay_period': None, 'paycheck_type': None,'employer': None, 'account_type': None, 'bank_name': None, 'routing_number': None, 'account_number': None, 'years_bank_account': None, 'months_bank_account': None, 'ip_address': None, 'dts': None, 'Excel_name': 'health', 'postal_code': None, 'zipcode': None, 'Create_time': datetime.datetime(2019, 12, 12, 10, 54, 2), 'reference1_first_name': None, 'reference1_last_name': None, 'reference1_relationship': None, 'phone_reference1': None, 'reference2_first_name': None, 'reference2_last_name': None, 'reference2_relationship': None, 'phone_reference2': None, 'ip': None, 'title': None, 'emailaddress': None, 'phone': None, 'flag_use': 0, 'tzid': None, 'windows': None}, 'ip_lpm': '192.168.159.130', 'port_lpm': '27629', 'state_': 'AL', 'Mission_Id': '10002', 'Country': 'US', 'Site': 'http://bkln.xyz/click.php?c=10&key=miqhd1p7ec783mr8a497j4q4\n', 'Excels_dup': ['health', ''], 'Alliance': 'Adpump', 'Account': '1', 'Offer': 'GETAROUND(Done)', 'ID': 561, 'sleep_flag': 2, 'Mission_dir': 'C:\\EMU\\emu_chromes\\10002,1', 'Record': 0, 'ua': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari', 'Status': 2}    
    db.write_one_info(Mission_list,submit)


def test_qt_test():
    import qt
    qt.test_k()

def more_test():
    Mission_Id = 10045
    Page_flags = db.get_page_flag(Mission_Id)
    print(Page_flags)
    Page_flags = [item for item in Page_flags if item['Country'] == 'US']
    print(Page_flags)

def test_ps():
    # Page_flags = db.get_page_flag(10088)
    configs = db.get_page_config(10088,1)
    configs.sort(key=takeStep)
    for config_ in configs:
        print(config_)
        config_['General'] = json.loads(config_['General'])     
    print(configs)


def test_123():
    alias = db.read_alias_num()
    print(alias)
    Mission_Ids = [10089]
    if str(Mission_Ids[0]) in alias:
        Mission_Ids[0] = alias[str(Mission_Ids[0])].replace('\n','') 
    print(Mission_Ids)  

def test_124():
    import Submit_handle
    payday = Submit_handle.get_next_payday_all()
    print(payday)

def test_1232():
    account = db.get_account()
    conn,cursor=db.login_sql(account)    
    res = cursor.execute('SELECT Basicinfo_Id from BasicInfo')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    res = cursor.execute('SELECT Basicinfo_Id from Mission')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict2 = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来          
    # print(len(Mission_dict))
    # print(Mission_dict[0:5])
    ids = [item['Basicinfo_Id'] for item in Mission_dict]
    ids = list(set(ids))
    print('Number before set1:',len(ids))    
    ids2 = [item['Basicinfo_Id'] for item in Mission_dict2]
    ids = ids+ids2
    print('Number before set:',len(ids))
    print(ids[:5])
    ids = list(set(ids))
    print('Number after set:',len(ids))
    print(ids[:5])
    return ids

def test_1231():
    import uuid
    ids = test_1232()
    for i in range(1000):
        uuid_sin = str(uuid.uuid1())     
        if uuid_sin in ids:
            print('uuid found in ids')
        else:
            print('uuid not found in ids,this is single')            
            break
    print(uuid_sin)    

if __name__ == '__main__':
    i = 1
    if i == 0:
        test_flag_use()
    elif i==1:
        test_1231()
    else:
        test_write()
