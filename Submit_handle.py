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



if __name__ == '__main__':
    # Mission_list = [10001] 
    # Excel_names = ['Auto','Uspd']
    # submit = db.read_one_info(Config['IP_country'],Mission_list,Email_list,Excel_names)
    # print(submit)
    # birthday = get_auto_birthday(submit['Uspd']['date_of_birth'])
    # print(birthday)
    # [print(get_auto_birthday('')) for i in range(100)]
    # for i in range(500):
    #     birthday = get_auto_birthday('')
        # print(birthday[0]+'-'+birthday[1]+'-'+birthday[2])
    # city,state = get_city_by_zip(18444)
    # print(city,state)
    # transfer_zipcode_into_city()
    day=get_auto_birthday('')
    print(day)
