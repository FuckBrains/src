from selenium import webdriver
from time import sleep
import requests
import threadpool
import db

Flag_sql = 1

pool = threadpool.ThreadPool(200)

def read_proxy():
	proxys = []
	with open('vipsocks.txt') as f:
		while True:
			line = f.readline()
			if line == '':
				break
			if ':' in line:
				proxys.append(line.strip('\n'))
	return proxys


def test_whoer_post(proxy=None):
	# ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
	# headers = {'User-Agent': ua}
	proxies = {'http': proxy,'https':proxy} 
	url = 'https://whoer.net' 
	response = requests.get(url, proxies=proxies) 
	# response = requests.get(url) 
	print('Success getting to whoer!!!!!!!')
	print((response.content)[0:100]) 


def test_whoer_selenium(proxy=None):
    service_args = [
    '--proxy='+proxy,
    '--proxy-type=socks5',
    ]
    chrome_driver=webdriver.Chrome(service_args=service_args)
    chrome_driver.get('https://whoer.net')
    sleep(1000)


def test_proxy(proxy):
	try:
		print('Using proxy:',proxy)
		test_whoer_post(proxy)
		values = [proxy,'Socket5','Good']
		print(values)
		global Flag_sql
		try:
			while Flag_sql == 0:
				sleep(3)
			db.update_ip_pools(values)
			print('Uploading ip',Flag_sql)
		except Exception as e:
			print('================')
			print(e)
		Flag_sql = 1
	except Exception as e:
		print(str(e))
		print('Fail to connect whoer')	



def multi_test_proxy(proxys):
    reqs = threadpool.makeRequests(test_proxy, proxys)
    [pool.putRequest(req) for req in reqs]
    pool.wait() 	


if __name__ == '__main__':
	# test_whoer_post()
	proxys=read_proxy()
	print(len(proxys))
	multi_test_proxy(proxys)
