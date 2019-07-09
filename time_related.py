import datetime
import os  
import time  
import ntplib  
from time import sleep


def Time_start():
    starttime = datetime.datetime.utcnow()
    # print(str(starttime)[:19])
    return str(starttime)[:19]

#long running
def Time_end():
    endtime = datetime.datetime.utcnow()
    print(endtime)
    return str(endtime)[:19]

# def Time_used(starttime,endtime):    
#     time_used = (endtime - starttime).seconds
#     return time_used

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
    		# os.environ['TZ'] = 'Asia/Shanghai'
    		# print(os.system("tzutil /l "))    		
    		
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


if __name__ == '__main__':
    print(time_threeday_after)
    