import luminati
import threading
import threadpool
import db
from time import sleep




pool = threadpool.ThreadPool(5)

def traffic_test(traffic):
    port = traffic['port_lpm']
    ip = traffic['ip_lpm']
    url = traffic['url_link']    
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



def main():
    while True:
        account = db.get_account()
        plan_id = account['plan_id']    
        traffics = db.read_plans(plan_id)
        print(traffics)
        print(len(traffics))
        ip_lpm = account['IP']
        ports_used = luminati.ports_get(ip_lpm)
        if len(ports_used) == 0:
            basic_port = 24000
        else:
            basic_port = max(ports_used) 
        print('Basic_port:',basic_port) 
        for traffic in traffics:
            traffic['port_lpm'] = basic_port + 1
            basic_port += 1
            print(basic_port)
            print(traffic['Country'],traffic['port_lpm'])
            luminati.add_proxy(traffic['port_lpm'],country=traffic['Country'],proxy_config_name='zone2',ip_lpm=ip_lpm)
        # return
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

if __name__ == '__main__':
    main()


