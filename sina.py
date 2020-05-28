# _*_ coding:utf-8 _*_
# import pytesseract
import time
import Chrome_driver
import json
import requests
import base64
from io import BytesIO
from PIL import Image
from sys import version_info


def main():
    url = 'https://weibo.com/u/5818390567/home?wvr=5&sudaref=graph.qq.com'
    chrome_driver = Chrome_driver.get_chrome() 
    chrome_driver.get(url)
    xpath_name = '//*[@id="loginname"]'
    xpath_pwd = '//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input'
    xpath_captcha = '//*[@id="pl_login_form"]/div/div[3]/div[3]/a/img'
    xpath_capt_input = '//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input'
    xpath_button = '//*[@id="pl_login_form"]/div/div[3]/div[6]/a'    
    element_name = chrome_driver.find_element_by_xpath(xpath_name)
    element_name.send_keys('zxcas')
    time.sleep(1)
    chrome_driver.find_element_by_xpath(xpath_pwd).send_keys('Jack123son')
    imgelement = chrome_driver.find_element_by_xpath(xpath_captcha)
    for i in range(5):
    	if  imgelement.is_displayed() == True:
    		print('see captcha displayed')
    		break
    	else:
    		print('click')
    		chrome_driver.find_element_by_xpath(xpath_button).click()
    		time.sleep(3)
    # time.sleep(15)
    chrome_driver.save_screenshot('C:\\printscreen.png')

    print(imgelement)
    img_path = 'C:\\save.png'
    imgelement.screenshot(img_path)
    img = Image.open(img_path)
    result = base64_api(uname='nv', pwd='Jack123son', img=img)
    print(result)
    chrome_driver.find_element_by_xpath(xpath_capt_input).send_keys(result)  
    time.sleep(1)
    element_name.clear()
    element_name.send_keys('2507461149@qq.com')
    time.sleep(1)
    chrome_driver.find_element_by_xpath(xpath_button).click()
    time.sleep(3000)

    # location = imgelement.location  # 获取验证码x,y轴坐标
    # print('location:',location)
    # # for locate in location:
    # # 	if int(locate)<0:
    # # 		locate = 0
    # size = imgelement.size  # 获取验证码的长宽
    # print('size:',size)
    # rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
    #           int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    # i = Image.open("C:\\printscreen.png")  # 打开截图
    # frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    # print('rangle:',rangle)
    # frame4.save('C:\\save.png') # 保存我们接下来的验证码图片 进行打码time
    # time.sleep(3000)





def base64_api(uname, pwd,  img):
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


if __name__ == "__main__":
	main()

