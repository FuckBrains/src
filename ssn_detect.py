import time
import requests
import json
import sys
sys.path.append("..")
from urllib import parse
import xlrd
from xlutils.copy import copy
import threadpool
import threading
import db

def get_headers():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-length': '61',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.ssnregistry.org',
        'referer': 'https://www.ssnregistry.org/validate',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }
    '''
    to change
    XSRF-TOKEN
    laravel_session
    '''
    cookies = {
    '__cfduid':'dcb0dbd4e34dbf751bfa5e6d1042292831580802619',
    '_ga':'GA1.2.1459630284.1581131618',
    '_gid':'GA1.2.539623217.1581131620',
    '__gads':'',
    'ID':'3c7df452b92ae7c0',
    'T':'1580802622',
    'S':'ALNI_MYkIzFc-_-4o_7H1PUHcCnX8SNCZA',
    'XSRF-TOKEN':'eyJpdiI6IkRZRkdhVE4wWlkrMUNNckVCY1A4MVE9PSIsInZhbHVlIjoibllLRUdvbTZPVmsxT2VsRVpXNkF0N1R1WU02OU5OSmx1WGQ1UTEyTDlYMWxNMm9tbGhjRTJ5Q3NSQjdzT0Y4OU1abmZQTHZuV1Q3S1VDWVFGXC9zNWRnPT0iLCJtYWMiOiJhYTk4ZjhmMDlhYjc4NTUyZjQwMTZkZDI0NGU4OGQ5NmUxYTEzMzhiZjIyYTMxZTU2ZGE0M2RhMDRkMDAxZGE2In0',
    'laravel_session':'eyJpdiI6IndYd2E2TDMwNUwyQmFCSEV6Q2R3dVE9PSIsInZhbHVlIjoiZEIxbnI3SjVSWmZnSTc2blBkTXBoVVdOaUZDTVBCYmhIa01XTzhnVURiam1GVUhVTVwvOSs3TVpcL1pZMkp1VGkyQUpaRERaWlNiVXVmcVcrRWh4c3NVdz09IiwibWFjIjoiZDVmZGZkZmU1NWM1NmZjMDM0NjI3NzFlOGYyMWYwNmJmY2ExZTEzYzA0YzM5MTMwZmFhNWJkOGUwNzU3NzI5ZiJ9',
    }

    # stick = int(round(time.time() * 1000))
    return headers,cookies

def get_headers2():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '29',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://socialsecurityofficenear.me',
        'pragma': 'no-cache',
        'referer': 'https://socialsecurityofficenear.me/social-security-numbers/validator/',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
    return headers


def validate_address(Address='',ZipCode=''):
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://cashrequestonline.com',
        'Referer': 'https://cashrequestonline.com/Home/GetStarted?RequestedAmount=1000&ZipCode=85705',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }
    url_ = 'https://www.consumerconnecting.com/LeadProcessing/CheckAddress'
    # Address='P.O Box 434'
    # ZipCode=35068  
    headers['Referer'] = headers['Referer'].replace('85705',str(ZipCode))
    data = {}
    data['Address'] = Address
    data['ZipCode'] = ZipCode
    # print('preparing to add proxy config:',data)
    data_ = parse.urlencode(data)      
    s = requests.session()
    try:
        resp = s.post(url_,data=data_,headers=headers)
    except:
        return -1
    # resp.encoding = 'utf-8'  # 设置编码
    resp.encoding='UTF-8'  
    # resp = requests.post(url_,data=data)            
    # print(resp.apparent_encoding)
    resp_text = resp.text
    # print(resp_text)
    data = json.loads(resp.text)
    flag = 0
    if data['StatusCode'] == 200:
        # print('address alive')
        flag = 1
    else:
        # print('address fake')
        flag = 0
    return flag




def get_first_headers():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }
    return headers

def validate_phone(phone):
    # phone = 2489710778
    url = 'http://apilayer.net/api/validate?access_key=1bb8e33a938a9bb0a25b904d51775710&number=%d&country_code=US&format=1'%int(phone)
    try:
        resp = requests.get(url)
        data = json.loads(resp.text)        
    except:
        return -1
    # print(resp.text)
    # print(str(resp))
    flag = 0
    if data['valid'] == True:
        # print('phone is valid')
        flag = 1
    else:
        # print('phone is not valid')
        flag = 0
    return flag

def validate_routing(routing):
    # routing = 421051540
    url = 'https://www.consumerconnecting.com/misc/?responsetype=json&action=validatebankaba&bankaba=%d&uts=1582817828788&uid=d127367d-6053-4c65-b60b-fb53d7008f10&callback=jQuery2230839557435128814_1582817474953&_=1582817474957'%int(routing)
    try:
        resp = requests.get(url)
        # data = json.loads(resp.text)        
    except:
        return -1
    # print(resp.text)
    resp_txt = resp.text
    resp_text = resp_txt.replace('jQuery2230839557435128814_1582817474953(','').replace(')','')
    data = json.loads(resp_text)
    # print(data['Result'])
    # print(str(resp))
    flag = 0
    if data['Result'] == 1:
        # print('routing is valid')
        flag = 1
    elif data['Result'] == 4:
        # print('routing is not valid')
        flag = 0
    else:
        print(data)
    return flag

def get_emails(file):
    # file = r'..\res\email.txt' 
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
    # print('email:',email)
    url = 'https://www.consumerconnecting.com/misc/?responsetype=json&action=validateemail&email=%s'%email
    resp = requests.get(url)
    # print(resp.text)
    try:
        res = json.loads(resp.text)
    except:
        return -1
    # print("res['Result']",res['Result'])
    flag = 0
    if res['Result'] == 1:
        # print('email alive')
        flag = 1
    else:
        # print('email not exist')
        flag = 0
    # print(str(resp))  
    return flag

def validate_10088_email(email):
    '''
    Result:
        3:in database
        1: not in database
    '''    
    stick = int(round(time.time() * 1000))
    url2 = 'https://www.consumerconnecting.com/misc/?responsetype=json&action=campaignstatus&c=235100&email=%s&leadtypeid=9&mailsrc=field&callback=posting.isReturning&uts=%d&uid=5c8f7594-e795-4f00-b670-c43415d65d64'%(email,stick)
    # print(url)
    url = 'http://lumtest.com/myip.json'
    # print('email:',email)
    ip = '192.168.89.130'
    port = '25945'
    proxy = 'socks5://%s:%s'%(ip,port)    
    session = requests.session()
    # session.proxies = {'http': proxy,
    #                    'https': proxy}      
    # resp = session.get(url)
    # print(resp.text)
    try:
        resp = session.get(url2)
    # print(resp.text)    
    # resp = session.get(url)
        # print(resp.text)   
        response = resp.text.replace('posting.isReturning(','').replace(')','')
        res = json.loads(response)
    except:
        return -1
    # print("res['Result']",res['Result'])
    flag = 0
    if res['Result'] == 1:
        # print('email alive')
        flag = 1
    else:
        # print('email not exist')
        flag = 0
    # print(str(resp))  
    return flag 

def validate_ssn(ssn):
    data = {}
    data['ssn'] = str(ssn)
    data['_token'] = 'IQCWfm8ze7Ktfn2GhkwoPcA9KRWTFtEuvH8ZmeE7'
    # print('preparing to add proxy config:',data)
    data_ = parse.urlencode(data)
    headers,cookies = get_headers()
    first_headers = get_first_headers() 
    url_ = 'https://www.ssnregistry.org/validate/'
    # token = 'x0SExcS3MxhTKH0V20EeAcNbthGONNPGT8WBWOUJ'
    # url_ = 'http://127.0.0.1:22999/api/proxies'
    # url_ = 'http://%s:22999/api/proxies'%ip_lpm
    # print(url_)
    # try:
    for i in range(1):
        s = requests.session()
        # resp = s.get(url_,headers=first_headers)
        # resp_token = resp.text
        # print(resp_token)
        # a = resp_token.find('_token')
        # b = resp_token.find('value',a)
        # c = resp_token.find('">',b)
        # _token = resp_token[b+7:c]
        # print(_token)
        # data['_token'] = _token
        # print('resp.headers:',resp.headers)
        # cookie_set = resp.headers['Set-Cookie']
        # a = cookie_set.find('__cfduid=')
        # b = cookie_set.find(';',a)
        # cookies['__cfduid'] = cookie_set[a+9:b]  
        # cookies['T'] = str(int(cookies['__cfduid'][-10:])+5)
        # print('__cfduid:',a,b)

        # a = cookie_set.find('XSRF-TOKEN=')
        # b = cookie_set.find(';',a)
        # cookies['XSRF-TOKEN'] = cookie_set[a+11:b]   
        # print('XSRF-TOKEN:',a,b)        

        # a = cookie_set.find('laravel_session=')
        # b = cookie_set.find(';',a)
        # cookies['laravel_session'] = cookie_set[a+16:b]
        # print('laravel_session:',a,b)        
        # print('cookies:',cookies)

        resp = s.post(url_,data=data_,headers=headers,cookies = cookies)
        # resp.encoding = 'utf-8'  # 设置编码
        resp.encoding='UTF-8'  
        # resp = requests.post(url_,data=data)            
        # print(resp.apparent_encoding)
        resp_text = resp.text
        # print(resp_text)
        a = resp_text.find(str(ssn))
        ssn_status = 'empty'
        ssn_state = ''
        if a!= -1:
            b = resp_text.find('.</p>',a)
            # print('a and b :',a,b)
            content = 'Social Security number '+resp_text[a:b]
            print('Content is :',content)
            if 'invalid' in content:
                ssn_status = 'invalid' 
            if 'for ' in content:
                state = content[-2:]
                print('State is:',state)
                ssn_status = 'valid' 
                ssn_state = state
        print(ssn_status,ssn_state,ssn)
        ssn = str(ssn)+'.0'
        sql_content = "UPDATE BasicInfo SET ssn_status = '%s' , ssn_state = '%s' WHERE ssn = '%s'" % (ssn_status,ssn_state,ssn)
        # print(sql_content)
        db.Execute_sql([sql_content])
    # except Exception as e:
    #     print(str(e))

def validate_ssn2(ssn):
    headers = get_headers2()
    url = 'https://socialsecurityofficenear.me/social-security-numbers/validator/'
    data = {
        'area': '364',
        'group': '87',
        'series': '9625'  
    }  
    data_ = parse.urlencode(data)
    s = requests.session()
    s.get(url)
    resp = s.post(url,headers=headers,data=data_)
    resp_text = resp.text
    print(resp_text)
    print(resp.headers)
    if 'No match found' in resp_text:
        print('No match found')
    else:
        pass

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


pool = threadpool.ThreadPool(20)
def test_ssn():
    file = r'..\res\ssn.txt' 
    ssns = get_emails(file)
    length = len(ssns)
    print('total %d ssns to test'%length)
    # ssns = ssns[0:20]
    requests = threadpool.makeRequests(validate_ssn, ssns)
    [pool.putRequest(req) for req in requests]
    pool.wait()     

def get_ssn():
    '''
    empty
    ''
    '''
    file = r'..\res\ssn.txt'     
    ssn_empty,ssn_isnull = db.get_ssn()
    # print(ssn_empty[0:3])
    # print(ssn_isnull[0:3])
    ssns_empty = [int(float(item['ssn'])) for item in ssn_empty]
    ssns_isnull = [int(float(item['ssn'])) for item in ssn_isnull]
    with open(file,'w') as f:
        content = ''
        for ssn in ssns_empty:
            content += str(ssn)+'\n'
        for ssn in ssns_isnull:
            content += str(ssn)+'\n'
        f.write(content)

def test_email():
    ssn_status,ssn_state = '',''
    ssn = 275238997
    sql_content = "UPDATE BasicInfo SET ssn_status = '%s' and ssn_state = '%s' WHERE ssn = '%.1f'" % (ssn_status,ssn_state,float(ssn))
    print(sql_content)

def test_email_10088():
    email = 'jerry.griffin@cableone.net'    
    validate_email(email)

if __name__ == '__main__':
    # print(ssn)
    # phone = 7602075622
    # validate_phone(phone)
    # test_ssn()
    routing = 421051540
    validate_routing(routing)