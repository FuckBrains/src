import requests
from time import sleep

def get_id():
    url_sign = 'https://elements.envato.com/sign-up'
    key = '6Lcs71EUAAAAAJy8xeSKqmof7E35MsfvQmdrE4DD'    
    url_id = 'https://2captcha.com/in.php?key=281ec4a6084e341f5ebb845513096114&method=userrecaptcha&googlekey=%s&pageurl=%s&json=1'%(key,url_sign)    
    id_google = get_response(url_id)
    print(id_google)
    return id_google

def wait_token(id_google):
    i = 1
    while True:
        url_code = 'https://2captcha.com/res.php?key=281ec4a6084e341f5ebb845513096114&action=get&id=%s&json=1'%(str(id_google))
        token = get_response(url_code)
        if token != 'CAPCHA_NOT_READY':
            return token
        else:
            print(token,i)
            sleep(3)

def get_response(url):
    response = requests.get(url)
    print('get_response:',response)
    res = response.json()['request']
    return res


def get_token(id_google):
    print('id_google:',id_google)
    token = wait_token(id_google)
    print('token:',token)
    return token

def get_js(id_google):
    token = get_token(id_google)
    js = 'document.getElementById("g-recaptcha-response").innerHTML="%s";'%token
    print(js)
    return js


if __name__ == '__main__':
    get_js(id_google)


