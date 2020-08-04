def get_info(submit):
    email = submit['email']
    pwd = submit['pwd']
    return email,pwd

def gmx_get_link(chrome_driver,submit):
    email,pwd = get_info(submit)
    url = 'gmx.net'
    xpath_email = '//*[@id="freemailLoginUsername"]'
    xpath_pwd = '//*[@id="freemailLoginPassword"]'
    xpath_login = '//*[@id="freemailLoginForm"]/button'
    chrome_driver.find_element_by_xpath(xpath_email).send_keys(email)
    chrome_driver.find_element_by_xpath(xpath_pwd).send_keys(pwd)    
    chrome_driver.find_element_by_xpath(xpath_login).click()