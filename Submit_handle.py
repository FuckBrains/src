import db
import random
from xlrd import xldate_as_tuple


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
        birthday = [str(random.randint(1,12)),str(random.randint(1,25)) ,str(random.randint(1960,1980))]  
    if len(birthday[0]) == 1:
        birthday[0] = '0'+str(birthday[0])  
    if len(birthday[1]) == 1:
        birthday[1] = '0'+str(birthday[1])  

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


def chansfer_float_into_int(str_float):
    str_int = (str_float.split('.'))[0]
    return str_int


if __name__ == '__main__':
    Mission_list = [10001] 
    Excel_names = ['Auto','Uspd']
    # submit = db.read_one_info(Config['IP_country'],Mission_list,Email_list,Excel_names)
    # print(submit)
    # birthday = get_auto_birthday(submit['Uspd']['date_of_birth'])
    # print(birthday)
