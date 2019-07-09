from time import sleep
from selenium import webdriver

def web_submit(submit):
    # print(submit)    
    chrome_driver = webdriver.Chrome()
    chrome_driver.get('http://www.baidu.com')
    sleep(4)    
    chrome_driver.close()
    chrome_driver.quit()    
    print('7777')


if __name__ == '__main__':
    web_submit(1)