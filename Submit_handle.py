import db
import random
from xlrd import xldate_as_tuple
import requests
import json

# Delay, Config, Mission_conf, Email_list  = Cam4_allin.Config_read()

'''
Already handled:
['']
'''


def password_get():
    a = '0123456789'
    b = '!@#$%^&'
    c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    d = 'abcdefghijklmnopqrstuvwxyz'
    num = random.randint(9,15)
    pwd = ''
    for i in range(num):
        num_pwd = random.randint(0,3)
        if i == 5:
            num_pwd = 0
        if i == 7:
            num_pwd = 1            
        if i == 3:
            num_pwd = 2  
        if i == 8:
            num_pwd = 3                         
        if num_pwd == 0:
            pwd += a[random.randint(0,len(a)-1)]
        elif num_pwd == 1:
            pwd += b[random.randint(0,len(b)-1)]
        elif num_pwd == 2:
            pwd += c[random.randint(0,len(c)-1)]
        else :
            pwd += d[random.randint(0,len(d)-1)]                                    
    return pwd

def Submit_handle(submit):
    try:
        submit['Home_phone'] = str(int(submit['Home_phone'])).replace('-','')
        submit['Zip'] = str(int(submit['Zip']))
        if len(submit['Zip']) == 4:
            submit['Zip'] = '0' + submit['Zip']
        if submit['Height_FT'] == '':
            submit['Height_FT'] = str(random.randint(4,7))
        if submit['Height_Inch'] == '':            
            submit['Height_Inch'] = '0'+str(random.randint(7,9))
        if submit['Weight'] == '':                        
            submit['Weight'] = str(int(random.randint(100,200)))
        type_float = type('1')
        print(type(submit['Date_of_birth']))
        if type(submit['Date_of_birth']) == type_float:
            print('===========')
            try:
                date = xldate_as_tuple(submit['Date_of_birth'],0)
                print(date)
            except Exception as e:
                print(str(e))
                date = [str(random.randint(1960,1980))] 
        else:
            # print(date)
            date = [str(random.randint(1960,1980))] 
        print(date)
        for item in date:
            if len(str(item)) == 2:
                if int(item) >= 50:
                    submit['Year'] = '19' + str(item)    
            if len(str(item)) == 4:
                submit['Year'] = str(item)
        submit['Month'] = str(random.randint(1,12))
        submit['Day'] = str(random.randint(1,25))
        submit['handle'] = True   
    except: 
        submit['handle'] = False          
    return submit

def get_zip(zip_):
    zip_ = zip_.split('.')[0]
    if len(zip_) == 4:
        zip_ = '0' + zip_
    return zip_ 

def get_auto_birthday(date):
    if '/' in date:
        birthday = date.split('/')
    elif '-' in date:
        birthday = date.split('-')    
    else:
        # 'MM/DD/Year'
        if '.0' in date:
            birthday_ = xldate_as_tuple(float(date),0)
            birthday = [str(birthday_[1]),str(birthday_[2]),str(birthday_[0])]
        else:
            birthday = [str(random.randint(1,12)),str(random.randint(1,25)) ,str(random.randint(1970,1990))]  
    if len(str(birthday[0])) == 1:
        birthday[0] = '0'+str(birthday[0])  
    if len(str(birthday[1])) == 1:
        birthday[1] = '0'+str(birthday[1]) 
    if len(str(birthday[2])) == 2:
        birthday[2] = '19'+birthday[2]
    if int(birthday[2]) <= 1970:
        birthday[2] = str(random.randint(1970,1990))
    return birthday

def get_height_info():
    num_ft = random.randint(5,7)
    num_in = random.randint(1,9)
    num_weight = random.randint(105,275)
    num_info = {}
    num_info['Height_FT'] = num_ft
    num_info['Height_Inch'] = num_in
    num_info['Weight'] = num_weight
    return num_info

def get_city_by_zip(zip_):
    url = 'https://tools.usps.com/tools/app/ziplookup/cityByZip'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "NSC_uppmt-xbt8-mc=ffffffff3b2237bf45525d5f4f58455e445a4a4212d3; _gcl_au=1.1.1688992039.1565917935; mab_usps=81; _ga=GA1.2.1159374976.1565917935; _gid=GA1.2.577685537.1565917935; _ga=GA1.3.1159374976.1565917935; _gid=GA1.3.577685537.1565917935; kampyleUserSession=1565917958000; kampyleUserSessionsCount=1; kampyleSessionPageCounter=1; _dc_gtm_UA-80133954-3=1; _gat_UA-80133954-3=1",
        "dnt": "1",
        "origin":'https://tools.usps.com',
        "referer":"https://tools.usps.com/zip-code-lookup.htm?citybyzipcode",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }

    data = {
    'zip':zip_
    }
    response = requests.post(url=url,data =data,headers =headers,timeout=10)
    # print(response.text)
    # print(type(response.text))
    response_dict = json.loads(response.text)
    # print(response_dict)
    city = response_dict['defaultCity']
    state = response_dict['defaultState']
    return city,state

    # print(requests.get('https://adpgtrack.com/click/5d43f1a4a03594103a75da46/146827/233486/subaccount').text) 

def chansfer_float_into_int(str_float):
    str_int = (str_float.split('.'))[0]
    return str_int

def transfer_zipcode_into_city():
    with open('testzip.txt') as f:
        lines = f.readlines()
        for line in lines:
            zipcode = line.strip('\n')
            try:
                city,state = get_city_by_zip(zipcode)
                print(city)
            except:
                print('')

def get_phone(phone):
    phone_ = phone.replace('(','').replace(')','').replace('-','')
    if '.' in phone_:
        phone_ = (phone_).split('.')[0]
    return phone_

def get_uk_phone1(phone):
    phone = phone.replace(' ','')
    if phone[0] == '0':
        if phone[0:4] == '0044':
            phone = phone[4:]
        else:
            phone = phone[1:]
    elif phone[0:2] == '44':
        phone = phone[2:]
    elif phone[0:3] == '+44':
        phone = phone[3:]
    return phone

def get_next_payday():
    import datetime
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    if day>=15:
        if month != 2:
            day_pay = 30
        else:
            day_pay = 28
    else:
        day_pay = 15
    month_word = ['January','February','March','April','May','June','July','August','September','October','November','December']
    month_list = [i+1 for i in range(12)]
    index = month_list.index(month)
    month = month_word[index]
    date = []
    date = [month,day_pay,year,]
    return date

if __name__ == '__main__':
    date = get_next_payday()
    print(date)
