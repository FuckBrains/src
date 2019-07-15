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
        # print(jss)
        for js in jss:
            submit = json.loads(js)
            submits.append(submit)
            # print(submit)
    return submits[-1]

def get_sheet(file_flag):
    if file_flag == 1:
        path_excel = r'..\res\Config.xlsx'
    else:
        path_excel = r'..\res\Email.xlsx'
    workbooks = xlrd.open_workbook(path_excel)
    sheet = workbooks.sheet_by_index(0)
    return sheet  

def get_data(keys,values,create):
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
    if create != True: 
        uuid_sin = str(uuid.uuid1())     
        values.insert(0,uuid_sin)  
    return values  

def read_excel(i,file_flag=1,create=True):
    sheet = get_sheet(file_flag)
    keys = sheet.row_values(0)
    values = sheet.row_values(i)
    values = get_data(keys,values,create)
    return keys,values

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
    res = cursor.execute('CREATE TABLE  IF NOT EXISTS BasicInfo (BasicInfo_Id VARCHAR(50) PRIMARY KEY NOT NULL)')
    for i in range(len(keys)):
        if keys[i] == 'Ua':
            content = 'ALTER table BasicInfo ADD %s varchar(500)'%str(keys[i])
        elif keys[i] == 'Address':
            content = 'ALTER table BasicInfo ADD %s varchar(500) UNIQUE'%str(keys[i])            
        elif keys[i] == 'Country':
            content = 'ALTER table BasicInfo ADD %s varchar(50) NOT NULL'%str(keys[i])                
        else:
            content = 'ALTER table BasicInfo ADD %s varchar(100)'%str(keys[i])
        res = cursor.execute(content)   
    login_out_sql(conn,cursor)        

def create_Email(account):
    conn,cursor = login_sql(account)
    res = cursor.execute("CREATE TABLE  IF NOT EXISTS Email (Email_Id VARCHAR(50) PRIMARY KEY NOT NULL,Email_emu VARCHAR(50) UNIQUE NOT NULL,Email_emu_pwd VARCHAR(50) NOT NULL,Email_assist VARCHAR(50) NULL,Email_assist_pwd VARCHAR(50) NULL,Status VARCHAR(20) NULL)")
    # res = cursor.fetchall()
    # for item in res:
    #     print(item)    
    login_out_sql(conn,cursor)

def create_Mission(account):
    conn,cursor = login_sql(account)
    res = cursor.execute("CREATE TABLE  IF NOT EXISTS Mission (Mission_Id INT(10) NOT NULL,Email_Id VARCHAR(50),BasicInfo_Id VARCHAR(50),Cookie VARCHAR(1000))")
    # Mission_Id INT PRIMARY KEY AUTO_INCREMENT,
    login_out_sql(conn,cursor)

def create_all_tables():
    account = get_account()
    create_Email(account)
    create_Mission(account)
    keys,values = read_excel(1)
    create_BasicInfo(account,keys,values)    

def upload_data(i):
    tables = ['BasicInfo','Email']
    table = tables[i-1]
    sheet = get_sheet(i)    
    keys = sheet.row_values(0)
    if i == 1:
        keys.insert(0,'BasicInfo_Id') 
    else:
        keys.insert(0,'Email_Id') 
    rows = sheet.nrows
    account = get_account() 
    conn,cursor = login_sql(account)
    for j in range(rows):
        if j == 0:
            continue
        values = sheet.row_values(j) 
        values = get_data(keys,values,False)
        sql_content = get_upload_sql_content(table,keys,values) 
        print(table,'Uploading data of row',j) 
        print(sql_content)
        res = cursor.execute(sql_content)
        print(res)
        if res == 0:
            print('duplicated data')
        else:
            print('Upload finished') 
    login_out_sql(conn,cursor)

def get_upload_sql_content(table,keys,values):
    a = 'INSERT IGNORE INTO  '+table+' ('
    for key in keys:
        a+= key + ','
    a = a[0:-1] +') VALUES('
    type_str = type('1')
    type_int = type(1)    
    for i in range(len(values)):
        if type(values[i]) == type_str:
            a+='"{}",'
        else:
            a+='{},'
    a = a[0:-1] + ');'
    sql_content = a.format(*values)
    return sql_content    

def read_one_info(Country,Mission_list,Email_list):
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from BasicInfo')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    BasicInfo_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    res = cursor.execute('SELECT * from Mission')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    res = cursor.execute('SELECT * from Email')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    Info_dict = {}
    for i in range(len(BasicInfo_dict)):
        if BasicInfo_dict[i]['Country'] != Country:
            continue
        flag = 0
        for j in range(len(Mission_dict)):
            if Mission_dict[j]['Mission_Id'] in Mission_list: 
                if BasicInfo_dict[i]['BasicInfo_Id'] == Mission_dict[j]['BasicInfo_Id']:
                    flag = 1
                    break
        if flag == 0:
            Info_dict = BasicInfo_dict[i]
            break
    Info_dict2 = {}
    for i in range(len(Email_dict)):
        if Email_dict[i]['Status'] == 'Bad':
            continue
        a = Email_dict[i]['Email_emu'].find('@')
        end = Email_dict[i]['Email_emu'][a+1:]
        # print(Email_dict[i]['Email_emu'])
        # print(end)
        if end not in Email_list:
            continue 
        flag = 0
        for j in range(len(Mission_dict)):
            if Mission_dict[j]['Mission_Id'] in Mission_list: 
                if Email_dict[i]['Email_Id'] == Mission_dict[j]['Email_Id']:
                    flag = 1
                    break
        if flag == 0:
            Info_dict2 = Email_dict[i]
            break
    login_out_sql(conn,cursor)
    submit = dict(Info_dict,**Info_dict2)
    return submit

def write_one_info(Mission_list,submit):
    try:
        Email_Id = submit['Email_Id']
    except:
        Email_Id = ''
    try:
        BasicInfo_Id = submit['BasicInfo_Id']
    except:
        BasicInfo_Id = ''
    Cookie = ''
    account = get_account()
    conn,cursor=login_sql(account)    
    for Mission_Id in Mission_list:
        sql_content = 'INSERT INTO Mission(Mission_Id,Email_Id,BasicInfo_Id,Cookie)VALUES("%d","%s","%s","%s")'%(Mission_Id,Email_Id,BasicInfo_Id,Cookie)
        res = cursor.execute(sql_content)    
    login_out_sql(conn,cursor)


def updata_email_status(Email_Id,flag = 1):
    if flag == 1:
        status = 'Good'
    else:
        status = 'Bad'
    account = get_account()
    conn,cursor=login_sql(account)    
    sql_content = 'UPDATE Email SET Status = "%s" WHERE Email_Id = "%s"'%(status,Email_Id)
    res = cursor.execute(sql_content)    
    login_out_sql(conn,cursor)


def test():
    ua = 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 6.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)'
    print(len(ua))

if __name__ == '__main__':
    paras=sys.argv
    paras = [0,1,2]
    i = int(paras[2])
    if i == 0:
        create_all_tables()
    else:
        upload_data(i)
    # updata_email_status('99ad0eef-a6ed-11e9-904f-00233a633931',1)