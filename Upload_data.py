import xlrd
from xlutils.copy import copy
from xlrd import xldate_as_tuple
import Get_conf
sys.path.append("..")
from res import db




def read_excel():
    path_excel = r'..\res\Config.xlsx'
    workbooks = xlrd.open_workbook(path_excel)
    sheet = workbooks.sheet_by_index(0)
    rows = sheet.nrows
    keys = sheet.row_values(0)
    # print(keys)
    submit = {}
    submit['Index'] = -1
    submits = []
    for i in range(2):    
        if i == 0:
            continue
    # for i in range(rows):
        values = sheet.row_values(i)
        # submit = dict(zip(keys,values))
        # submit['Index'] = i
        # submits.append(submit)

    a = type(1)
    b = type('1')
    for i in range(len(values)):
        if type(values[i]) != b:
            values[i] = int(values[i])
    print(keys)
    print(values)            
    return keys,values
    if len(submit) == 1:
        return submit
    if submit['Zip'] == '':
        return submit
    submit['Home_phone'] = str(int(submit['Home_phone'])).replace('-','')
    submit['Zip'] = str(int(submit['Zip']))
    if len(submit['Zip']) == 4:
        submit['Zip'] = '0' + submit['Zip']
    submit['Height_FT'] = str(random.randint(4,7))
    submit['Height_Inch'] = '0'+str(random.randint(7,9))
    submit['Weight'] = str(int(random.randint(100,300)))
    if submit['Date_of_birth'] != '':
        date = xldate_as_tuple(submit['Date_of_birth'],0)
        # print(date)
    else:
        date = [str(random.randint(1960,1980))] 
    for item in date:
        if len(str(item)) == 2:
            if int(item) >= 50:
                submit['Year'] = '19' + str(item)    
        if len(str(item)) == 4:
            submit['Year'] = str(item)
    submit['Month'] = str(random.randint(1,12))
    submit['Day'] = str(random.randint(1,25))            
    return submit



if __name__ == '__main__':
    keys,values = read_excel()
    Get_conf.add_key('BasicInfo',keys,values)
