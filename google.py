import requests
from time import sleep

def get_id(key,url_sign):
    url_id = 'https://2captcha.com/in.php?key=281ec4a6084e341f5ebb845513096114&method=userrecaptcha&googlekey=%s&pageurl=%s&json=1'%(key,url_sign)
    id_google = get_response(url_id)
    return id_google

def wait_token(id_google):
    while True:
        url_code = 'https://2captcha.com/res.php?key=281ec4a6084e341f5ebb845513096114&action=get&id=%s&json=1'%(str(id_google))
        token = get_response(url_code)
        if token != 'ERROR_WRONG_CAPTCHA_ID':
            return token
        else:
            sleep(3)

def get_response(url):
    response = requests.get(url)
    res = response.json()['request']
    return res


def get_code():
    url_sign = 'https://elements.envato.com/sign-up'
    key = '6Lcs71EUAAAAAJy8xeSKqmof7E35MsfvQmdrE4DD'
    id_google = get_id(key,url_sign)
    token = wait_token(id_google)
    return code

