from time import sleep 




def scroll_and_find(chrome_driver,element):
	target = chrome_driver.find_element_by_xpath(element) 
	chrome_driver.execute_script("arguments[0].scrollIntoView();", target)
	js="var q=document.documentElement.scrollTop=-300"
	chrome_driver.execute_script(js) 
	sleep(3)
	return target

def scroll_and_find_up(chrome_driver,element):
	target = chrome_driver.find_element_by_xpath(element) 
	chrome_driver.execute_script("arguments[0].scrollIntoView();", target)
	# js="var q=document.documentElement.scrollTop=-300"
	# chrome_driver.execute_script(js) 
	sleep(3)
	return target



def overlay_click(chrome_driver,element):
	js = 'arguments[0].click();'
	chrome_driver.execute_script(js) 


