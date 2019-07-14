import pymysql
import sys
sys.path.append("..")
import json
import xlrd
from xlutils.copy import copy
from xlrd import xldate_as_tuple
import uuid


'''
4 accounts for 4 members.
same tables.different db name

requirements:
1.read info from table
    1.1 read Basicinfo table union select from Mission
    1.2 read Email table union select from Mission

2.update info into table 

3.write log into Mission table

4.delete info from table

'''



def write_json_test(file,content):
    content = json.dumps(content) 
    with open(file,'w') as f:
        # content += '\n'
        f.write(content)

def get_account():
    file = r'..\res\db_config.txt' 
    submits = []
    with open(file,'r') as f:
        jss = f.readlines()
        print(jss)
        for js in jss:
            submit = json.loads(js)
            submits.append(submit)
            # print(submit)
    return submits[-1]

def read_excel(i,file_flag=0):
    if file_flag == 0:
        path_excel = r'..\res\Config.xlsx'
    else:
        path_excel = r'..\res\Email.xlsx'
    workbooks = xlrd.open_workbook(path_excel)
    sheet = workbooks.sheet_by_index(0)
    rows = sheet.nrows
    keys = sheet.row_values(0)
    values = sheet.row_values(i)
    a = type(1)
    b = type('1')
    for i in range(len(values)):
        if type(values[i]) != b:
            values[i] = int(values[i])
        else:
            if '"' in values[i]:
                values[i] = values[i].replace('"','')
    print(keys)
    print(values) 
    keys.insert(0,'Uuid')   
    uuid_sin = str(uuid.uuid1())    
    print(uuid_sin)  
    print(type(uuid_sin))
    print('=============')  
    values.insert(0,uuid_sin)
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


def login_sql(account):
    conn = pymysql.connect(host= account['IP'],port=3306,user=account['username'],passwd=str(account['pwd']))
    cursor = conn.cursor()
    Create_db='CREATE DATABASE IF NOT EXISTS EMU'
    cursor.execute(Create_db)    
    cursor.execute('use %s;'%account['db_name'])
    print('Login db success.')
    # res = cursor.execute('select * from TOKENTABLE;')
    return conn,cursor

def login_out_sql(conn,cursor):
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

def create_tokentable():
    conn,cursor = login_sql()
    res = cursor.execute('CREATE TABLE  IF NOT EXISTS Email (id INT(30),token VARCHAR(100));')
    res = cursor.fetchall()
    for item in res:
        print(item)    
    login_out_sql(conn,cursor)    

def create_BasicInfo(account,keys,values):
    conn,cursor = login_sql(account)
    a = type(1)
    b = type('1')
    res = cursor.execute('CREATE TABLE  IF NOT EXISTS BasicInfo (Uuid VARCHAR(50) PRIMARY KEY NOT NULL)')
    # res.fetchall()
    print(res)
    for i in range(len(keys)):
        if type(values[i]) == b:
            content = 'ALTER table BasicInfo ADD %s varchar(50)'%keys[i]
        else :
            content = 'ALTER table BasicInfo ADD %s int(30)'%keys[i]
        print(content)
        res = cursor.execute(content)
    # return
        # res = cursor.execute(content)
    
    # for item in res:
    #     print(item)    
    login_out_sql(conn,cursor)        

def create_Email(account):
    conn,cursor = login_sql(account)
    res = cursor.execute("CREATE TABLE  IF NOT EXISTS Email (Uuid VARCHAR(50) PRIMARY KEY NOT NULL,Email_emu VARCHAR(50) NOT NULL,Email_emu_pwd VARCHAR(50) NOT NULL,Email_assist VARCHAR(50) NULL,Email_assist_pwd VARCHAR(50) NULL)")
    # res = cursor.fetchall()
    # for item in res:
    #     print(item)    
    login_out_sql(conn,cursor)

def create_Mission(account):
    conn,cursor = login_sql(account)
    res = cursor.execute("CREATE TABLE  IF NOT EXISTS Mission (Id INT PRIMARY KEY AUTO_INCREMENT,Mission_Id INT(10) NOT NULL,TABLE_Id INT(10) NOT NULL,Uuid VARCHAR(50) NOT NULL)")
    # res = cursor.fetchall()
    # for item in res:
    #     print(item)    
    login_out_sql(conn,cursor)

def create_all_tables():
    account = get_account()
    create_Email(account)
    create_Mission(account)
    keys,values = read_excel(1)
    create_BasicInfo(account,keys,values)    

def read_one_info(table):
    res = cursor.execute('SELECT one from %s WHERE;'%s)
    res = cursor.fetchall()

def upload_data(table,keys,values):
    account = get_account()
    a = 'INSERT INTO '+table+' ('
    for key in keys:
        a+= key + ','
    # print(a)
    a = a[0:-1] +') VALUES('
    # print(a)
    type_str = type('1')
    type_int = type(1)    
    # for value in values:
    #     if type(value) == type_str:
    for i in range(len(values)):
        if type(values[i]) == type_str:
            a+='"{}",'
        else:
            a+='{},'
    a = a[0:-1] + ');'
    # print(a)
    # print(len(values))
    # print(a.format(*values))
    sql_content = a.format(*values)
    print(sql_content)
    conn,cursor = login_sql(account)
    res = cursor.execute(sql_content)
    login_out_sql(conn,cursor)  



if __name__ == '__main__':
    # create_all_tables()
    paras=sys.argv
    paras = [1,2]
    i = int(paras[0])
    if i == 1:
        keys,values = read_excel(1)
        print(type(values))
        upload_data('Basicinfo',keys,values)
    elif i == 2:
        keys,values = read_excel(1,1)
        print(type(values))
        upload_data('Email',keys,values)        
    # print(uuid.uuid1())
