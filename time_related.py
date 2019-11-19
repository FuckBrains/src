import datetime
import os  
import time  
import ntplib  
from time import sleep
import time
from wrapt_timeout_decorator import *
import time
from functools import wraps
import db

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running : %s seconds" %
            (str(t1-t0))
            )
        return result
    return function_timer



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
    # while True:
    # 	i = 0
    # 	try:
    os.system("tzutil /s \"AUS Central Standard Time\"")
    # os.system("tzutil /l")    
    # sleep(5)
    # c = ntplib.NTPClient()
    # response = c.request('pool.ntp.org')
    # ts = response.tx_time
    # _date = time.strftime('%m-%d-%Y',time.localtime(ts))
    # _time = time.strftime('%X',time.localtime(ts))
    # print(_date,_time)
    # os.environ['TZ'] = 'Asia/Shanghai'
    os.system("tzutil /g")        
    # print(os.system("tzutil /l "))    		
    # os.system('date {} && time {}'.format(_date,_time))
    	# 	break
    	# except Exception as e:
    	# 	i += 1
    	# 	if i >= 20:
    	# 		break 
    	# 	print('Fail to update system for',str(i),'times,try again.')
    	# 	pass



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

@fn_timer
def test_db_time():
    config = db.read_plans(-1)
    Config = config[0]
    Config['Email_Id'] = '1234'
    Config['BasicInfo_Id'] = '123123123'
    Email_list = {"hotmail.com": 1, "outlook.com": 1, "yahoo.com": 1, "aol.com": 1}    
    Mission_Ids,Excels_dup = [Config['Mission_Id']],Config['Excel']
    # print(Excels_dup)
    # print(Config)
    Info_dicts = db.read_one_excel_(Mission_Ids,Excels_dup,Email_list)    
    print(Info_dicts)

    # submit = db.get_luminati_submit(config[0])
    # print(len(submit))

def main_():
    update_time_system()

if __name__ == '__main__':
    # time_3=time_threeday_after()
    main_()
    