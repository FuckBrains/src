import socket
import datetime
import os
import db
import time_related
import random
import re
import requests
import sys
import json
from time import sleep
import re
import Chrome_driver
import threading
import threadpool
from wrapt_timeout_decorator import *

def get_account():
    '''
    get account for sql db,read a config file in res folder
    eg:submit = {'password':...}
    requies nothing
    return the sql db account
    '''
    file = r'..\res\lpm_config.txt' 
    submits = []
    with open(file,'r') as f:
        jss = f.readlines()
        # print(jss)
        for js in jss:
            submit = json.loads(js)
            submits.append(submit)
            # print(submit)
    return submits[-1]


def test_luminati():
    customer = 'caichao'
    zone_name = 'zone2'
    pwd = 'abitpt3isvvj'
    if sys.version_info[0]==2:
        print(2)
        import six
        from six.moves.urllib import request
        opener = request.build_opener(
            request.ProxyHandler(
                {'http': 'http://lum-customer-%s-zone-%s:%s@zproxy.lum-superproxy.io:22225'%(customer,zone_name,pwd)}))
        print(opener.open('http://lumtest.com/myip.json').read())
    if sys.version_info[0]==3:
        print('3')
        import urllib.request
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler(
                {'http': 'http://lum-customer-%s-zone-%s:%s@zproxy.lum-superproxy.io:22225'%(customer,zone_name,pwd)}))
                # {'socks5':'socks5://192.168.30.131:24002'}))
                # {'http':'http://192.168.30.131:24001'}))
        # url_test = 'http://lumtest.com/myip.json'
        # url_test = 'http://www.google.com'
        res = str(opener.open('http://lumtest.com/myip.json').read(),encoding = "utf-8")
        # res = json.loads(res)
        print(res)

def api_test(proxy):
    import requests
    session = requests.session()
    session.proxies = {'http': proxy,
                       'https': proxy} 
    print('http://lumtest.com/myip.json')
    for i in range(5):
        try:
            resp=session.get("http://lumtest.com/myip.json",timeout=5)
            print('===')
            break
        except:
            print('try',i,'time')
            pass
    print(resp.text)                       
    headers = {
    'accept': 'application/json',
    'Origin': 'http://petstore.swagger.io',
    'Referer': 'http://petstore.swagger.io/?url=https://raw.githubusercontent.com/luminati-io/luminati-proxy/master/lib/swagger.json',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    # data = {}
    url = 'http://192.168.30.131:22999/api/refresh_sessions/24003'
    # url = 'http://192.168.30.131:22999/api/refresh_sessions/24002'
    try:
        resp = requests.post(url,headers=headers)
        print(resp)
        print(resp.text)
    except Exception as e:
        print(str(e))

    # print(resp)   

@timeout(30)
def refresh_proxy(ip,port):
    headers = {
    'accept': 'application/json'
    }    
    url = 'http://%s:22999/api/refresh_sessions/%s'%(str(ip),str(port))
    flag = 0
    for i in range(10):
        try:
            resp = requests.post(url,headers=headers)
            # print(resp)
            # print(type(str(resp)))
            # print(str(resp))
            resp_code = str(re.sub("\D", "", str(resp)))
            # print(resp_code)
            if resp_code == '204':
                flag = 1
            if flag == 1:
                print('refresh proxy success')
                break
        except Exception as e:
            print(str(e))
    return flag

@timeout(30)
def get_lpm_ip(port,url="http://lumtest.com/myip.json",Referer='',debug=0):
    if debug==1:
        print('debug==================',debug)
    account = get_account()
    ip = account['IP_lpm']
    proxy = 'socks5://%s:%s'%(ip,port)
    uas = Chrome_driver.get_ua_all()
    ua = Chrome_driver.get_ua_random(uas) 
    if Referer != '': 
        headers = {
            'User-Agent':ua,
            'Referer':Referer
        }   
    else:
        headers = {
            'User-Agent':ua
        }          
    session = requests.session()
    session.proxies = {'http': proxy,
                       'https': proxy}  
    # print('Approaching:',url)
    # print(proxy)
    resp=session.get(url,headers=headers)
    # print(headers)
    # print(resp.text)
    # print(resp.headers)
    # print(resp.status_code)
    # print(type(resp.status_code))
    if resp.status_code == 502:
        print('============,502')
        proxy_info = ''
        return proxy_info   
    try:
        # print('--------------------')
        # print(resp.text)            
        proxy_info = json.loads(resp.text)
        # print(proxy_info)
    except Exception as e:
        print(str(e))
        proxy_info = ' '
    if debug != 0:
        print('++++++++++++')
        while True:
            print(resp.text)
            a = resp.text.find('window.location = "')
            print('window.location = .......found')
            if a == -1:
                break
            else:
                b = resp.text.find('"',a+22)
                # print(a,b)
                # print(resp.text[a:b])
                url = (resp.text)[a+19:b]
                print(url)
                resp=session.get(url,headers=headers)
            print(resp.text)
    # print('proxy_info...',proxy_info,'...')
    return proxy_info

def tz_test():
    url="http://lumtest.com/myip.json"
    resp=requests.get(url)
    # resp=session.get(url,headers=headers)    
    proxy_info = json.loads(resp.text)
    print(proxy_info)
    tz = proxy_info['geo']['tz']
    print(tz)


@timeout(30)
def add_proxy(port_add,country='us',proxy_config_name='zone2',ip_lpm='127.0.0.1'):
    account = get_account()
    ip_lpm = account['IP_lpm']    
    data = {}
    data_proxy_config = read_proxy_config()
    data_proxy_config[proxy_config_name]['country'] = country
    data_proxy_config[proxy_config_name]['port'] = port_add
    data['proxy'] = data_proxy_config[proxy_config_name]
    # print('preparing to add proxy config:',data)
    data_ = json.dumps(data)
    headers = {
    'Content-Type': 'application/json'
    }    
    # url_ = 'http://127.0.0.1:22999/api/proxies'
    url_ = 'http://%s:22999/api/proxies'%ip_lpm
    # print(url_)
    flag = 0
    for i in range(1):
        try:
            resp = requests.post(url_,data=data_,headers=headers)
            # print(resp)
            # print(type(str(resp)))
            # print(str(resp))
        except Exception as e:
            print(str(e))  

def write_proxy_config(zone,pwd):
    data = read_proxy_config() 
    data[zone] = {
            "country": 'us',
            "keep_alive": True,
            "password": pwd,
            "pool_size": 1,
            "port": '24001',
            "proxy_resolve": True,
            "secure_proxy": True,
            "zone": zone
        }
    content = json.dumps(data) 
    with open(r'ini\proxy.ini','w+') as f:
        # content += '\n'
        f.write(content)    

def read_proxy_config():
    with open(r'ini\proxy.ini','r') as f:
        # content += '\n'
        proxy_details =f.readline()
        # for line in content:
            # proxy_details = line.strip('\n')    
            # print(proxy_details)
    data = json.loads(proxy_details)
    return data

pool = threadpool.ThreadPool(50)

# @timeout(30)
def delete_port(ports=''):
    account = get_account()
    print('read account finished ')
    ip_lpm = account['IP_lpm']
    print(ports)
    if ports == '': 
        try:       
            print('start getting ports')
            ports = ports_get(ip_lpm)
        except Exception as e:
            print(str(e))
            return
    requests = threadpool.makeRequests(delete_port_s, ports)
    [pool.putRequest(req) for req in requests]
    pool.wait()     


# @timeout(30)
def delete_port_s(port_delete):
    account = get_account()
    ip_lpm = account['IP_lpm']    
    url_ = 'http://%s:22999/api/proxies/%s'%(ip_lpm,str(port_delete))
    headers = {
    'Content-Type': 'application/json'
    }     
    data = {
        "port":port_delete
    }
    data = json.dumps(data)
    # print(data)
    try:
        # print('start delete post sending')
        resp = requests.delete(url_,data=data,headers=headers)
    except:
        pass
    # print(resp)
    # print(type(str(resp)))
    # print(str(resp))
    if '204' in str(resp):
        print('delete success:',port_delete)



def get_luminati():
    import random
    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.common.proxy import ProxyType, Proxy
    username = 'caichao'
    password = 'ysm1014wszqn'
    port = 22225
    zone_name = 'jia1'
    session_id = str(random.random()).split('.')[1]
    # 'http://%s-session-%s:%s@zproxy.luminati.io:%d'
    super_proxy_url = 'http://lum-customer-%s-zone-%s-session-%s:%s@zproxy.superproxy.io:22225'%(username,zone_name,session_id,password,port)
    print(super_proxy_url)
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': super_proxy_url,
        'ftpProxy': super_proxy_url,
        'sslProxy': super_proxy_url,
        'noProxy': ''  # set this value as desired
    })
    # print(proxy)
    # driver = webdriver.Chrome(executable_path="./bin/geckodriver", proxy=proxy)
    # path_download = get_dir()
    # prefs = {
    #         # "download.default_directory": path_download,
    #          "download.prompt_for_download": False,
    #          "download.directory_upgrade": True,
    #          "safebrowsing.enabled": True,
    #          'profile.default_content_settings.popups': 0,
    #          "profile.managed_default_content_settings.images": 2
    #          }       
    options = webdriver.ChromeOptions()
    # options.add_argument("--disable-automation")
    # options.add_experimental_option("excludeSwitches" , ["enable-automation","load-extension"])
    # options.add_experimental_option("prefs", prefs)     
    # proxy = '192.168.30.131:240001'
    # options.add_argument('--proxy-server=%s'%proxy)
    # proxy = 'socks5://192.168.30.131:24001'
    options.add_argument('--proxy-server=%s'%super_proxy_url)
    chrome_driver = webdriver.Chrome(
        # executable_path='/Users/youjunliang/PycharmProjects/chromedriver',
        chrome_options=options
       # options=options
    )
    # driver.manage().timeouts().pageLoadTimeout(30,TimeUnit.SECONDS)
    # driver.get('https://www.google.com')
    chrome_driver.get('https://whoer.net')
    sleep(3)    
    chrome_driver.get('https://whoer.net')
    sleep(300)    
    return chrome_driver

def get_proxy_test():
    from selenium import webdriver    
    import urllib.request
    import time
    username = 'lum-customer-caichao-zone-jia1'
    # username = 'caichao'
    password = 'ysm1014wszqn'
    port = 22225
    session_id = random.random()
    super_proxy_url = ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' %
                       (username, session_id, password, port))
    proxy_handler = urllib.request.ProxyHandler({
        'http': super_proxy_url,
        'https': super_proxy_url,
    })
    opener = urllib.request.build_opener(proxy_handler)
    proxy_details = opener.open('http://lumtest.com/myip.json').read()
    print(proxy_details)
    data = json.loads(proxy_details)
    print(data)

def ip_test(port_lpm,state = '',country=''):
    '''
    choose ip with state
    args:
        ip_lpm:ip of the lpm server
        port_lpm: port of the lpm server,based of Mission config created
    kargs:
        state: target state where ip located
        country: based of Mission config
    return string
    '''
    # ip_lpm = '192.168.30.131'
    # port_lpm = '24003'
    if country != 'US':
        state = ''
    account = get_account()
    # print(account)
    ip_lpm = account['IP_lpm']
    flag = 0
    proxy_info = ''    
    for i in range(10):
        # print('starting refresh ip...........')
        flag_ip = refresh_proxy(ip_lpm,port_lpm)
        sleep(3)
        if flag_ip == 0:
            # print('proxy_info',-1)
            flag = -1
            break        
        proxy_info = ''
        try:
            proxy_info = get_lpm_ip(port_lpm)
        except Exception as e:
            print(str(e))
            # print('fail to get lpm ip')
            flag = -1
            # flag_ip = refresh_proxy(ip_lpm,port_lpm)
            break
        if proxy_info == '':
            # print('proxy_info',-1)
            flag = -1
            break
        if state == '':
            # print(proxy_info)  
            flag = 1          
            break
        # print(proxy_info)
        try:
            state_proxy = proxy_info['geo']['region'] 
        except:
            continue
        # print(state_proxy)
        # flag = 1
        # break
        if state_proxy == state:
            # print('Find target state:',state_proxy)
            flag = 1
            break
        else:
            # print('State of proxy:',state_proxy)
            # print('Target state:',state)
            continue
    return flag,proxy_info

def ip_test_life(j):
    ip_lpm = '192.168.30.131'
    port_lpm = '24031'    
    start = datetime.datetime.utcnow()
    refresh_proxy(ip_lpm,port_lpm)
    proxy_info = get_lpm_ip(ip_lpm,port_lpm)
    print(proxy_info)
    ip_first = proxy_info['ip']
    i = 0
    while True:
        try:
            proxy_info = get_lpm_ip(ip_lpm,port_lpm)
            print('detect ip ',i,'time')
            print('proxy info:',proxy_info['ip'])
            if ip_first != proxy_info['ip']:
                print(proxy_info)
                break
            i += 1
            sleep(5)
        except:
            i+=1
            sleep(5)
            continue
    end = endtime = datetime.datetime.utcnow()
    time_used = time_related.Time_used(start,end)
    # print(time_used)
    print(start,end)
    print('Test',j,' used:',time_used,'seconds')
    return time_used

def main(proxy):
    get_lpm_ip(proxy)

def ports_get(ip_lpm):
    # print('ports_get',ip_lpm)
    url_ports = 'http://%s:22999/api/proxies_running'%ip_lpm
    try:
        res = requests.get(url_ports)
        print(res.text)
    except Exception as e:
        print(str(e))
    config_info = json.loads(res.text)
    ports_used = []
    for config in config_info:
        ports_used.append(config['port'])
    # print(ports_used)
    return ports_used

def test_ip():
    time_used_lists = []
    for i in range(20):
        time_used = ip_test_life(i)
        time_used_lists.append(time_used)
    for i in range(len(time_used_lists)):
        print('Test',i,'used',time_used_lists[i],'seconds')


@timeout(30)
def get_port_random():
    ports_set = db.get_ports_set()
    # print(ports_set)
    account = get_account()
    ip = account['IP_lpm']        
    ports_used = ports_get(ip)
    # print(']]]]]]]]]]')
    # print(set(ports_set))
    ports_used.extend(set(ports_set))
    port_ = 24000
    ports_used.append(port_)
    # print('ports_used:',ports_used)
    while port_ in ports_used:
        port_rand = random.randint(0,5999)
        basic_port = 24000
        port_ = basic_port + port_rand
    return port_

def create_plan_data(plan_id,Offer_links):
    account = get_account()
    # print('===================')
    # print('account',account)
    Configs = db.read_plans(plan_id)
    ip_lpm = account['IP_lpm']
    # print('Basic_port:',basic_port) 
    path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    dir_account_chrome = os.path.join(path,r'emu_chromes')
    myname = socket.getfqdn(socket.gethostname())
    # print(myname)
    myaddr = socket.gethostbyname(myname)
    # print(myaddr)
    print('Star uploading')
    num_plan = 1
    for item in Offer_links:
        print(' uploading plan %d'%num_plan)
        num_plan+=1
        Config = Offer_links[item]
        num_mission = 1
        for i in range(len(Configs)):
            if Configs[i]['Mission_Id'] == Config['Mission_Id']:
                num_mission += 1
        Mission_num_str = str(Config['Mission_Id'])+','+str(num_mission) 
        dir_account = os.path.join(dir_account_chrome,Mission_num_str) 
        dir_account = dir_account.replace('\\','//')                
        Offer_links[item]['Mission_dir'] = dir_account
        # print('dir_account:',dir_account)
        if account['IP_lpm'] == '127.0.0.1':
            Offer_links[item]['ip_lpm'] = myaddr
        else:
            Offer_links[item]['ip_lpm'] = ip_lpm            
        Offer_links[item]['port_lpm'] = get_port_random()  
        # print('Start adding proxy port:',Offer_links[item]['port_lpm'])
        if 'zone' in Offer_links[item]:
            proxy_zone = Offer_links[item]['zone']
        else:
            proxy_zone = 'jia1'      
        Config['zone'] = proxy_zone  
        add_proxy(Offer_links[item]['port_lpm'],country=Offer_links[item]['Country'],proxy_config_name= proxy_zone,ip_lpm=ip_lpm)
        Offer_links[item]['Plan_Id'] = plan_id
        Configs.append(Config)
    # print('Uploading finished')
    return Offer_links    

def create_plans():
    plan_id = 1
    plans,ports_toopen = create_plan_data(plan_id)
    db.upload_plans(plans)



if __name__ == '__main__':
    delete_port('')

