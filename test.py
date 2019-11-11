import time
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

def test_write():
    # account = db.get_account()
    plan_id = 1
    print('Plan_id:',plan_id,',connecting sql for plan info...')
    plans = db.read_plans(plan_id)    
    submit = db.get_luminati_submit(plans[0])
    print(submit)
    db.write_one_info([str(submit['Mission_Id'])],submit)    

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
    Mission_list = ['10005','10043']
    Excel_name = ['','Email']
    Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
    submit1 = db.read_one_excel(Mission_list,Excel_name,Email_list) 
    print(submit1)  


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
    


def main_():
    test_db_time()


if __name__ == '__main__':
    main_()
