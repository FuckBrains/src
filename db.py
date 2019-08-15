import pymysql
import sys
sys.path.append("..")
import json
import xlrd
from xlutils.copy import copy
from xlrd import xldate_as_tuple
import uuid
import random
import os


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


def get_excel_path():
    path = os.getcwd()
    # print(path)
    path = r'..\res'
    files = os.listdir(path)
    # print(files)
    excels_path = [os.path.join(path,file) for file in files if 'xlsx' in file and 'Email' not in file]
    return excels_path    


def get_excel_names():
    '''
    get excel names from file folder:res,except Email.xlsx
    eg: Auto,Uslife...
    requires nothing
    return a list of the names of these excel files
    '''
    excels_path = get_excel_path()
    # print(excels_path)
    # print(len(excels_path))
    ex_names = [((os.path.split(file))[1].split('.'))[0] for file in excels_path]    
    return ex_names

def check_keys():
    '''
    get keys set dict from excels of file folder res,except Email.xlsx
        adding key of Excel_name
    eg:Keys_all = {'Excel_name':class<str>,'firstname':class<str>,'lastname':class<str>,...}  ps:lower keys
    requires nothing
    return a dict of the unique lower keys from all the excels,and values of the type of the keys
    '''
    ex_names = get_excel_names()
    excels_path = get_excel_path()
    print(ex_names)
    Keys_all = {}
    # type_all = []
    for excel in excels_path:
        keys,values = read_excel_new(excel)
        values_type = [type('1') for value in values]
        # types = set(values_type)
        # for type_ in types:
        #     if type_ not in type_all:
        #         type_all.append(type_)
        keys_dict=dict(zip(keys,values_type))
        Keys_all = dict(Keys_all,**keys_dict)
    Keys_all['Excel_name'] = type('1')
    return Keys_all

def read_excel_new(path_excel):
    '''
    get lower keys and values from the excel given,also fix the ' ' of the keys,like 'first name'
    eg; keys = ['firstname','lastname',...]
    requies given excel path(relevent path or abs path)
    return keys, and values of the second row which changed all non str type into str type
    '''
    workbooks = xlrd.open_workbook(path_excel)
    sheet = workbooks.sheet_by_index(0)
    rows = sheet.nrows
    keys = sheet.row_values(0)
    keys = [key.lower().replace(' ','') for key in keys]
    for i in range(2):    
        if i == 0:
            continue
        values = sheet.row_values(i)
    # a = type(1)
    # b = type('1')
    # for i in range(len(values)):
    #     if type(values[i]) != b:
    #         values[i] = str(values[i])
    return keys,values

def write_json_test(file,content):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    content = json.dumps(content) 
    with open(file,'w') as f:
        # content += '\n'
        f.write(content)

def get_account():
    '''
    get account for sql db,read a config file in res folder
    eg:submit = {'password':...}
    requies nothing
    return the sql db account
    '''
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

def get_sheet(path_excel):
    '''
    get sheet from given path :path_excel
    requies excel file with path
    return sheet
    '''
    workbooks = xlrd.open_workbook(path_excel)
    sheet = workbooks.sheet_by_index(0)
    return sheet  

def get_data(values,create):
    '''
    change values into str type.
    if create is not True,insert uuid into values on the first place
    '''
    a = type(1)
    b = type('1')
    for i in range(len(values)):
        if type(values[i]) != b:
            values[i] = str(values[i])
        else:
            if '"' in values[i]:
                values[i] = values[i].replace('"','')
    if create != True: 
        uuid_sin = str(uuid.uuid1())     
        values.insert(0,uuid_sin)  
    return values  

def login_sql(account,create = False):
    '''
    Login sql and create EMU db if not exist
    choose emu db
    return the cursor and conn
    '''
    conn = pymysql.connect(host= account['IP'],port=3306,user=account['username'],passwd=str(account['pwd']))
    cursor = conn.cursor()
    try:
        cursor.execute('use %s;'%account['db_name'])
    except:
        pass
    print('Login db success.')
    # res = cursor.execute('select * from TOKENTABLE;')
    return conn,cursor


def create_db():
    Create_db='CREATE DATABASE IF NOT EXISTS EMU;'
    Execute_sql([Create_db])


def login_out_sql(conn,cursor):
    '''
    commit and close connection
    '''
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    print('exit sql server success')

'''
get sql contet for 
1.create table together
2.create tokentable
3.create basicinfo table
'''

def create_tokentable(account):
    sql_content = 'CREATE TABLE  IF NOT EXISTS Tokens (id BIGINT(20),token VARCHAR(100));'
    Execute_sql(sql_content)

def create_BasicInfo(keys):
    account = get_account()
    conn,cursor = login_sql(account)
    res = cursor.execute('CREATE TABLE  IF NOT EXISTS BasicInfo (BasicInfo_Id VARCHAR(50) PRIMARY KEY NOT NULL)')
    type_str = type('1')
    for item in keys:
        if item == 'ua':
            content = 'ALTER table  BasicInfo ADD %s varchar(500)'%str(item)
        elif item == 'address':
            content = 'ALTER table  BasicInfo ADD %s varchar(500) UNIQUE'%str(item)            
        elif item == 'country':
            content = 'ALTER table BasicInfo ADD %s varchar(50) NOT NULL'%str(item)                
        elif item == 'state':
            content = 'ALTER table BasicInfo ADD %s varchar(50) NOT NULL'%str(item)                            
        else:
            content = 'ALTER table  BasicInfo ADD %s varchar(100)'%str(item)
        print(content)  
        try:            
            res = cursor.execute(content)   
        except:
            pass
    login_out_sql(conn,cursor)        

def create_all_tables():
    create_db()
    sql_contents = []
    sql_email = "CREATE TABLE  IF NOT EXISTS Email (Email_Id VARCHAR(50) PRIMARY KEY NOT NULL,Email_emu VARCHAR(50) UNIQUE NOT NULL,Email_emu_pwd VARCHAR(50) NOT NULL,Email_assist VARCHAR(50) NULL,Email_assist_pwd VARCHAR(50) NULL,Status VARCHAR(20) NULL);"
    sql_mission = "CREATE TABLE  IF NOT EXISTS Mission (Mission_Id INT(10) NOT NULL,Email_Id VARCHAR(50),BasicInfo_Id VARCHAR(50),Cookie VARCHAR(1000));"
    sql_ip = "CREATE TABLE  IF NOT EXISTS Ip_Pools (Ip VARCHAR(50) UNIQUE NOT NULL,Type VARCHAR(20) NOT NULL,Status VARCHAR(20) NULL);"
    sql_contents = [sql_email,sql_mission,sql_ip]
    Execute_sql(sql_contents)
    keys = check_keys()
    create_BasicInfo(keys)  




'''
Upload data together for all the excels in file folder res
'''
def unique_index(L,e):
    '''
    find all the Duplicated poses of e in list L
    return a poses list
    '''
    return [i for (i,j) in enumerate(L) if j == e]

def upload_data():
    '''
    deal with the Duplicated keys
    Upload all the excel datas in file folder res
    '''
    account = get_account()
    path = os.getcwd()
    path = r'..\res'
    files = os.listdir(path)
    excels_path = [os.path.join(path,file) for file in files if 'xlsx' in file]
    conn,cursor = login_sql(account)
    for path_excel in excels_path:
        # print(path_excel)
        Excel_name = ((os.path.split(path_excel))[1].split('.'))[0]
        # print(Excel_name)
        sheet = get_sheet(path_excel)    
        keys = sheet.row_values(0)
        keys = [key.lower().replace(' ','') for key in keys] 
        # print(keys)
        rids = []
        # print('================')
        # print(keys)
        for key in set(keys):
            pos = unique_index(keys,key)
            # print(pos)       
            if len(pos) >= 2:
                print('Duplicated keys,in Excel:',path_excel,key)
                rids = pos[1:]
                rids.reverse()
        # print(keys)
        # print('---------------')
        if 'Email' not in path_excel:
            keys.insert(0,'BasicInfo_Id') 
            keys.insert(1,'Excel_name')            
            table = 'BasicInfo'
        else:
            keys.insert(0,'Email_Id') 
            table = 'Email'
        rows = sheet.nrows
        account = get_account() 
        if len(rids) >= 1:
            for rid in rids:
                if 'Email' not in path_excel:
                    keys.pop(rid+2)        
                else:
                    keys.pop(rid+1)
        for j in range(rows):
            if j == 0:
                continue
            values = sheet.row_values(j) 
            values = get_data(values,False)
            if 'BasicInfo_Id' in keys:
                values.insert(1,Excel_name)
            if len(rids) >= 1:
                for rid in rids:
                    values.pop(rid+1)
            sql_content = get_upload_sql_content(table,keys,values) 
            print(Excel_name,'Uploading data of row',j) 
            print(sql_content)
            res = cursor.execute(sql_content)
            conn.commit()
            # print(res)
            if res == 0:
                print('duplicated data')
            else:
                print('Upload finished') 
    login_out_sql(conn,cursor)


'''
read all infos in listed excel of Excel_names,and the email info into one big dict
eg: submit = {
    'Auto':{'firstname':'lee',...},
    'Uspd':{'firstname':'song',...}
    ...
    'Email':{'Email_Id':'asd123asd-asd123-asd123-asd12','Email_emu':'asd123@hotmail.com'}
}
conditions:
1.selected country
2.uuid not in Mission table
3.email should be in email_list

return submit with same state in every excel
'''

def read_one_info(Country,Mission_list,Email_list,Excel_names):
    print('     Start reading info from sql server...')
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
    while True:
        Info_dicts = {}
        Excel_names_check = []
        list_BasicInfo = random.sample(range(len(BasicInfo_dict)),len(BasicInfo_dict))
        for i in list_BasicInfo:
            if BasicInfo_dict[i]['country'] != Country:
                continue
            if BasicInfo_dict[i]['Excel_name'] in Excel_names_check:
                continue 
            if BasicInfo_dict[i]['Excel_name'] not in Excel_names:
                continue             
            if len(Excel_names_check) > 0:
                if BasicInfo_dict[i]['state'] != Info_dicts[Excel_names_check[0]]['state']:
                    # if BasicInfo_dict[i]['state1'] != Info_dicts[Excel_names_check[0]]['state']:
                    continue
            flag = 0
            '''
            BasicInfo_dict[i]['BasicInfo_Id'] should not in table Mission
            '''
            for j in range(len(Mission_dict)):
                if Mission_dict[j]['Mission_Id'] in Mission_list: 
                    if BasicInfo_dict[i]['BasicInfo_Id'] == Mission_dict[j]['BasicInfo_Id']:
                        flag = 1
                        break
            if flag == 0:
                Info_dicts[BasicInfo_dict[i]['Excel_name']] = BasicInfo_dict[i]
                Excel_names_check.append(BasicInfo_dict[i]['Excel_name'])
            if len(Excel_names_check) == len(Excel_names):
                break
        print(Excel_names_check)
        if len(Excel_names_check) == len(Excel_names):
            break
    Info_dict2 = {}
    list_Email = random.sample(range(len(Email_dict)),len(Email_dict))
    for i in list_Email:
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
    Info_dicts['Email'] = Info_dict2
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    return Info_dicts

'''
return dict with selected excel 
'''
def read_one_excel(Mission_list,Excel_name,Email_list):
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    if Excel_name[0] != '' : 
        res = cursor.execute('SELECT * from BasicInfo WHERE Excel_name = "%s"'%Excel_name[0])
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        BasicInfo_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    else:
        BasicInfo_dict = {}
    res = cursor.execute('SELECT * from Mission')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    if Excel_name[1] != '':
        res = cursor.execute('SELECT * from Email')
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    else:
        # Excel_name[1] = {}
        Email_dict = {}
    Info_dicts = {}
    if len(BasicInfo_dict) != 0:
        list_BasicInfo = random.sample(range(len(BasicInfo_dict)),len(BasicInfo_dict))
        for i in list_BasicInfo:
            flag = 0
            '''
            BasicInfo_dict[i]['BasicInfo_Id'] should not in table Mission
            '''
            for j in range(len(Mission_dict)):
                if Mission_dict[j]['Mission_Id'] in Mission_list: 
                    if BasicInfo_dict[i]['BasicInfo_Id'] == Mission_dict[j]['BasicInfo_Id']:
                        flag = 1
                        break
            if flag == 0:
                Info_dicts[BasicInfo_dict[i]['Excel_name']] = BasicInfo_dict[i]
                break
    Info_dict2 = {}
    if len(Email_dict) != 0:
        list_Email = random.sample(range(len(Email_dict)),len(Email_dict))
        for i in list_Email:
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
    if len(Info_dict2) != 0:
        Info_dicts['Email'] = Info_dict2
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    return Info_dicts

def write_one_info(Mission_list,submit,Cookie = ''):
    try:
        Email_Id = submit['Email']['Email_Id']
    except:
        Email_Id = '' 
    account = get_account()
    conn,cursor=login_sql(account)  
    for item in submit:  
        if item == 'Email':
            continue    
        for Mission_Id in Mission_list:
            sql_content = 'INSERT INTO Mission(Mission_Id,Email_Id,BasicInfo_Id,Cookie)VALUES("%s","%s","%s","%s")'%(Mission_Id,Email_Id,submit[item]['BasicInfo_Id'],Cookie)
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

def update_ip_pools(values):
    # values=[proxy,'Socket5','Good']
    table = 'Ip_Pools'
    keys = ['Ip','Type','Status']
    sql_content = get_upload_sql_content(table,keys,values)
    print(sql_content)
    sql_contents = []
    sql_contents.append(sql_content)
    Execute_sql(sql_contents)

def get_create_table_sql_content(table,keys):
    sql_content = "CREATE TABLE  IF NOT EXISTS" + table + " ("
    for key in keys:
        sql_content += key
    sql_content += " );"
    return sql_content

def get_upload_sql_content(table,keys=None,values=None):
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

def Execute_sql(sql_contents):
    account = get_account()
    conn,cursor = login_sql(account)
    for sql_content in sql_contents:
        print(sql_content)
        res = cursor.execute(sql_content)
    login_out_sql(conn,cursor)     

def get_one_info():
    Country ='US'
    Mission_list = ['10004']
    Email_list = ['hotmail','aol.com','yahoo.com','outlook.com']
    Excel_names = ['Auto','Uspd']
    submit = read_one_info(Country,Mission_list,Email_list,Excel_names)
    submit['Email']
    print(submit)
    print(len(submit))
    return submit

def init():
    create_all_tables()
    upload_data()    

def read_rest(Mission_list,Excel_name,Email_list):
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    if Excel_name[0] != '' : 
        res = cursor.execute('SELECT * from BasicInfo WHERE Excel_name = "%s"'%Excel_name[0])
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        BasicInfo_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    else:
        BasicInfo_dict = {}
    res = cursor.execute('SELECT * from Mission')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    if Excel_name[1] != '':
        res = cursor.execute('SELECT * from Email')
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    else:
        # Excel_name[1] = {}
        Email_dict = {}
    Info_dicts = [0,0]
    if len(BasicInfo_dict) != 0:
        list_BasicInfo = random.sample(range(len(BasicInfo_dict)),len(BasicInfo_dict))
        for i in list_BasicInfo:
            flag = 0
            '''
            BasicInfo_dict[i]['BasicInfo_Id'] should not in table Mission
            '''
            for j in range(len(Mission_dict)):
                if str(Mission_dict[j]['Mission_Id']) in Mission_list: 
                    if BasicInfo_dict[i]['BasicInfo_Id'] == Mission_dict[j]['BasicInfo_Id']:
                        flag = 1
                        print(BasicInfo_dict[i]['BasicInfo_Id'])
                        break
            if flag == 0:
                Info_dicts[0] += 1
    # Info_dict2 = {}
    if len(Email_dict) != 0:
        list_Email = random.sample(range(len(Email_dict)),len(Email_dict))
        for i in list_Email:
            # if Email_dict[i]['Status'] == 'Bad':
            #     continue
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
                Info_dicts[1] += 1
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    return Info_dicts

def test_rest():
    Mission_list = [10000]
    Excel_name = ['Auto','Email']
    Email_list = ['hotmail.com','aol.com','outlook.com','yahoo.com']
    rest = read_rest(Mission_list,Excel_name,Email_list)
    print(rest)

if __name__ == '__main__':
    test_rest()
    # init()
