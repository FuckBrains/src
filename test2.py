import db
import test
import ssn_detect
import Chrome_driver
from time import sleep
import random
from selenium import webdriver
import Submit_handle

def test_1():
    Mission_Id =10095
    pages = db.get_page_flag(Mission_Id)
    print(pages)

def test_10088():
    email = 'ag_1977@live.com'    
    ssn_detect.validate_10088_email(email)

def test_2():
    chrome_driver = Chrome_driver.get_chrome()
    url = 'http://falbk.top/click.php?c=5&key=yift22rta15kfnq9upqfowq9'
    chrome_driver.get(url)
    sleep(1000)

def test_3():
    sql_content = 'Select Basicinfo_Id,home_phone,work_phone from Basicinfo where Excel_name="Us_pd_native"'
    response = db.Execute_sql_single([sql_content])    
    # print(response)
    excels = [[key[0],key[1]] for key in response[0] if key[1]==key[2]]
    print(excels)
    print(len(excels))
    sql_contents = []
    for key in excels: 
        phone = key[1]
        for i in range(15):
            num = random.randint(0,9) 
            if int(phone[-3])!= num:
                print(phone[-3],num)
                phone = phone[:-3]+str(num)+phone[-2:]
                print(phone)
                break
        sql_content = "UPDATE Basicinfo SET work_phone = %s WHERE Basicinfo_Id = '%s'" % (phone,key[0])
        sql_contents.append(sql_content)
    db.Execute_sql(sql_contents)    
    # print(excels)
    # sql_contents = []
    # for excel in excels:
    #     sql_content = 'SELECT * from BasicInfo  WHERE Excel_name = "%s"'%excel
        
    #     response = db.Execute_sql_single(sql_content)

def test_4():
    info = {'Alliance_name': 'Convert2Media', 'Number of Offers': '4000+', 'Commission Type': 'CPA, CPL, CPI, Pay per call', 'Minimum Payment': '$100', 'Payment Frequency': 'Net-15,Weekly', 'Payment Method': 'Check,PayPal,Wire,Payoneer,Direct Deposit', 'Referral Commission': 'N/A', 'Tracking Software': 'CAKE', 'Tracking Link': 'http://clickztrax.com/?a=', 'Skypes': 'publishers@convert2media.com,1-800-689-1260', 'alliance_url': 'http://www.convert2media.com/'}    
    print(info)
    keys_detect = ['Alliance_name','Skypes','Number of Offers','Commission Type','Minimum Payment','Payment Frequency','Payment Method','Referral Commission','Tracking Software','Tracking Link']
    for key in keys_detect:
        if key not in info:
            print(key,'of info not in keys of database')
            info[key] = ''
    Alliance_name = info['Alliance_name']
    print(Alliance_name)    
    sql_contents = ['use emu','show tables','INSERT IGNORE INTO alliances(Alliance_name,Skypes,NumberofOffers)values("%s","%s","%s")'%("test",'111','222')]
    db.Execute_sql(sql_contents)
    # infos = [info]
    # db.upload_alliance_info(infos) 

def test_oxylabs():
    import urllib.request
    import random
    username = 'r782992280'
    password = 'nV3nqFtt9S'
    country = 'us'
    session = random.random()
    entry = ('http://customer-%s-cc-%s-sesstime-30:%s@pr.oxylabs.io:7777' %
        (username, country, password))
    query = urllib.request.ProxyHandler({
        'http': entry,
        'https': entry,
    })
    execute = urllib.request.build_opener(query)
    for i in range(3000):
        print(i+1)
        print(execute.open('https://ipinfo.io').read())
        sleep(5)

def test_chrome():
    from selenium.webdriver.common.proxy import ProxyType, Proxy

    options = webdriver.ChromeOptions()
    # options.add_argument('user-agent=' + ua)
    # account_lpm = luminati.get_account()
    # ip = account_lpm['IP_lpm']
    # print(ip)
    # port = submit['port_lpm']
    # proxy = 'socks5://%s:%s'%(ip,str(port))
    path_driver = Chrome_driver.get_chromedriver_path()
    print(path_driver)
    username = 'r782992280'
    password = 'nV3nqFtt9S'
    country = 'us'    
    # proxy = 'http://customer-%s-cc-%s-sesstime-30:%s@pr.oxylabs.io:7777'%(username, country, password)   
    super_proxy_url = 'http://customer-%s-cc-%s-sesstime-30:%s@pr.oxylabs.io:7777'%(username, country, password)  
    # proxy = 'http://lum-customer-%s-zone-%s-session-%s:%s@zproxy.superproxy.io:22225'%(username,zone_name,session_id,password,port)
    print(super_proxy_url)
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': super_proxy_url,
        'ftpProxy': super_proxy_url,
        'sslProxy': super_proxy_url,
        'noProxy': ''  # set this value as desired
    })    
    options.add_argument('--proxy-server=%s'%proxy)    
    chrome_driver = webdriver.Chrome(chrome_options=options,executable_path=path_driver)    
    return chrome_driver    


# def test_chrome_proxy():
    

def get_employer():
    submit = {
        'employer':'aaaa'
    }
    employer = Submit_handle.get_employer_info(submit)
    return employer
    # employer = [key[0] for key in res]
    # print(len(employer))
    # print('first 10')
    # print(employer[:10])
    # print('last time')
    # print(employer[-10:])


def main():
    # test_10088()
    # test.test_write()
    email = 'ricdevin@yahoo.com'
    # email=''
    # ssn_detect.validate_10088_email(email)
    routing = '2857880817'
    ssn_detect.validate_routing(routing)
    # Address = '237 BURNING TREE DRIVE'
    # ZipCode = 95119
    # ssn_detect.validate_address(Address,ZipCode)

if __name__ == '__main__':
    db.get_driver_license()