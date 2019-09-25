import datetime
import os  
import time  
import ntplib  
from time import sleep
import time
from wrapt_timeout_decorator import *


@timeout(5)
def mytest(message):
    # this example does NOT work on windows, please check the section
    # "use with Windows" in the README.rst
    print(message)
    for i in range(1,3):
        time.sleep(1)
        print('{} seconds have passed'.format(i))


def Time_start():
    starttime = datetime.datetime.utcnow()
    # print(str(starttime)[:19])
    return str(starttime)[:19]

#long running
def Time_end():
    endtime = datetime.datetime.utcnow()
    print(endtime)
    return str(endtime)[:19]

def Time_used(starttime,endtime):    
    time_used = (endtime - starttime).seconds
    return time_used

def update_time_system():
    while True:
    	i = 0
    	try:
    		os.system("tzutil /s \"China Standard Time\"")
    		sleep(5)
    		c = ntplib.NTPClient()
    		response = c.request('pool.ntp.org')
    		ts = response.tx_time
    		_date = time.strftime('%m-%d-%Y',time.localtime(ts))
    		_time = time.strftime('%X',time.localtime(ts))
    		print(_date,_time)
    		os.environ['TZ'] = 'Asia/Shanghai'
    		print(os.system("tzutil /l "))    		
    		
    		os.system('date {} && time {}'.format(_date,_time))
    		break
    	except Exception as e:
    		i += 1
    		if i >= 20:
    			break 
    		print('Fail to update system for',str(i),'times,try again.')
    		pass



def time_threeday_after():
    time_now = datetime.datetime.utcnow()
    time_delta = datetime.timedelta(hours=-24*3)
    # print(time_delta)
    invalid_time = str(time_now - time_delta)
    # print(invalid_time) 
    return invalid_time


def utc_time_compare(time_compare):
    # import datetime   
    # time_delta = datetime.timedelta(hours=-24*3) 
    # time_now = datetime.datetime.utcnow() 
    # # print(type(time_now))
    # print(time_delta)
    # # sleep(10)
    try:
        a = datetime.datetime.utcnow() > datetime.datetime.strptime(time_compare,"%Y-%m-%d %H:%M:%S")
    except Exception as e:
        a = 'True'
    # time_after = datetime.datetime.utcnow()
    # invalid_time = str(time_now - time_after)   
    # print(invalid_time) 
    return a 


def getactivatetime(b):

    # b = datetime.datetime(2019,9,15,10,10,10)
    # print(b)
    a1 = b + datetime.timedelta(hours=24*1)
    a2 = b + datetime.timedelta(hours=24*2)
    a3 = b + datetime.timedelta(hours=24*3)
    a4 = b + datetime.timedelta(hours=24*4)
    a5 = b + datetime.timedelta(hours=24*5)
    a6 = b + datetime.timedelta(hours=24*6)    
    a7 = b + datetime.timedelta(hours=24*7)
    a = datetime.datetime.now()
    # print(a1,a2,a3,a4,a5,a6,a7)
    # print('system time :',a)
    if a>a7:
        # print(a)
        return 0
    elif a<a1 :
        # print(a)
        return 0
    elif a1<=a <a2:
        # print('Activate1.............')
        return 1
    elif a2<=a<a3:
        return 0
    elif a3<=a<a4:
        # print('Activate2.............')
        return 2
    elif a4<=a<a5:
        return 0
    elif a5<=a<a6:
        # print('Activate3...............')
        return 3
    else:
        return 0






if __name__ == '__main__':
    # time_3=time_threeday_after()
    test()
    