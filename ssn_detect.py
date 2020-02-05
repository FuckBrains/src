import requests


def get_headers():
    headers = {
    ':authority': 'www.ssnregistry.org',
    ':method': 'POST',
    ':path': '/validate',
    ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': '__cfduid=dcb0dbd4e34dbf751bfa5e6d1042292831580802619; _ga=GA1.2.1839060536.1580802621; _gid=GA1.2.1620766078.1580802621; __gads=ID=3a46765ac7bc8fe6:T=1580802622:S=ALNI_Ma8LEnD1T-8aNy2Ju0EClB8F-1J2w; XSRF-TOKEN=eyJpdiI6IlU2Z0diS2pqZVMrWk9zZXJpdExRUXc9PSIsInZhbHVlIjoiWCtUamtTV1RpRUFMS3M4V2RnWTlxYUoxdDNlaTF2a0tTclwvT29cLzlyUHQ5NDlRWWdzd3I4OTBCOGtUSzI3TExpN1ZTT3A0TUtSSFBQS1o1ck9aODRtQT09IiwibWFjIjoiNzVhMWEwNGE3Y2U2YjFiODg2NDdkMDUyY2ZmNjI1YTFjNGEwYmUxNzhhZDg4ZjQzYmI5OGQ4ZTM0YmVhNzU3YSJ9; laravel_session=eyJpdiI6IjdHcDdhVDVvQWV2enc1MEFxU2psY0E9PSIsInZhbHVlIjoiR2lOeXFuQmk3bzMrYTRuVEdpbHB0Z2FvdzhYUFk5NFNVN3lPZ1lRa25La24wN3BoNUI1T3FzSVBVNlA0VEhMR1JDVG5yWTVIWlVKMDVSNHNmUDRxS3c9PSIsIm1hYyI6ImNhYzNhMjM1YzlmNTYyOWRhMjkwY2JjY2JmOTEwNGM4ZWNhZWEwNjZiZmI3ZmFmMjQxNmQzODhjOTllMGI4ZjYifQ%3D%3D',
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

def validate_ssn():
    data = {}
    data['_token'] = 'BxJjgSPgCwC5PXmTNVLGlnfj3q6szSBUYFIxFqLl'
    data['ssn'] = '256480148'

    # print('preparing to add proxy config:',data)
    # data_ = json.dumps(data)
    headers = get_headers() 
    # url_ = 'http://127.0.0.1:22999/api/proxies'
    # url_ = 'http://%s:22999/api/proxies'%ip_lpm
    # print(url_)
    flag = 0
    for i in range(1):
        try:
            resp = requests.post(url_,data=data_,headers=headers)
            print('adding new port to luminati success!!!!!!!!!!!!')
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

if __name__ == '__main__':
    varidate_phone()