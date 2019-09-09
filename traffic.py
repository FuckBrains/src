import luminati
import threading
import threadpool
import db




pool = threadpool.ThreadPool(5)

def traffic_test(traffic):
    port = traffic['port_lpm']
    ip = traffic['ip_lpm']
    url = traffic['url_link']    
    click = 400
    for i in range(click):
        print(i)
        luminati.refresh_proxy(ip,port)
        luminati.get_lpm_ip(ip,port,url = url,debug=1)



def main():
    account = db.get_account()
    plan_id = account['plan_id']    
    traffics = db.read_plans(-1)
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
        luminati.add_proxy(traffic['port_lpm'],country=traffic['Country'],ip_lpm=ip_lpm)
    # return
    requests = threadpool.makeRequests(traffic_test, traffics)
    [pool.putRequest(req) for req in requests]
    pool.wait()     


if __name__ == '__main__':
    main()


