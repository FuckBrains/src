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
    from requests_html import HTMLSession
    session = HTMLSession()
    proxy = {"http": "socks5://"+socket_s5,"https": "socks5://"+socket_s5}
    url = "https://www.google.co.jp"
    req = session.get(url, proxies=proxy)
    print(req.text)    


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
    options = webdriver.ChromeOptions()
    PROXY_IP = '94.74.182.134:4145'
    options.add_argument("--proxy-server=%s" % PROXY_IP)
    driver = webdriver.Chrome(chrome_options=options)
    # driver = webdriver.Chrome(proxy=proxy)
    # driver = webdriver.Chrome(proxy=proxy)
    driver.get("http://www.google.com")  
    print('=======')
    sleep(1000)  


def main():
    sockets = read_proxy()
    print(len(sockets))
    requests = threadpool.makeRequests(test_s5_requests, sockets[:])
    [pool.putRequest(req) for req in requests]
    pool.wait()      

if __name__ == '__main__':
    # test_chrome()
    main()

