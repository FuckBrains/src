


def caiji():
    import requests
    import Chrome_driver
    session = requests.session()
    # session.proxies = {'http': proxy,
    #                    'https': proxy} 
    print('http://lumtest.com/myip.json')
    url = 'https://www.affplus.com/?networks%5B0%5D=cpagrip'
    ua = Chrome_driver.get_ua()
    headers = {
        'ua':ua
    }
    try:
        resp=session.get(url,headers=headers,timeout=10)
        print('===')
    except Exception as e:
        print(str(e))
    print(resp.text)      


if __name__ == '__main__':
    caiji()

