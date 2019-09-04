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
    uas = get_ua_all()
    ua = get_ua_random(uas)
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept - Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
        # 'Connection': 'Keep-Alive',
        'User-Agent': ua
    }
    url = 'https://adpgtrack.com/click/5d43f1a4a03594103a75da46/146827/233486/subaccount'    
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
    except:
        print('connect failed')
        pass    

def get_ua_all():
    uas = []
    with open(r'ua.txt') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip('\n') != '':
                if 'Windows' not in line:
                    continue 
                if 'Chrome' in line:
                    uas.append(line.strip('"').strip("'").strip('\n'))

    # for ua in uas.split('/n'):
        # print(ua)
    return uas

def get_ua_random(uas):
    num = random.randint(0,len(uas)-1)
    # print(uas[num])
    return uas[num]


def test_s5_requests(socket_s5):
    import socket
    import socks
    import requests
    proxy_s5 = socket_s5.split(':')
    print(proxy_s5)
    proxyaddr_ = proxy_s5[0]
    proxyport_ = int(proxy_s5[1])    
    socks.set_default_proxy(socks.SOCKS5, proxyaddr_, proxyport_)
    socket.socket = socks.socksocket
    try:
        print(requests.get('https://adpgtrack.com/click/5d43f1a4a03594103a75da46/146827/233486/subaccount').text) 
        print(requests.status)   
    except Exception as e:
        print(str(e))
        print('failed')
        pass


def test_size():
    import requests
    


def main():
    sockets = read_proxy()
    requests = threadpool.makeRequests(test_s5_requests, sockets)
    [pool.putRequest(req) for req in requests]
    pool.wait()      

if __name__ == '__main__':
    main()

