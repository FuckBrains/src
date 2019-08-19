from sockshandler import SocksiPyHandler
import socks
from urllib.request import build_opener
import threadpool
import random
import sys
sys.path.append("..")
import Chrome_driver



pool = threadpool.ThreadPool(100)
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
    url = 'http://whoer.net'    
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


def test_chrome():
    from selenium import webdriver
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    print(help(webdriver.Chrome))
    return
    myProxy = "207.97.174.134:1080"
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy,
        'ftpProxy': myProxy,
        'sslProxy': myProxy,
        'noProxy': '' # set this value as desired
        })
    driver = webdriver.Chrome(proxy=proxy)
    # driver = webdriver.Chrome(proxy=proxy)
    driver.get("http://www.google.com")    


def main():
    sockets = read_proxy()
    print(len(sockets))
    requests = threadpool.makeRequests(test_s5, sockets[:])
    [pool.putRequest(req) for req in requests]
    pool.wait()      

if __name__ == '__main__':
    test_chrome()

