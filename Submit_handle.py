import db
import Cam4_allin
import random
from xlrd import xldate_as_tuple


Delay, Config, Mission_conf, Email_list  = Cam4_allin.Config_read()

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


if __name__ == '__main__':
    Mission_list = [10001] 
    submit = db.read_one_info(Config['IP_country'],Mission_list,Email_list)
    print(submit)
    Submit_handle(submit)
    print(submit)
