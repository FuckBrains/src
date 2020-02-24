import sys
from luminati import ip_test,get_port_random,delete_port_s,add_proxy,get_lpm_ip
import threading
import threadpool
from db import update_port,get_account,read_plans
from time import sleep
import Chrome_driver



pool = threadpool.ThreadPool(50)

def traffic_test(traffic):
    uas = Chrome_driver.get_ua_all()
    ua = Chrome_driver.get_ua_random(uas)
    # print(ua)
    traffic['ua'] = ua    
    click = 10000
    referer = ''
    i = 0
    while True:    
        flag,proxy_info = ip_test(traffic['port_lpm'])
        print(flag,proxy_info,'\n=========================')
        if flag == 1:
            pass
        elif flag == -1:
            print('bad port,change into new')
            port_new = get_port_random()
            update_port(traffic['port_lpm'],port_new)
            delete_port_s(traffic['port_lpm'])                
            traffic['port_lpm'] = port_new
            print(port_new)
            try:
                add_proxy(port_new,country=traffic['Country'],proxy_config_name='zone2',ip_lpm=traffic['ip_lpm'])
                continue
            except Exception as e:
                print(str(e))
                continue
    # for i in range(click):
        print('Sending traffic:',i+1,'clicks for mission',traffic['Mission_Id'])
        # luminati.refresh_proxy(traffic['ip_lpm'],traffic['port_lpm'])
        if traffic['traffic_method'] == 'Crawl':
            print('Crawl')
            # print('fffffffffffffffffffffffff')
            try:
                get_lpm_ip(traffic['port_lpm'],url = traffic['url_link'],Referer = referer,debug=1)
            except Exception as e:
            	print(str(e))
        else:
            try:
                print('+++++++++++++++++++++++++++')
                get_unique_traffic(traffic)
            except:
                pass
        i += 1
    delete_port_s(traffic['port_lpm'])

def main(i):
    for j in range(111):
        account = get_account()
        plan_id = account['plan_id']    
        traffics = read_plans(i)
        print(traffics)
        # print(len(traffics))
        ip_lpm = account['IP']
        for traffic in traffics:
            # traffic['key'] = 'getaround'
            traffic['port_lpm'] = get_port_random()
            # traffic['Record'] = 3            
            # print('===========================')
            # print(traffic['Country'],traffic['port_lpm'])
            # luminati.add_proxy(traffic['port_lpm'],country=traffic['Country'],proxy_config_name='zone2',ip_lpm=ip_lpm)
            add_proxy(traffic['port_lpm'],country=traffic['Country'],proxy_config_name='zone2',ip_lpm=ip_lpm)            
        requests = threadpool.makeRequests(traffic_test, traffics)
        [pool.putRequest(req) for req in requests]
        pool.wait() 
        print('finish sending traffic,sleep for 30')
        # sleep(30)

def test():
    traffic = {}
    traffic['port_lpm'] = 24000
    traffic['Country'] = 'us'
    traffic['ip_lpm'] = '192.168.89.130'
    while True:    
        flag,proxy_info = ip_test(traffic['port_lpm'])
        print(flag,proxy_info,'\n=========================')
        if flag == 1:
            pass
        elif flag == -1:
            print('bad port,change into new')
            port_new = get_port_random()
            update_port(traffic['port_lpm'],port_new)
            delete_port_s(traffic['port_lpm'])                
            traffic['port_lpm'] = port_new
            print('New port:',port_new)
            try:
                add_proxy(port_new,country=traffic['Country'],proxy_config_name='zone2',ip_lpm=traffic['ip_lpm'])
            except Exception as e:
                print(str(e))

def get_unique_traffic(traffic):
    traffic['traffic'] = True
    chrome_driver = Chrome_driver.get_chrome(traffic)
    # traffic['url_link'] = 'https://www.moneymethods.net'
    chrome_driver.get(traffic['url_link'])
    for i in range(15):
        # print(chrome_driver.current_url)
        if traffic['traffic_key'] in chrome_driver.title:
            # sleep(500)
            # sleep(15)
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
    paras=sys.argv
    i = int(paras[1])
    # i = 9
    main(i)
    # test()


