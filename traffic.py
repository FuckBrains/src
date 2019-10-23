import sys
import luminati
import threading
import threadpool
import db
from time import sleep
import Chrome_driver



pool = threadpool.ThreadPool(20)

def traffic_test(traffic):
    uas = Chrome_driver.get_ua_all()
    ua = Chrome_driver.get_ua_random(uas)
    print(ua)
    traffic['ua'] = ua    
    click = 10
    referer = ''
    while True:    
        flag = luminati.ip_test(traffic['port_lpm'])
        print(flag,'=========================')
        if flag == 1:
            break
        elif flag == -1:
            print('bad port,change into new')
            port_new = luminati.get_port_random()
            db.update_port(traffic['port_lpm'],port_new)
            luminati.delete_port_s(traffic['port_lpm'])                
            traffic['port_lpm'] = port_new
            print(port_new)
            try:
                luminati.add_proxy(port_new,country=traffic['Country'],proxy_config_name='zone2',ip_lpm=traffic['ip_lpm'])
            except Exception as e:
                print(str(e))
    for i in range(click):
        print(i)
        # luminati.refresh_proxy(traffic['ip_lpm'],traffic['port_lpm'])
        if traffic['method'] == 1:
            try:
                luminati.get_lpm_ip(traffic['port_lpm'],url = traffic['url_link'],Referer = referer,debug=1)
            except Exception as e:
            	print(str(e))
        else:
            get_unique_traffic(traffic)
    luminati.delete_port_s(traffic['port_lpm'])

def main(i):
    while True:
        account = db.get_account()
        plan_id = account['plan_id']    
        traffics = db.read_plans(i)
        print(traffics)
        print(len(traffics))
        ip_lpm = account['IP']
        for traffic in traffics:
            traffic['method'] = 1
            traffic['key'] = 'consumerrewards.us.com'
            traffic['port_lpm'] = luminati.get_port_random()
            print(traffic['Country'],traffic['port_lpm'])
            # luminati.add_proxy(traffic['port_lpm'],country=traffic['Country'],proxy_config_name='zone2',ip_lpm=ip_lpm)
            luminati.add_proxy(traffic['port_lpm'],country=traffic['Country'],proxy_config_name='zone2',ip_lpm=ip_lpm)            
        requests = threadpool.makeRequests(traffic_test, traffics)
        [pool.putRequest(req) for req in requests]
        pool.wait() 
        print('finish sending traffic,sleep for 30')
        sleep(30)

def test():
    port = 24058
    ip = '192.168.30.131'
    url = 'http://track.meanclick.com/im/click.php?c=19&key=uy140s20ieojce6k1i1qilwg'    
    click = 99999
    referer = ''
    for i in range(click):
        print(i)
        luminati.refresh_proxy(ip,port)
        try:
            luminati.get_lpm_ip(ip,port,url = url,Referer = referer,debug=1)
        except Exception as e:
            print(str(e))
    luminati.delete_port([port])  

def get_unique_traffic(traffic):
    traffic['traffic'] = True
    chrome_driver = Chrome_driver.get_chrome(traffic)
    chrome_driver.get(traffic['url_link'])
    for i in range(15):
        print(chrome_driver.current_url)
        if traffic['key'] in chrome_driver.current_url:
            chrome_driver.close()
            chrome_driver.quit()
        else:
            sleep(1)
    try:
        chrome_driver.close()
        chrome_driver.quit()
    except:
        pass

if __name__ == '__main__':
    # paras=sys.argv
    # i = int(paras[1])
    i = 9
    main(i)


