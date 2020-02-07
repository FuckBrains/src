import requests
import json
import sys
sys.path.append("..")


def get_headers():
    headers = {
    ':authority': 'www.ssnregistry.org',
    # ':method': 'POST',
    ':path': '/validate',
    ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.ssnregistry.org',
    'referer': 'https://www.ssnregistry.org/validate',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
    }

def varidate_phone():
    phone = 2489710778
    url = 'http://apilayer.net/api/validate?access_key=1bb8e33a938a9bb0a25b904d51775710&number=%d&country_code=US&format=1'%phone
    resp = requests.get(url)
    print(resp.text)
    print(str(resp))

def get_emails():
    file = r'..\res\email.txt' 
    emails = []
    with open(file,'r') as f:
        emails = f.readlines()
    # print('First 10 emails')
    # print(emails[0:10])
    # print('Last 10 emails')
    # print(emails[-10:])
    emails = [email.replace('\n','') for email in emails]
    return emails

def validate_email(email):
    '''
    Result:
        1: email alive
        2: email not alive
    '''    
    print('email:',email)
    url = 'https://www.consumerconnecting.com/misc/?responsetype=json&action=validateemail&email=%s'%email
    resp = requests.get(url)
    # print(resp.text)
    res = json.loads(resp.text)
    print("res['Result']",res['Result'])
    if res['Result'] == 1:
        print('email alive')
    else:
        print('email not exist')
    # print(str(resp))  
    return res['Result']  

def validate_10088_email(email):
    '''
    Result:
        3:in database
        1: not in database
    '''    
    import time
    stick = int(round(time.time() * 1000))
    url2 = 'https://www.consumerconnecting.com/misc/?responsetype=json&action=campaignstatus&c=235361&email=%s&leadtypeid=9&mailsrc=field&callback=posting.isReturning&uts=%d&uid=5c8f7594-e795-4f00-b670-c43415d65d64'%(email,stick)
    # print(url)
    url = 'http://lumtest.com/myip.json'
    print('email:',email)
    ip = '192.168.89.130'
    port = '25945'
    proxy = 'socks5://%s:%s'%(ip,port)    
    session = requests.session()
    # session.proxies = {'http': proxy,
    #                    'https': proxy}      
    # resp = session.get(url)
    # print(resp.text)
    resp = session.get(url2)
    print(resp.text)    
    # resp = session.get(url)
    # print(resp.text)    
    response = resp.text.replace('posting.isReturning(','').replace(')','')
    res = json.loads(response)
    print("res['Result']",res['Result'])
    # if res['Result'] == 1:
    #     print('email alive')
    # else:
    #     print('email not exist')
    # print(str(resp))  
    return res['Result'] 



def validate_ssn():
    data = {}
    data['_token'] = 'x0SExcS3MxhTKH0V20EeAcNbthGONNPGT8WBWOUJ'
    data['ssn'] = '256480148'

    # print('preparing to add proxy config:',data)
    # data_ = json.dumps(data)
    # headers = get_headers() 
    url = 'https://www.ssnregistry.org/validate/'
    # token = 'x0SExcS3MxhTKH0V20EeAcNbthGONNPGT8WBWOUJ'
    # url_ = 'http://127.0.0.1:22999/api/proxies'
    # url_ = 'http://%s:22999/api/proxies'%ip_lpm
    # print(url_)
    for i in range(1):
        try:
            s = requests.session()
            resp = s.get(url_,headers=headers)
            resp = s.post(url_,data=data)
            # resp = requests.post(url_,data=data)            
            print(resp.text)
            # print('adding new port to luminati success!!!!!!!!!!!!')
            # print(resp)
            # print(type(str(resp)))
            # print(str(resp))
        except Exception as e:
            print(str(e)) 
            print('add new port to luminati failed ..............')     

def main():
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

def test():
    emails = get_emails()
    length = len(emails)
    length = 30
    flags = {}
    flags['bad'] = 0
    for i in range(length):
        print('Email number:',i)
        try:
            flag = validate_10088_email(emails[i])
        except:
            flags['bad'] += 1
            continue
        if str(flag) not in flags:
            flags[str(flag)] = 1
        else:
            flags[str(flag)] += 1
    print(flags)

if __name__ == '__main__':
    email = 'jjames3002@yahoo.com'
    # email = 'mari_san38@yahoo.com.mx'
    validate_10088_email(email)