import requests
from time import sleep
from selenium import webdriver
import Chrome_driver


def cpx_handler():
    # url_lp = 'https://cpx24.net'
    # url_login = 'https://cpx24.net/login'
    # data = {
    # 'menu':'login',
    # 'username':'GrantJoshua',
    # 'password':'Jack123son'
    # }
    # headers = {
    # 'referer':'https://cpx24.net/login',
    # 'Content-Type':'application/x-www-form-urlencoded',
    # 'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    # }
    # s = requests.session()
    # s.get(url_lp)
    # r = s.post(url=url_login,data=data,headers=headers,allow_redirects=True)
    # # sleep(10)
    # r = s.get('https://cpx24.net/dashboard')
    # print(r)
    # print('=================')
    # r = s.get('https://cpx24.net/dashboard/campaigns')
    # print(r.text)    
    # cookies = {
    # '__cfduid':'d94684f618a7314a69cad9ad833e265681553267296',
    # ' __guid':'232594765.2322300367180337000.1553267304335.8572',
    # 'PHPSESSID':'c5111b0f66b6785162c5302e1cd62ceb',
    # 'cf_clearance':'a8823d22690d42fdc757c4f171c09e46843b0715-1567012819-1800-150'
    # }
    cookies = cpx_login()
    s = requests.session()
    r = s.get('https://cpx24.net/dashboard',cookies=cookies)
    print(r.text)
    campaign_handler(s,cookies)
    return s

def cpx_login():
    chrome_driver = Chrome_driver.get_chrome()
    chrome_driver.get('https://cpx24.net/login')
    sleep(5)
    chrome_driver.find_element_by_xpath('//*[@id="username"]').send_keys('GrantJoshua')
    chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys('Jack123son')
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="login"]/p[3]/input').click()
    sleep(3)
    cookies = chrome_driver.get_cookies()
    print(cookies)
    cookies_ = {}
    for i in range(len(cookies)):
        cookies_[cookies[i]['name']] = cookies[i]['value']

    chrome_driver.quit()
    return cookies_


def campaign_handler(s,cookies):
    url_campaigns = 'https://cpx24.net/dashboard/campaigns'
    r = s.get(url_campaigns,cookies=cookies)
    print(r.text)



def main():
    cpx_handler()


if __name__ == '__main__':
    main()
