import xlrd
from xlutils.copy import copy
from xlrd import xldate_as_tuple
import Get_conf
import os
import sys
sys.path.append("..")
import db




def read_excel(path_excel):
    workbooks = xlrd.open_workbook(path_excel)
    sheet = workbooks.sheet_by_index(0)
    rows = sheet.nrows
    keys = sheet.row_values(0)
    for i in range(2):    
        if i == 0:
            continue
        values = sheet.row_values(i)
    a = type(1)
    b = type('1')
    for i in range(len(values)):
        if type(values[i]) != b:
            values[i] = int(values[i])
    return keys,values

def read_data(path_excel):
    # list1 = [BasicInfo_Id,country,homephone,firstname,lastname,address,city,state,zip,email,dateofbirth,leadtype,coveragetype,relationshiptoapplicant,education,student,gender,maritalstatus,occupation,usresidence,height_ft,height_inch,weight,deniedcoverage,currentlyinsured,relativeheartdisease,relativecancer,medicaltreatment,hospitalized,pregnant,smoker,alcoholabstain,dui,ipaddress,preexistingconditions]
    pass


def test_read_data():
    Mission = [10001,10002]
    Email_list = ['hotmail.com','outlook.com'] 
    Excel_names = ['Auto','Usload','Uslife','Uspd','Ukpd','Ushealth','Uklife']
    submit=db.read_one_info('UK',Mission,Email_list,Excel_names)
    print(len(submit))
    # print(submit)
    for item in submit:
        print(item,len(submit[item]))



if __name__ == '__main__':
    # keys,values = read_excel()
    # Get_conf.add_key('BasicInfo',keys,values)
    test_read_data()