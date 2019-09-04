from sockshandler import SocksiPyHandler
import socks
from urllib.request import build_opener
import threadpool
import random
import sys
sys.path.append("..")
import Chrome_driver
from time import sleep



pool = threadpool.ThreadPool(500)
def read_proxy():
    with open('vipsocks.txt') as f:
        lines = f.readlines()
        sockets = []
        for line in lines:
            if line != '' and ':' in line:
                sockets.append(line.replace('\n',''))
    return sockets

def write_proxy(proxyaddr,proxyport):
    num_file = random.randint(1000000,10000000)
    with open(r'proxys\%s.txt'%(str(num_file)),'w') as f:
        f.write(proxyaddr+':'+str(proxyport))

def test_s5(socket_s5):
    uas = Chrome_driver.get_ua_all()
    ua = Chrome_driver.get_ua_random(uas)
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept - Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
        # 'Connection': 'Keep-Alive',
        'User-Agent': ua
    }
    url = 'https://www.google.com/'    
    proxy_s5 = socket_s5.split(':')
    print(proxy_s5)
    proxyaddr_ = proxy_s5[0]
    proxyport_ = int(proxy_s5[1])
    proxy_handler = SocksiPyHandler(proxytype=socks.SOCKS5, proxyaddr=proxyaddr_, proxyport=proxyport_)
    # proxy_handler = SocksiPyHandler(proxytype=socks.SOCKS5, proxyaddr=proxyaddr_, proxyport=proxyport_, username='***', password='***')        
    opener = build_opener(proxy_handler)
    opener.addheaders = [(k, v) for k, v in headers.items()]
    try:
        resp = opener.open(url, timeout=30)
        resp_html = resp.read()
        print(resp_html.decode())
        write_proxy(proxyaddr_,proxyport_)
    except Exception as e:
        # print(str(e))
        print('connect failed')
        pass    

def test_s5_requests(socket_s5):
    # socket_s5 = '27.155.64.249:8081'
    proxy_s5 = socket_s5.split(':')
    proxyaddr_ = proxy_s5[0]
    proxyport_ = int(proxy_s5[1])    
    from requests_html import HTMLSession
    session = HTMLSession()
    proxy = {"http": "socks5://"+socket_s5,"https": "socks5://"+socket_s5}
    url = "https://www.google.com"
    # url = 'http://myip.kkcha.com/'
    try:
        req = session.get(url, proxies=proxy,timeout=20)
        # req = session.get(url,timeout=20)        
        print(req.text)    
        write_proxy(proxyaddr_,proxyport_)
    except Exception as e:
        # print(str(e))
        print('connect failed')
        pass


def test_chrome():
    from selenium import webdriver
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    # print(help(webdriver.Chrome))
    # return
    # myProxy = "207.97.174.134:1080"
    # proxy = Proxy({
    #     'proxyType': ProxyType.MANUAL,
    #     'httpProxy': myProxy,
    #     'ftpProxy': myProxy,
    #     'sslProxy': myProxy,
    #     'noProxy': '' # set this value as desired
    #     })
    # proxy = '207.97.174.134:1080'
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.http_proxy = proxy
    # prox.socks_proxy = proxy
    # print(help(prox))
    # return

    # pproxy -r ${HTTP_PROXY}\#${PROXY_AUTH} -l http://:8080 -v
    # 1.2.3.4:1234 is remote address:port, username and password is used auth for remote proxy.
    
     # pproxy -r http://207.97.174.134:1080\#username:password  -l http://:8080 -v
     # pproxy -r http://207.97.174.134:1080  -l http://:8080 -v
     
    
    
    # prox.ssl_proxy = proxy
    # capabilities = webdriver.DesiredCapabilities.CHROME
    # prox.add_to_capabilities(capabilities)
    # print(capabilities)
    # return
    chrome_options = webdriver.ChromeOptions()
    PROXY_IP = '47.94.142.38:7302'
    chrome_options.add_argument('--proxy-server=socks5://%s'% PROXY_IP)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_page_load_timeout(90)
    # driver.get('http://myip.ms')

    # driver = webdriver.Chrome(proxy=proxy)
    # driver = webdriver.Chrome(proxy=proxy)
    driver.get("whoer.net")  
    sleep(3)
    driver.get("whoer.net")  


    # driver.get("http://www.baidu.com")  

    print('=======')
    sleep(1000)  




# {'http': 'http://lum-customer-%s-zone-%s:%s@zproxy.lum-superproxy.io:22225'%(customer,zone_name,pwd)}))


    #driver.quit()



def test_luminati2():
    from selenium import webdriver
    # http://username:password@localhost:8080
    username = 'caichao'
    password = 'abitpt3isvvj'
    port = 22225
    zone_name = 'zone2'
    PROXY = 'http://lum-customer-%s-zone-%s:%s@zproxy.lum-superproxy.io:22225'%(username,zone_name,password)
    # Create a copy of desired capabilities object.
    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    # Change the proxy properties of that copy.
    desired_capabilities['proxy'] = {
        "httpProxy":PROXY,
        "ftpProxy":PROXY,
        "sslProxy":PROXY,
        "noProxy":None,
        "proxyType":"MANUAL",
        "class":"org.openqa.selenium.Proxy",
        "autodetect":False
    }
    # you have to use remote, otherwise you'll have to code it yourself in python to 
    # dynamically changing the system proxy preferences
    driver = webdriver.Remote("http://localhost:4444/wd/hub", desired_capabilities)    
    driver.get('http://lumtest.com/myip.json')
    time.sleep(2000)







def main():
    sockets = read_proxy()
    print(len(sockets))
    requests = threadpool.makeRequests(test_s5_requests, sockets[:])
    [pool.putRequest(req) for req in requests]
    pool.wait()      

if __name__ == '__main__':
    # test_chrome()
    get_luminati()
    # test_s5_requests('')
