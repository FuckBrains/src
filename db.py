import Dadao
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
import Chrome_driver
from wrapt_timeout_decorator import *


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

def get_account(ali = 0):
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
    submit = submits[-1]
    if ali == 1:
        submit['IP'] = 'rm-bp100p7672g0g8z9kjo.mysql.rds.aliyuncs.com'
        submit["username"] = "emu3man_win"
        submit["pwd"] = "sAz6x4SD8dF1"
    return submit

def get_sheet(path_excel):
    '''
    get sheet from given path :path_excel
    requies excel file with path
    return sheet
    '''
    workbooks = xlrd.open_workbook(path_excel)
    sheet = workbooks.sheet_by_index(0)
    return sheet  

def get_data(values,create,ids):
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
            values[i] = pymysql.escape_string(values[i])
            # if '"' in values[i]:
                # values[i] = values[i].replace('"','')
    if create != True: 
        for i in range(10000):
            uuid_sin = str(uuid.uuid1())     
            if uuid_sin in ids:
                pass
            else:
                ids.append(uuid_sin)
                break
        values.insert(0,uuid_sin)  
    return values,ids  

def login_sql(account,create = False):
    '''
    Login sql and create EMU db if not exist
    choose emu db
    return the cursor and conn
    '''
    ip = 'rm-bp100p7672g0g8z9kjo.mysql.rds.aliyuncs.com'
    conn = pymysql.connect(host= account['IP'],port=3306,user=account['username'],passwd=str(account['pwd']),charset='utf8mb4',use_unicode=True)
    cursor = conn.cursor()
    try:
        cursor.execute('use %s;'%account['db_name'])
    except:
        pass
    # print('Login db success.')
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
    # print('exit sql server success')

'''
get sql contet for 
1.create table together
2.create tokentable
3.create basicinfo table
'''

def create_tokentable():
    sql_content = 'CREATE TABLE  IF NOT EXISTS Tokens (id BIGINT(20),token VARCHAR(100));'
    Execute_sql(sql_content)

def create_PageFlag_table():
    sql_content = 'CREATE TABLE  IF NOT EXISTS Page_Flag (Mission_Id INT(10) NOT NULL,Page VARCHAR(50) NOT NULL,Flag_xpath VARCHAR(1000) NOT NULL,Flag_text VARCHAR(1000) NOT NULL));'
    Execute_sql(sql_content)

def upload_pageflag(Mission_Id,flag):
    Page = flag['Page']
    Flag_xpath = flag['Flag_xpath'] 
    Flag_text = flag['Flag_text']
    if flag['Quotes'] == 'True':
        Flag_text = 'bbb==='+Flag_text
    Flag_iframe = flag['Iframe']    
    Status = flag['Status']
    Country = flag['Country']
    Pic = 0
    # flag_check = check_flag(Mission_Id,flag)
    # if flag_check == False:
    #     return -1    
    # sql_content = (int(Mission_Id),Page,pymysql.escape_string(Flag_xpath),pymysql.escape_string(Flag_text))      
    sql_content = 'INSERT INTO Page_Flag(Mission_Id,Country,Page,Flag_xpath,Flag_text,Iframe,Status,Pic)VALUES("%d","%s","%s","%s","%s","%s","%s","%d")'%(int(Mission_Id),Country,Page,pymysql.escape_string(Flag_xpath),pymysql.escape_string(Flag_text),pymysql.escape_string(Flag_iframe),Status,Pic)     
    # sql_content = 'INSERT IGNORE INTO Page_Flag(Mission_Id,Page,Flag_xpath,Flag_text)VALUES("%d","%s","%s","%s")'%(Mission_Id, Page,Flag_xpath,Flag_text)
    Execute_sql([sql_content])

def check_flag(Mission_Id,flag):
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from Page_Flag WHERE Mission_Id = "%d" and Flag_text = "%s"'%(int(Mission_Id),str(flag['Flag_text'])))
    print(res)
    # desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    # Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    if res == 0:
        flag = True
    else:
        flag = False
    print(flag)
    return flag


def get_employer():
    account = get_account()
    conn,cursor=login_sql(account)
    cursor.execute('SELECT employer from Basicinfo WHERE Excel_name = "Us_pd_native"')
    res = cursor.fetchall()
    employer = [key[0] for key in res]
    # desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    # Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    num = random.randint(0,len(employer)-10)
    employer = employer[num]
    return employer

def get_occupation():
    account = get_account()
    conn,cursor=login_sql(account)
    cursor.execute('SELECT occupation from Basicinfo WHERE Excel_name = "Us_pd_native"')
    res = cursor.fetchall()
    occupation = [key[0] for key in res]
    # desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    # Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    num = random.randint(0,len(occupation)-10)
    occupation = occupation[num]
    return occupation



def check_step(Mission_Id,flag):
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from Page_Config WHERE Mission_Id = "%d" and Page = "%s" and Step = "%d"'%(int(Mission_Id),str(flag['Page']),int(flag['Step'])))
    print(res)
    # desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    # Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    if res == 0:
        flag = True
    else:
        flag = False
    print(flag)
    return flag

def upload_pageconfig(flag):
    Page = flag['Page']
    Step = flag['Step']
    Mission_Id = flag['Mission_Id']
    flag_check = check_step(Mission_Id,flag)
    if flag_check == False:
        return -1
    Action = flag['Action'] 
    General = json.dumps(flag['General'])
    Step_config = json.dumps(flag['Step_config'])  
    print('General',General)
    print('Step_config',Step_config)
    print(flag)  
    # sql_content = (int(Mission_Id),Page,pymysql.escape_string(Flag_xpath),pymysql.escape_string(Flag_text))      
    sql_content = 'INSERT INTO Page_config(Mission_Id,Page,Step,Action,General,Step_config)VALUES("%d","%s","%d","%s","%s","%s")'%(int(Mission_Id),str(Page),int(Step),str(Action),pymysql.escape_string(General),pymysql.escape_string(Step_config))     
    # sql_content = 'INSERT IGNORE INTO Page_Flag(Mission_Id,Page,Flag_xpath,Flag_text)VALUES("%d","%s","%s","%s")'%(Mission_Id, Page,Flag_xpath,Flag_text)
    Execute_sql([sql_content])
    return 1






def update_pageflag(Mission_Id,flag):
    Page = flag['name']
    Flag_xpath = flag['xpath'] 
    Flag_text = flag['text']
    # sql_content = (int(Mission_Id),Page,pymysql.escape_string(Flag_xpath),pymysql.escape_string(Flag_text))      
    sql_content = 'INSERT INTO Page_Flag(Mission_Id,Page,Flag_xpath,Flag_text)VALUES("%d","%s","%s","%s")'%(int(Mission_Id),Page,pymysql.escape_string(Flag_xpath),pymysql.escape_string(Flag_text))     
    # sql_content = 'INSERT IGNORE INTO Page_Flag(Mission_Id,Page,Flag_xpath,Flag_text)VALUES("%d","%s","%s","%s")'%(Mission_Id, Page,Flag_xpath,Flag_text)
    if Flag_xpath != '':
        sql_content = 'UPDATE Page_Flag SET Flag_xpath = "%s" WHERE Mission_Id = "%d" and Page = "%s"' % (Flag_xpath,int(Mission_Id),Page)
    if Flag_text != '':
        sql_content = 'UPDATE Page_Flag SET Flag_text = "%s" WHERE Mission_Id = "%d" and Page = "%s"' % (Flag_text,int(Mission_Id),Page)
    Execute_sql([sql_content])

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
    '''
    login db
    init table email,mission,plans,ip_pools if not exists
    '''
    create_db()
    sql_contents = []
    sql_email = "CREATE TABLE  IF NOT EXISTS Email (Email_Id VARCHAR(50) PRIMARY KEY NOT NULL,Email_emu VARCHAR(50) UNIQUE NOT NULL,Email_emu_pwd VARCHAR(50) NOT NULL,Email_assist VARCHAR(50) NULL,Email_assist_pwd VARCHAR(50) NULL,Status VARCHAR(20) NULL,create_time timestamp DEFAULT CURRENT_TIMESTAMP);"
    sql_mission = "CREATE TABLE  IF NOT EXISTS Mission (Alliance_email VARCHAR(50),Account_email VARCHAR(50),Mission_Id INT(10) NOT NULL,Email_Id VARCHAR(50),BasicInfo_Id VARCHAR(50),Cookie VARCHAR(1000),create_time timestamp DEFAULT CURRENT_TIMESTAMP);"    
    sql_plans = "CREATE TABLE  IF NOT EXISTS Plans (Plan_Id INT(10) NOT NULL,Alliance VARCHAR(50),Account VARCHAR(50),Offer VARCHAR(50),url_link VARCHAR(1000),Country VARCHAR(50),Excel VARCHAR(50),Mission_Id VARCHAR(50),Mission_dir VARCHAR(100),ip_lpm VARCHAR(50),port_lpm VARCHAR(50),create_time timestamp DEFAULT CURRENT_TIMESTAMP);"    
    sql_ip = "CREATE TABLE  IF NOT EXISTS Ip_Pools (Ip VARCHAR(50) UNIQUE NOT NULL,Type VARCHAR(20) NOT NULL,Status VARCHAR(20) NULL,create_time timestamp DEFAULT CURRENT_TIMESTAMP);"
    sql_contents = [sql_email,sql_plans,sql_mission,sql_ip]
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
    # blacklist = ['Dadao']
    excels_path = [os.path.join(path,file) for file in files if 'xlsx' in file and 'Dadao' not in file]
    print(excels_path)
    if len(excels_path) == 0:
        print('No excel to upload')
        return
    conn,cursor = login_sql(account)
    ids = uuid_set()
    for path_excel in excels_path:
        print(path_excel)
        Excel_name = ((os.path.split(path_excel))[1].split('.'))[0]
        print(Excel_name)
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
            values,ids = get_data(values,False,ids)
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


def uuid_set():
    account = get_account()
    conn,cursor=login_sql(account)    
    res = cursor.execute('SELECT Basicinfo_Id from BasicInfo')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    res = cursor.execute('SELECT Basicinfo_Id from Mission')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict2 = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来          
    # print(len(Mission_dict))
    # print(Mission_dict[0:5])
    ids = [item['Basicinfo_Id'] for item in Mission_dict]
    ids = list(set(ids))
    print('Number before set1:',len(ids))    
    ids2 = [item['Basicinfo_Id'] for item in Mission_dict2]
    ids = ids+ids2
    print('Number before set:',len(ids))
    print(ids[:5])
    ids = list(set(ids))
    print('Number after set:',len(ids))
    print(ids[:5])
    login_out_sql(conn,cursor) 

    return ids    

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
        print(i)
        if Email_dict[i]['Status'] == 'Bad':
            continue
        print(Email_dict[i]['Status'])
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

def test111():
    a+1
    


'''
return dict with selected excel 
'''
def read_one_excel_(Mission_list,Excel_name,Email_list):
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    print('     Login success')
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
            for Mission in Mission_list:
                for j in range(len(Mission_dict)):
                    if str(Mission_dict[j]['Mission_Id']) in str(Mission): 
                        if BasicInfo_dict[i]['BasicInfo_Id'] == Mission_dict[j]['BasicInfo_Id']:
                            flag = 1
                            break
                if flag == 1:
                    break
            if flag == 0:
                Info_dicts[BasicInfo_dict[i]['Excel_name']] = BasicInfo_dict[i]
                break
    Info_dict2 = {}
    if len(Email_dict) != 0:
        list_Email = random.sample(range(len(Email_dict)),len(Email_dict))
        print(len(Email_dict))
        for i in list_Email:
            # print(i)
            if Email_dict[i]['Status'] == 'Bad':
                continue
            # if Email_dict[i]['Status'] == 'Good':
            #     continue                
            # print('========',Email_dict[i]['Status'])
            a = Email_dict[i]['Email_emu'].find('@')
            end = Email_dict[i]['Email_emu'][a+1:]
            # print(Email_dict[i]['Email_emu'])
            # print(end)
            if end not in Email_list:
                continue 
            flag = 0
            # print('===============')
            # print(Mission_list)
            # print(Email_dict[i]['Email_Id'])
            for Mission in Mission_list:
                # print('On going search:',Mission)
                for j in range(len(Mission_dict)):
                    # print(Mission_dict[j]['Mission_Id'])
                    # print(Mission)
                    # print(list(str(Mission)))
                    if str(Mission_dict[j]['Mission_Id']) == str(Mission): 
                        # print('---------')
                        if Email_dict[i]['Email_Id'] == Mission_dict[j]['Email_Id']:
                            # print('Duplicated email:',Mission_dict[j]['Email_Id'])
                            # print('22222222222222')
                            flag = 1
                            break
                        else:
                            pass
                            # print(Email_dict[i]['Email_Id'],Mission_dict[j]['Email_Id'])
                if flag == 1:
                    break
            if flag == 0:
                # print('Unique email for all Missions required:',Email_dict[i])
                print('find email unique')
                Info_dict2 = Email_dict[i]
                break
    if len(Info_dict2) != 0:
        Info_dicts['Email'] = Info_dict2
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    return Info_dicts

# def read_one_excel(Mission_list,Excel_name,Email_list):
#     print('     Start reading info from sql server...')
#     account = get_account()
#     conn,cursor=login_sql(account)
#     print('     Login success')    
#     res = cursor.execute('SELECT * from Mission WHERE Mission_Id="%d"'%int(Mission_list[0]))
#     desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
#     Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
#     num = 0
#     step = 100
#     Info_dicts = {}   
#     Mission_basicinfo_list = [Mission['BasicInfo_Id'] for Mission in Mission_dict]
#     Mission_email_list = [Mission['Email_Id'] for Mission in Mission_dict]  
#     sql_content = 'SELECT COUNT(*) FROM Basicinfo WHERE Excel_name="%s"'%Excel_name[0]
#     res = cursor.execute(sql_content)
#     tt = cursor.fetchall()
#     print(tt)
#     num_excel = tt[0][0]
#     # print(num_excel)
#     Basicinfo_ids = []     
#     if Excel_name[0] != '' :
#         while True:
#             # res = cursor.execute('SELECT * from BasicInfo  WHERE Excel_name = "%s" limit 0,1'%(Excel_name[0]))
#             res = cursor.execute('SELECT * from BasicInfo  WHERE Excel_name = "%s" and flag_use = 0 ORDER BY rand() limit 10'%Excel_name[0])
#             # res = cursor.execute('SELECT * from BasicInfo  WHERE Excel_name = "%s" and flag_use = 0 limit %d,%d'%(Excel_name[0],num,step))            
#             print(res)
#             desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
#             BasicInfo_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
#             for info in BasicInfo_dict:
#                 # print('leninfo',len(info))
#                 if info['BasicInfo_Id'] not in Mission_basicinfo_list:
#                     # print(Info_dicts[Excel_name[0]])
#                     # print(BasicInfo_dict)
#                     # print(1)
#                     Info_dicts[Excel_name[0]] = info
#                     break
#                 if info['BasicInfo_Id'] not in Basicinfo_ids:
#                     Basicinfo_ids.append(info['BasicInfo_Id'])

#             sql_content = 'SELECT COUNT(*) FROM Basicinfo WHERE Excel_name="%s" and flag_use = 1'%Excel_name[0]
#             res = cursor.execute(sql_content)
#             ff = cursor.fetchall()
#             # print(ff)
#             num_flag = ff[0][0]     
#             # print(num_flag,'infos flag_use = 1')           
#             if len(Info_dicts) > 0:
#                 break            
#             if len(Basicinfo_ids) >= num_excel-num_flag:
#                 print('No available data for Mission_Id:',str(Mission_list[0]))
#                 return None
#         sql_content = "UPDATE BasicInfo SET flag_use = 1 WHERE BasicInfo_Id = '%s'" % Info_dicts[Excel_name[0]]['BasicInfo_Id']
#         res = cursor.execute(sql_content)                 
#     else:
#         BasicInfo_dict = {}
#     if Excel_name[1] != '':
#         res = cursor.execute('SELECT * from Email')
#         desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
#         Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
#     else:
#         # Excel_name[1] = {}
#         Email_dict = {}            
#     Info_dict2 = {}
#     if len(Email_dict) != 0:
#         list_Email = random.sample(range(len(Email_dict)),len(Email_dict))
#         # print(len(Email_dict))
#         for i in list_Email:
#             # print(i)
#             if Email_dict[i]['Status'] == 'Bad':
#                 continue
#             a = Email_dict[i]['Email_emu'].find('@')
#             end = Email_dict[i]['Email_emu'][a+1:]
#             if end not in Email_list:
#                 continue 
#             flag = 0
#             if Email_dict[i]['Email_Id'] not in Mission_email_list:
#                 # print('find email unique')
#                 Info_dict2 = Email_dict[i]
#                 break
#     if len(Info_dict2) != 0:
#         Info_dicts['Email'] = Info_dict2
#     login_out_sql(conn,cursor)
#     # submit = dict(Info_dict,**Info_dict2)
#     return Info_dicts

def read_one_excel(Mission_list,Excel_name,Email_list):
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    print('     Login success')    
    res = cursor.execute('SELECT * from Mission WHERE Mission_Id="%d"'%int(Mission_list[0]))
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
    # num = 0
    # step = 100
    Info_dicts = {}   
    Mission_basicinfo_list = [str(Mission['BasicInfo_Id']) for Mission in Mission_dict]
    Mission_email_list = [Mission['Email_Id'] for Mission in Mission_dict]  
    print('Total %d emails used in Misision:%d'%(len(Mission_email_list),int(Mission_list[0])))
    sql_content = 'SELECT COUNT(*) FROM Basicinfo WHERE Excel_name="%s"'%Excel_name[0]
    res = cursor.execute(sql_content)
    tt = cursor.fetchall()
    # print(tt)
    num_excel = tt[0][0]
    print('Total',num_excel,'infos in excel',Excel_name[0])
    res = cursor.execute('SELECT * from BasicInfo  WHERE Excel_name = "%s" and flag_use = 0 '%Excel_name[0])
    # print(res)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可    
    BasicInfo_dict_ = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
    flag_test = 0
    if Excel_name[0] != '' :
        BasicInfo_dict_key = random.sample(range(len(BasicInfo_dict_)),len(BasicInfo_dict_))
        for key in BasicInfo_dict_key:
            # print('leninfo',len(info))
            if BasicInfo_dict_[key]['BasicInfo_Id'] not in Mission_basicinfo_list:
                Info_dicts[Excel_name[0]] = BasicInfo_dict_[key]
                flag_test = 1
                break
        if len(Info_dicts) == 0:
            return {}
        # print(Info_dicts)
        print(Info_dicts[Excel_name[0]]['BasicInfo_Id'])
        sql_content = "UPDATE BasicInfo SET flag_use = 1 WHERE BasicInfo_Id = '%s'" % Info_dicts[Excel_name[0]]['BasicInfo_Id']
        res = cursor.execute(sql_content)
    else:
        BasicInfo_dict = {}
    if Excel_name[1] != '':
        res = cursor.execute('SELECT * from Email')
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
        print('Total %d emails good to use'%(len(Email_dict)))
    else:
        # Excel_name[1] = {}
        Email_dict = {}            
    Info_dict2 = {}
    if len(Email_dict) != 0:
        list_Email = random.sample(range(len(Email_dict)),len(Email_dict))
        # print(len(Email_dict))
        for i in list_Email:
            # print(i)
            if Email_dict[i]['Status'] == 'Bad':
                continue
            a = Email_dict[i]['Email_emu'].find('@')
            end = Email_dict[i]['Email_emu'][a+1:]
            if end not in Email_list:
                continue 
            flag = 0
            if Email_dict[i]['Email_Id'] not in Mission_email_list:
                # print('find email unique')
                Info_dict2 = Email_dict[i]
                break
    print('Info_dict2',Info_dict2)
    if len(Info_dict2) != 0:
        Info_dicts['Email'] = Info_dict2
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    return Info_dicts



def read_one_selected_email(Mission_list,Email_list):
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from Mission')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    res = cursor.execute('SELECT * from Email')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    Info_dicts = {}
    Info_dict2 = {}
    if len(Email_dict) != 0:
        list_Email = random.sample(range(len(Email_dict)),len(Email_dict))
        print(len(Email_dict))
        for i in list_Email:
            # print(i)
            if Email_dict[i]['Status'] == 'Bad':
                continue
            # if Email_dict[i]['Status'] == 'Good':
            #     continue                
            print('========',Email_dict[i]['Status'])
            a = Email_dict[i]['Email_emu'].find('@')
            end = Email_dict[i]['Email_emu'][a+1:]
            # print(Email_dict[i]['Email_emu'])
            # print(end)
            if end not in Email_list:
                continue 
            flag = 0
            # print('===============')
            # print(Mission_list)
            # print(Email_dict[i]['Email_Id'])
            for Mission in Mission_list:
                print('On going search:',Mission)
                for j in range(len(Mission_dict)):
                    # print(Mission_dict[j]['Mission_Id'])
                    # print(Mission)
                    # print(list(str(Mission)))
                    if str(Mission_dict[j]['Mission_Id']) == str(Mission): 
                        # print('---------')
                        if Email_dict[i]['Email_Id'] == Mission_dict[j]['Email_Id']:
                            print('Duplicated email:',Mission_dict[j]['Email_Id'])
                            # print('22222222222222')
                            flag = 1
                            break
                        else:
                            pass
                            # print(Email_dict[i]['Email_Id'],Mission_dict[j]['Email_Id'])
                if flag == 1:
                    break
            if flag == 0:
                print('Unique email for all Missions required:',Email_dict[i])
                Info_dict2 = Email_dict[i]
                break
    if len(Info_dict2) != 0:
        Info_dicts['Email'] = Info_dict2
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    return Info_dicts    

def get_all_emails():
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from Email')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    return Email_dict      

def test_count(Excel_name):
    sql_content = 'SELECT COUNT(*) FROM Basicinfo WHERE Excel_name="%s"'%Excel_name
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute(sql_content)
    a = cursor.fetchall()[0]
    print(a)
    # desc = ╒cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    # Email_d╒ict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    return       

def get_unique_soi_email(Mission,Email_list=[]):
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from Mission')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来 
    res = cursor.execute('SELECT * from BasicInfo WHERE Excel_name = "SOI" ')  
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    SOI_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来     
    list_BasicInfo = random.sample(range(len(SOI_dict)),len(SOI_dict))
    flag = 0
    unique_soi = {}
    # unique_soi['SOI'] = {}
    print(len(list_BasicInfo))
    for i in list_BasicInfo:
        for j in range(len(Mission_dict)):
            if str(Mission_dict[j]['Mission_Id']) in str(Mission): 
                if SOI_dict[i]['BasicInfo_Id'] == Mission_dict[j]['BasicInfo_Id']:
                    print('Find used soi info for Mission',str(Mission))
                    flag = 1
                    break
        if flag == 0:
            print('---------------')
            if len(Email_list) == 0:
                unique_soi['SOI'] = SOI_dict[i]
                print('....................')
                break
            print(SOI_dict[i]['email'])
            print(SOI_dict[i]['email'].split('@')[1])
            if SOI_dict[i]['email'].split('@')[1] in Email_list:
                unique_soi['SOI'] = SOI_dict[i]
                break
    print('===============',unique_soi)
    if len(unique_soi) == 0:
        print('No unique_soi email found...............')
    login_out_sql(conn,cursor) 

    return unique_soi      

def write_one_info(Mission_list,submit,Cookie = ''):
    Email_Id = ''
    BasicInfo_Id = '' 
    account = get_account()
    conn,cursor=login_sql(account)  
    for item in submit:
        if item == 'Email':
            Email_Id = submit['Email']['Email_Id']
        else:
            try:
                BasicInfo_Id = submit[item]['BasicInfo_Id']
            except:
                pass
    Alliance = str(submit['Alliance'])
    Account = str(submit['Account'])
    ua = submit['ua']
    if 'Status' not in submit:
        Status = str(0)
    else:
        Status = submit['Status']
    # print('+++++++++++++++++++++++++')
    for Mission_Id in Mission_list:
        sql_content = 'INSERT INTO Mission(Mission_Id,Alliance,Account,Email_Id,BasicInfo_Id,ua,Cookie,Status)VALUES("%s","%s","%s","%s","%s","%s","%s","%s")'%(Mission_Id,Alliance,Account,Email_Id,BasicInfo_Id,ua,Cookie,Status)
        print('==============')
        # print(submit)
        # print(sql_content)
        res = cursor.execute(sql_content)   
        response = cursor.fetchall()        
        # print(response) 
    login_out_sql(conn,cursor)

def write_log_db(Mission_Id,traceback_,png):
    # sql_content = 'INSERT INTO Log(Mission_Id,traceback,png)VALUES("%s","%s","%s");'%(str(Mission_Id),pymysql.escape_string(traceback_),pymysql.Binary(png))
    # sql_content = 'INSERT INTO Log(Mission_Id,traceback,png)VALUES(str(Mission_Id),pymysql.escape_string(traceback_),pymysql.Binary(png));' 
    # print(type(pymysql.Binary(png)))
    # print(sql_content)
    account = get_account()
    conn,cursor=login_sql(account)    
    # res = cursor.execute(sql_content)  
    # args = (str(Mission_Id),pymysql.escape_string(traceback_),pymysql.Binary(png))  
    args = (int(Mission_Id),pymysql.escape_string(traceback_),png)      
    res = cursor.execute('INSERT INTO Log(Mission_Id,traceback,png)VALUES("%s","%s",_binary"%s")',args)        
    # -- res = cursor.execute('INSERT INTO Log(Mission_Id,traceback,png)VALUES("%s","%s","%s")',args)            
    login_out_sql(conn,cursor)    

def makedir_pic(path=r'c:\EMU\log\pic'):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)

def read_pic(Mission_Id):
    path_pic=r'c:\EMU\log\pics'
    folder = os.path.join(path_pic,str(Mission_Id))
    makedir_pic(folder)
    modules = os.listdir(folder)
    # print(modules)
    path_ = os.path.join(os.getcwd(),folder)
    modules_path = [os.path.join(path_,file) for file in modules]
    [os.remove(file) for file in modules_path]

    account = get_account()
    conn,cursor=login_sql(account)   
    print('===') 
    sql_content = 'SELECT Create_time,png FROM Log WHERE Mission_Id="%s" limit 30'%str(Mission_Id)
    # res = cursor.execute(sql_content)  
    res = cursor.execute(sql_content)  
    print(res)
    # fout = open('quchu1.png','wb')
    s = cursor.fetchall()
    for pic in s:
        name = str(pic[0]).replace(':','')+'.png'
        pic_ = os.path.join(folder,str(name))
        with open(pic_,'wb') as f:
            f.write(pic[1][1:-1])
    login_out_sql(conn,cursor) 
    print('Total %d pics for Mission %d'%(len(s),int(Mission_Id)))        

def read_txt_traceback(Mission_Id):
    path_pic=r'c:\EMU\log\pics'
    folder = os.path.join(path_pic,str(Mission_Id))
    makedir_pic(folder)
    modules = os.listdir(folder)
    # print(modules)
    path_ = os.path.join(os.getcwd(),folder)
    modules_path = [os.path.join(path_,file) for file in modules]
    # [os.remove(file) for file in modules_path]

    account = get_account()
    conn,cursor=login_sql(account)    
    sql_content = 'SELECT traceback,Create_time FROM Log WHERE Mission_Id="%s"'%str(Mission_Id)
    # res = cursor.execute(sql_content)  
    res = cursor.execute(sql_content)  
    # print(res)
    # fout = open('quchu1.png','wb')
    s = cursor.fetchall()
    content = ''
    for trace in s:
        content += str(trace[1]).replace('\\n','\n')+'\n\n'+trace[0].replace('\\n','\n')+'\n\n'
    name = str(Mission_Id)+'.txt'
    txt_ = os.path.join(folder,str(name))    
    # content = content.replace('\\n','\n')
    with open(txt_,'w') as f:
        f.write(content)
    login_out_sql(conn,cursor) 

def get_alliances_info():
    account = get_account()
    conn,cursor=login_sql(account)    
    sql_content = 'Select Alliance_name from alliances'
    cursor.execute(sql_content)    
    res = cursor.fetchall()
    # print(res)
    alliances = [item[0] for item in res]
    login_out_sql(conn,cursor)
    return alliances

def updata_alliance_description(alliance,description):
    account = get_account()
    conn,cursor=login_sql(account)    
    sql_content = 'Select * from alliances WHERE alliance = "%s"'%(alliance)
    cursor.execute(sql_content)
    res = cursor.fetchall()
    if len(res) != 0:
        sql_content = 'UPDATE alliances SET Description = "%s" WHERE alliance = "%s"'%(description,alliance)
    else:
        sql_content = 'insert into alliances(alliance,description)values("%s","%s")'%(alliance,description)
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

def update_data(table,keys,values):
    # values=[proxy,'Socket5','Good']
    # table = 'Ip_Pools'
    # keys = ['Ip','Type','Status']
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
        # print(values)
        # print(values[i])
        if type(values[i]) == type_str:
            a+='"{}",'
        else:
            a+='{},'
    a = a[0:-1] + ');'
    sql_content = a.format(*values)
    return sql_content    

def Execute_sql(sql_contents):
    account = get_account()
    # print(account)
    conn,cursor = login_sql(account)
    for sql_content in sql_contents:
        # print('\n\n\n')
        # print(sql_content)
        try:
            res = cursor.execute(sql_content)
            response = cursor.fetchall()
            # print(response)
        except Exception as e:
            print(str(e))
            pass
        # print(response)
    login_out_sql(conn,cursor)
    print('Login out db')

def Execute_sql_single(sql_contents,ali=0):
    account = get_account(ali)
    # print(account)
    responses = []
    conn,cursor = login_sql(account)
    for sql_content in sql_contents:
        print(sql_content)
        res = cursor.execute(sql_content)
        print(res)
        response = cursor.fetchall()
        responses.append(response)
    # desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    # response = cursor.fetchall()
    # res_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    # print(response)
    login_out_sql(conn,cursor)
    print('Login out db')
    return responses

def email_test():
    sql_content1 = 'SELECT * from Email'
    sql_contents = [sql_content1]
    account = get_account()
    conn,cursor = login_sql(account)
    for sql_content in sql_contents:
        print(sql_content)
        res = cursor.execute(sql_content)
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    login_out_sql(conn,cursor)  
    return Email_dict

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
    # upload_data()    


def get_ssn():
    '''
    empty
    ''
    '''
    account = get_account()
    conn,cursor=login_sql(account)
    Excel_name = 'Uspd_big'
    res = cursor.execute('SELECT * from BasicInfo WHERE Excel_name = "%s" and ssn_status = "empty"'%Excel_name)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    ssn_empty = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    print('Total %d ssn_empty get'%len(ssn_empty))
    res = cursor.execute('SELECT * from BasicInfo WHERE Excel_name = "%s" and ssn_status = "" '%Excel_name)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    ssn_isnull = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    print('Total %d ssn_isnull get'%len(ssn_isnull))    
    login_out_sql(conn,cursor)

    return ssn_empty,ssn_isnull


def get_driver_license():
    account = get_account()
    conn,cursor=login_sql(account)
    sql_content = 'select drivers_license from Basicinfo where Excel_name = "Us_pd_native"'
    cursor.execute(sql_content)
    res = cursor.fetchall()
    driver_licenses = [key[0] for key in res]
    print(driver_licenses[:20])
    print('Total %d licenses'%len(driver_licenses))
    # for driver_license in driver_licenses:

    login_out_sql(conn,cursor)
    return driver_licenses


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
    Info_dicts_all = [0,0]
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
                        # print(BasicInfo_dict[i]['BasicInfo_Id'])
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
                if str(Mission_dict[j]['Mission_Id']) in Mission_list: 
                    if Email_dict[i]['Email_Id'] == Mission_dict[j]['Email_Id']:
                        flag = 1
                        break
            if flag == 0:
                Info_dicts[1] += 1
    login_out_sql(conn,cursor)
    # submit = dict(Info_dict,**Info_dict2)
    return Info_dicts

def read_all_info():
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT Excel_name from BasicInfo')
    # res = cursor.execute('SELECT COUNT(*) FROM BasicInfo') 
    # res = cursor.execute('SELECT COUNT(*) FROM BasicInfo where Excel_name = "Uspd"')     
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    BasicInfo_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    # print(BasicInfo_dict)
    excels = {}
    for info in BasicInfo_dict:
        if info['Excel_name'] not in excels:
            excels[info['Excel_name']] = 0
        else:
            excels[info['Excel_name']] += 1
    # print(excels)
    # return excels
    # for key in BasicInfo_dict:
        # print(key)
    res = cursor.execute('SELECT Mission_Id from Mission')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    Missions = {}
    for Mission in Mission_dict:
        if Mission['Mission_Id'] not in Missions:
            Missions[Mission['Mission_Id']] = 0
        else:
            Missions[Mission['Mission_Id']] += 1
    # print(Missions)
    res = cursor.execute('SELECT * from Email')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    print(Email_dict)
    num = 0
    for i in range(len(Email_dict)):
        # print(i)
        if Email_dict[i]['Status'] == 'Bad':
            continue
        num+=1
    emails = {}
    emails['Email'] = num
    # for email in Email_dict:
    #     if email['Mission_Id'] not in emails:
    #         email[Mission['Mission_Id']] = 0
    #     else:
    #         email[Mission['Mission_Id']] += 1
    # print(emails)    
    # print(excels,emails,Missions)
    login_out_sql(conn,cursor) 
    return excels,emails,Missions

def get_mission_num_available():
    account = db.get_account()
    conn,cursor=db.login_sql(account)    
    Excel_name = 'Uspd_small'
    Mission_Id = 10088
    '''
    id in excel
    '''
    res = cursor.execute('SELECT Basicinfo_Id from BasicInfo where Excel_name="%s"'%Excel_name)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    ids = [item['Basicinfo_Id'] for item in Mission_dict]
    ids = list(set(ids))
    print('Info Number in excel %s:%d'%(Excel_name,len(ids)))    

    res = cursor.execute('SELECT Basicinfo_Id from Mission where Mission_Id="%d"'%Mission_Id)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict2 = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来          
    ids2 = [item['Basicinfo_Id'] for item in Mission_dict2]
    ids2 = list(set(ids2))
    print('Info Number in Mission table for Mission_Id %d:%d'%(Mission_Id,len(ids2)))    
    ids_unique = [id_ for id_ in ids if id_ not in ids2]
    print('Available Info Number for Mission_Id %d:%d'%(Mission_Id,len(ids_unique)))  
    login_out_sql(conn,cursor) 



def test_rest():
    Mission_list = [10005]
    Excel_name = ['','Email']
    Email_list = ['hotmail.com','aol.com','outlook.com','yahoo.com']
    rest = read_rest(Mission_list,Excel_name,Email_list)
    print(rest)

def delete_old_data():
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)    
    res = cursor.execute('SELECT Email_Id,BasicInfo_Id from Mission')
    response = cursor.fetchall()
    # print(response)
    Email_sets = []
    [Email_sets.append(a[0]) for a in response]
    Basicinfo_sets = []
    [Basicinfo_sets.append(a[1]) for a in response]    
    print(len(Email_sets))
    print(len(Basicinfo_sets))
    # print(Mission_dict)
    res = cursor.execute('SELECT BasicInfo_Id from BasicInfo')
    response = cursor.fetchall()
    # BasicInfo_Id_dict = [dict(zip('BasicInfo_Id', row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来      
    # print(BasicInfo_Id_dict)
    # print(response)
    BasicInfo_Id_dict = []
    [BasicInfo_Id_dict.append(a[0]) for a in response]
    print('Total',len(BasicInfo_Id_dict),'BasicInfos in BasicInfo db')

    # print(BasicInfo_Id_dict)
    # print(len(BasicInfo_Id_dict))
    # print(len(set(BasicInfo_Id_dict)))
    res = cursor.execute('SELECT Email_Id from Email')
    response = cursor.fetchall()    
    Email_Id_dict = []
    [Email_Id_dict.append(a[0]) for a in response]
    # print(Email_Id_dict)
    print('Total',len(Email_Id_dict),'Emails in email db')
    Email_sets_todelete = [a for a in Email_sets if a not in Email_Id_dict and  a != '' ]
    BasicInfo_sets_todelete = [a for a in Basicinfo_sets if a not in BasicInfo_Id_dict and  a != '' ]    
    print(Email_sets_todelete)
    print('TO delete email id:',len(Email_sets_todelete))
    print(BasicInfo_sets_todelete)
    print('TO delete BasicInfo id:',len(BasicInfo_sets_todelete))
    sql_contents=[]
    [sql_contents.append('DELETE  from Mission WHERE Email_Id = "%s"'%Email_Id) for Email_Id in Email_sets_todelete]
    [sql_contents.append('DELETE  from Mission WHERE BasicInfo_Id = "%s"'%BasicInfo_Id) for BasicInfo_Id in BasicInfo_sets_todelete]    
    login_out_sql(conn,cursor)
    Execute_sql(sql_contents)
    return

def delete_page_flag(Mission_Id,Page):
    sql_content = 'DELETE from Page_Flag WHERE Mission_Id = "%d" and Page = "%s"'%(int(Mission_Id),str(Page))
    sql_content = [sql_content]
    Execute_sql(sql_content)

def delete_page(Mission_Id,Page):
    sql_content1 = 'DELETE from Page_Flag WHERE Mission_Id = "%d" and Page = "%s"'%(int(Mission_Id),str(Page))
    sql_content2 = 'DELETE from Page_Config WHERE Mission_Id = "%d" and Page = "%s"'%(int(Mission_Id),str(Page))    
    sql_content = [sql_content1,sql_content2]
    Execute_sql(sql_content)

def delete_step(Mission_Id,Page,Step):
    print('===')
    sql_content = 'DELETE from Page_Config WHERE Mission_Id = "%d" and Page = "%s" and Step = "%d"'%(int(Mission_Id),str(Page),int(Step))    
    sql_content = [sql_content]
    Execute_sql(sql_content)


def get_duplicated_mission_record():
    sql_content1 = 'SELECT Mission_Id,Basicinfo_Id,count(*) as count from mission group by Mission_Id,Basicinfo_Id having count>1;'
    sql_content2 = 'SELECT Mission_Id,Email_Id,count(*) as count from mission group by Mission_Id,Email_Id having count>1;'

    Execute_sql([sql_content1,sql_content2])


# @timeout(30)
def read_plans(plan_id):
    '''
    return:
        plans:list of plans,eg.[plan1,plan2]
            plan1: list of Offer_links ,containing lpm_port
                Offer_links = [{'Mission_Id':10009,lpm_port:24002...},{'Mission_Id':10009,lpm_port:24003...},{'Mission_Id':10003,lpm_port:24004...}...]
                palns = {'1':Offer_links1,'2':Offer_links2,...}                
    '''
    # print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    plan_id = int(plan_id)
    if plan_id != -1:
        sql_content = 'SELECT * from Plans WHERE Plan_Id = %d'%plan_id
    else:
        sql_content = 'SELECT * from Plans'        
    res = cursor.execute(sql_content)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    plans = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    login_out_sql(conn,cursor)
    for plan in plans:
        plan['Mission_dir'] = plan['Mission_dir'].replace('//','\\')  
        plan['Excel'] = plan['Excel'].split(',')
    print('Find plan num:',len(plans))
    return plans

def upload_plans(plans):
    table = 'Plans'
    sql_contents = []
    for item in plans:
        list_keys , list_values =list(plans[item].keys()), list(plans[item].values()) 
        for i in range(len(list_values)):
            if type(list_values[i]) == type([]):
                list_values[i] = list_values[i][0]+','+list_values[i][1]
        # print(list_values)
        sql_content = get_upload_sql_content(table,list_keys,list_values)
        # print(sql_content)
        sql_contents.append(sql_content)
    print('==============================')
    print(sql_contents)
    Execute_sql(sql_contents)    
    # update_data(table,keys,values)

def test_dict():
    dict_test = {'0': {'Alliance': 'Finaff', 'Offer': 'Royal Cams(Done)', 'url_link': 'http', 'Country': 'US', 'Mission_Id': '10000', 'Excel': ['', 'Email']}}
    list_keys , list_values = dict_test['0'].keys(), dict_test['0'].values()    
    print(list(list_keys))
    # print(type(list_keys))
    print(list(list_values))

def get_cookie(Config=None):
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from Mission WHERE cookie!="" and Mission_Id="%s" and Alliance="%s" and Account="%s"'%(Config['Mission_Id'],Config['Alliance'],Config['Account']))
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    # print(len(Mission_dict))
    # print(Mission_dict)
    login_out_sql(conn,cursor)     
    return Mission_dict

def get_cehuoaccount(submit):
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from accounts WHERE country="%s" and cookie!="" and Mission_Id="%s" and  status!="%d" and flag!="%d" limit 0,1'%(submit['Country'],submit['Mission_Id'],1,1))
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    account_ = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    if len(account_) == 0:
        return {}
    account = account_[0]
    # print(len(Mission_dict))
    # print(Mission_dict)
    update_accounts(account['BasicInfo_Id'])
    login_out_sql(conn,cursor)     
    return account    

def get_page_flag(Mission_Id):
    print('     Start reading info from sql server...')
    account = get_account(1)
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from Page_Flag WHERE Mission_Id="%d"'%int(Mission_Id))
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Pages = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    login_out_sql(conn,cursor)
    print('Login out db')    
    # print(len(Mission_dict))
    # print(Mission_dict)
    return Pages

def unchosse_states(submit):
    Mission_Id = submit['Mission_Id']
    Excel_name = submit['Excel_name']
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from Basicinfo WHERE Excel_name="%s"'%str(Excel_name))
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    infos = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    states = submit['states']
    print('==========')
    print(states)
    ids = []
    for info in infos:
        if info['state'] in states:
            print(info['state'])
            ids.append(info['BasicInfo_Id']) 
    print('Total %d infos to delete'%len(ids))
    for id_ in ids:
        print('delete %s'%id_)
        sql_content = 'INSERT INTO Mission(Mission_Id,Alliance,Account,Email_Id,BasicInfo_Id,ua,Cookie,Status)VALUES("%s","%s","%s","%s","%s","%s","%s","%s")'%(Mission_Id,'','','',id_,'','','1')
        res = cursor.execute(sql_content)
        # response = cursor.fetchall() 
        # print(response)
    print('delete finished..............')
    login_out_sql(conn,cursor)
    print('Login out db')
    # print(len(Mission_dict))
    # print(Mission_dict)
    return infos

def get_page_config(Mission_Id,Page):
    print('     Start reading info from sql server...')
    account = get_account(1)
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from Page_config WHERE Mission_Id="%d" and Page="%s"'%(int(Mission_Id),str(Page)))
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Pages = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    login_out_sql(conn,cursor)
    print('Login out db')    
    # print(len(Mission_dict))
    # print(Mission_dict)
    return Pages

def get_state_byzip(zip_):
    print('     Start reading info from sql server...')
    account = get_account(1)
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from BasicInfo WHERE zip="%s" limit 1'%(str(zip_)))
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    statedict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    print('statedict:',statedict)
    login_out_sql(conn,cursor)
    print('Login out db')    
    # print(len(Mission_dict))
    # print(Mission_dict)
    return statedict[0]['state']

def add_key_db(sql_content):
    sql_content = "ALTER TABLE Mission ADD Alliance_basic DEFAULT '' AFTER BasicInfo_Id"
    Execute_sql([sql_content])

def clean_table(plan_id):
    sql_content = 'delete from Plans WHERE plan_id = %d'%int(plan_id)
    Execute_sql([sql_content])

def update_key():
    sql_content = "UPDATE Plans SET Plan_Id = 1 WHERE Mission_id = '%s'" % ('10000')
    Execute_sql([sql_content])

def update_port(port_old,port_new):
    sql_content = "UPDATE Plans SET port_lpm = '%s' WHERE port_lpm = '%s'" % (port_new,port_old)
    Execute_sql([sql_content])

def update_plan_status(Status,ID):
    sql_content = "UPDATE Plans SET Status = '%d' WHERE ID = '%d'" % (int(Status),int(ID))
    print('updating:',sql_content)
    Execute_sql([sql_content])

def get_plan_status(ID):
    sql_content = "SELECT * from plans WHERE ID = '%d'" % (int(ID))
    account = get_account()
    # print(account)
    conn,cursor = login_sql(account)
    # for sql_content in sql_contents:
        # print('\n\n\n')
        # print(sql_content)
    res = cursor.execute(sql_content)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    plans = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    print(plans)
    Status = plans[0]['Status']
    print('Status:',Status)
    login_out_sql(conn,cursor)
    return Status

def get_updateinfo():
    sql_content = "select * from update_config;"
    account = get_account(1)
    # print(account)
    conn,cursor = login_sql(account)
    # for sql_content in sql_contents:
        # print('\n\n\n')
        # print(sql_content)
    res = cursor.execute(sql_content)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    update_config = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    print(update_config[0])
    login_out_sql(conn,cursor)    
    return update_config



def update_flag_use(id_):
    return
    sql_content = "UPDATE BasicInfo SET flag_use = 0 WHERE BasicInfo_Id = '%s'" % id_
    print(sql_content)
    Execute_sql([sql_content])

def update_flag_use_all():
    print('Start cleaning.....')
    sql_content = "UPDATE BasicInfo SET flag_use = 0 WHERE flag_use = 1"
    Execute_sql([sql_content])

def get_ports_set():
    # print('     Start reading info from sql server...')
    account = get_account()
    vc_range = account['vc_range']
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from plans')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    plans = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    # print(len(Mission_dict))
    # print(Mission_dict)
    # print(plans[0])
    # print(len(plans))
    plans = [plan for plan in plans if int(plan['Plan_Id'])>=vc_range[0] and int(plan['Plan_Id'])<=vc_range[1]]
    # print(len(plans))    
    ports_set = [plan['port_lpm'] for plan in plans]
    login_out_sql(conn,cursor)     
    return ports_set    



def read_alias_num():
    Offer_configs = {}
    with open(r'ini\alias_num.ini') as f:
        lines = f.readlines()
        alias = {}
        for line in lines:
            if ',' in line:
                config = line.split(',')                
                alias[str(config[0])] = str(config[1])
    # print(Offer_configs)
    return alias

def get_luminati_submit(Config): 
    Email_list = {"hotmail.com": 1, "outlook.com": 1, "yahoo.com": 1, "aol.com": 1}
    Mission_Ids,Excels_dup = [Config['Mission_Id']],Config['Excel']
    # print(Excels_dup)
    Mission_Id  = Config['Mission_Id']
    if Config['Excel'][0] == 'Dadao':
        submit = {}
        path = r'..\res\Dadao.xlsx'
        sheet,workbook = Dadao.get_excel(path)   
        submit['Dadao'] = Dadao.get_one_data(sheet,Mission_Id,Config['Country'])
        print(submit)
        if len(submit['Dadao']) == 0:
            return {}
        submit['Dadao']['Mission_Id'] = Mission_Id 
        submit['Dadao']['path'] = path
        submit['Dadao']['workbook'] = workbook 
    else:
        alias = read_alias_num()
        if str(Mission_Ids[0]) in alias:
            Mission_Ids[0] = alias[str(Mission_Ids[0])].replace('\n','')
            Config['Mission_Id'] = Mission_Ids[0]
        submit = read_one_excel(Mission_Ids,Excels_dup,Email_list)
    if submit == {}:
        return {}
    # print(submit)
    submit['ip_lpm'] = Config['ip_lpm']
    submit['port_lpm'] = Config['port_lpm']
    if Excels_dup[0] == '':
        submit['state_'] = ''
    else:
        if Excels_dup[0] != 'Dadao':
            submit['state_'] = submit[Excels_dup[0]]['state']
        else:
            submit['state_'] = ''
    submit['Mission_Id'] = Config['Mission_Id']
    submit['Country'] = Config['Country']
    submit['Site'] = Config['url_link']
    submit['Excels_dup'] = Excels_dup
    submit['Alliance'] = Config['Alliance']
    submit['Account'] = Config['Account']
    submit['Offer'] = Config['Offer']
    submit['ID'] = Config['ID']
    # submit['Pic'] = Config['Pic']    
    submit['zone'] = Config['zone']    
    # submit['city'] = Config['city'] 
    if 'sleep_flag' in Config:
        submit['sleep_flag'] = Config['sleep_flag']
    # print(submit['Site'])
    submit['Mission_dir'] = Config['Mission_dir'] 
    submit['Record'] = Config['Record']  
    # print(submit)
    uas = Chrome_driver.get_ua_all()
    ua = Chrome_driver.get_ua_random(uas)
    # print(ua)  
    submit['ua'] = ua
    return submit

def upload_alliance_info(infos):
    sql_contents = ['use emu']
    for info in infos:
        print(info)
        keys_detect = ['Alliance_name','Skypes','Number of Offers','Commission Type','Minimum Payment','Payment Frequency','Payment Method','Referral Commission','Tracking Software','Tracking Link']
        for key in keys_detect:
            if key not in info:
                print(key,'of info not in keys of database')
                info[key] = ''
        Alliance_name = info['Alliance_name']
        print(Alliance_name)
        Number_of_Offers = info['Number of Offers'] 
        Commission_Type = info['Commission Type'] 
        Minimum_Payment = info['Minimum Payment'] 
        Payment_Frequency = info['Payment Frequency'] 
        Payment_Method = info['Payment Method'] 
        Referral_Commission = info['Referral Commission'] 
        Tracking_Software = info['Tracking Software'] 
        Tracking_Link = info['Tracking Link'] 
        Alliance_url = info['alliance_url']
        Skypes = info['Skypes'] 
        sql_content = r'INSERT IGNORE INTO alliances(Alliance_name,Alliance_url,Skypes,NumberofOffers,Commission_Type,Minimum_Payment,Payment_Frequency,Payment_Method,Referral_Commission,Tracking_Software,Tracking_Link)VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(Alliance_name,Alliance_url,Skypes,Number_of_Offers,Commission_Type,Minimum_Payment,Payment_Frequency,Payment_Method,Referral_Commission,Tracking_Software,Tracking_Link)
        sql_contents.append(sql_content)
    print(sql_contents)
    Execute_sql(sql_contents)    

def update_cookie(submit):
    print('Uploading cookie')
    print('Mission_Id:',submit['Mission_Id'])
    print('Email_Id:',submit['Email']['Email_Id'])
    print('Cookie:',submit['Cookie'])
    sql_content = "UPDATE Mission SET Cookie = '%s' WHERE Mission_id = '%s' and Email_Id = '%s'" % (pymysql.escape_string(submit['Cookie']),submit['Mission_Id'],submit['Email']['Email_Id'])
    Execute_sql([sql_content])

def upload_offer_config(Offer_configs):
    sql_contents = []
    for Offer_name in Offer_configs:
        Offer_config = Offer_configs[Offer_name]
        Mission_Id = Offer_config['Mission_Id']
        Excel = Offer_config['Excel'][0]+','+Offer_config['Excel'][1]
        sql_content = 'INSERT INTO Offer_config(Mission_Id,Excel,Offer_name)VALUES("%s","%s","%s")'%(Mission_Id,Excel,Offer_name)      
        sql_contents.append(sql_content)
    # print(sql_contents)
    # return
    Execute_sql(sql_contents)    

def upload_Allinace_config(Offer_configs):
    sql_contents = []
    for key in Offer_configs:
        for Mission_Id in Offer_configs[key]:
            Offer_config = Offer_configs[key]
            Alliance_name = key
            sql_content = 'INSERT INTO Alliance_config(Alliance_name,Mission_Id)VALUES("%s","%s")'%(Alliance_name,Mission_Id)      
            sql_contents.append(sql_content)
    # print(sql_contents)
    Execute_sql(sql_contents)   

def upload_offer(Mission_name,Mission_Id,Excel):
    # Mission_name = '123test'
    # Mission_Id = '10200'
    # Excel = ['','Uspd']
    Offer_configs = {}
    Offer_configs[Mission_name] = {}
    Offer_configs[Mission_name]['Mission_Id'] = Mission_Id
    Offer_configs[Mission_name]['Excel'] = Excel    
    upload_offer_config(Offer_configs)

def upload_alliance(Alliance_name,Mission_Id):
    # Mission_name = '123test'
    # Mission_Id = '10200'
    # Excel = ['','Uspd']
    Offer_configs = {}
    Offer_configs[Alliance_name] = [str(Mission_Id)]
    upload_Allinace_config(Offer_configs)


def get_current_version():
    sql_content = "SELECT * FROM VERSION"
    res = Execute_sql_single([sql_content],1)
    # print(res)
    # print('Current version:',res[0][0][0])
    num = res[0][0][0].split('.')
    return num    

def update_version(type_=0):
    '''
    type_:
        0--1.0.0-->1.0.1
        1--1.0.0-->1.1.0
    '''
    num = get_current_version()
    if type_ == 0:
        num[2] = str(int(num[2])+1)
    else:
        num[1] = str(int(num[1])+1)
    version_num = num[0]+'.'+num[1]+'.'+num[2]
    print('Next version:',version_num)
    sql_content = "UPDATE VERSION SET version = '%s'" % (version_num)
    Execute_sql([sql_content])
    file = r'ini\\VERSION.ini'
    with open(file,'w') as f:
        f.write(version_num)    


def change_version():
    num_db = db.get_current_version()
    num_db = str.join('.',num_db)    



def delete_offer_config(Mission_Id):
    sql_content = "DELETE FROM Offer_config where Mission_Id = '%s'"%str(Mission_Id)
    Execute_sql([sql_content])
    # print(res)
    # offers = {}
    # for offer_config in res[0]: 
    #     offers[offer_config[2]] = offer_config[0]
    # return res

def delete_alliance_config(Alliance_name,Mission_Id):
    sql_content = "DELETE FROM Alliance_config where Alliance_name = '%s' and Mission_Id = '%s'"%(Alliance_name,str(Mission_Id))
    res = Execute_sql_single([sql_content])
    return res



def get_offer_config():
    sql_content = "SELECT * FROM Offer_config"
    res = Execute_sql_single([sql_content])
    # print(res)
    # offers = {}
    # for offer_config in res[0]: 
    #     offers[offer_config[2]] = offer_config[0]
    return res

def get_alliance_config():
    sql_content = "SELECT * FROM Alliance_config"
    res = Execute_sql_single([sql_content])
    print(res)
    alliances = {}
    for offer_config in res[0]: 
        if offer_config[0] not in alliances:
            alliances[offer_config[0]] = offer_config[1]
        else:
            alliances[offer_config[0]]+='+'+offer_config[1]
    return alliances

def upload_accounts(submit):
    print('Uploading accounts')
    print('Mission_Id:',submit['Mission_Id'])
    # print('Email_Id:',submit['Email']['Email_Id'])
    print('Cookie:',submit['Cookie'])
    sql_content = 'INSERT INTO accounts(BasicInfo_Id,Mission_Id,country,ua,cookie)VALUES("%s","%s","%s","%s","%s")'%(submit['BasicInfo_Id'],submit['Mission_Id'],submit['Country'],submit['ua'],pymysql.escape_string(submit['Cookie']))      
    Execute_sql([sql_content])

def update_accounts(BasicInfo_Id):
    sql_content = "UPDATE accounts SET flag = '%d' WHERE BasicInfo_Id = '%s'" % (1,BasicInfo_Id)
    Execute_sql([sql_content])

def upload_traffic_keys(Mission_Id,country,key):
    sql_content = 'INSERT INTO traffic_key(Mission_Id,Country,traffic_key)VALUES("%d","%s","%s")'%(int(Mission_Id),country,key)
    Execute_sql([sql_content])

def update_activate_status(submit):
    print('Uploading activate status')
    print('Mission_Id:',submit['Mission_Id'])
    print('Email_Id:',submit['Email_Id'])
    print('Cookie:',submit['Cookie'])
    sql_content = "UPDATE Mission SET activate1 = '%s',activate2 = '%s',activate3 = '%s' WHERE Mission_id = '%s' and Email_Id = '%s'" % (submit['activate1'],submit['activate2'],submit['activate3'],submit['Mission_Id'],submit['Email_Id'])
    Execute_sql([sql_content])

def check_mission_status(submit):
    sql_content = "SELECT * FROM Mission  WHERE Mission_id = '%s' and Email_Id = '%s'" % (submit['Mission_Id'],submit['Email']['Email_Id'])
    account = get_account()
    print(account)
    conn,cursor = login_sql(account)
    res = cursor.execute(sql_content)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_status_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    login_out_sql(conn,cursor) 
    return Mission_status_dict

def get_traffic_key(Mission_Id,country):
    sql_content = "SELECT traffic_key FROM traffic_key  WHERE Mission_id = '%d' and Country = '%s'" % (int(Mission_Id),country)
    account = get_account()
    print(account)
    conn,cursor = login_sql(account)
    res = cursor.execute(sql_content)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    traffic_key = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    login_out_sql(conn,cursor) 
    if len(traffic_key) == 0:
        return ''
    else:
        return traffic_key[0]['traffic_key']

def get_soi_email():
    sql_content = "SELECT * FROM Basicinfo WHERE Excel_name = 'soi'"
    account = get_account()
    conn,cursor = login_sql(account)
    res = cursor.execute(sql_content)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_status_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    login_out_sql(conn,cursor) 
    return Mission_status_dict

def hotupdate(i):
    import hotupdate_contests as hu
    content = hu.get_contents(i)
    print(content)
    Execute_sql(content)

def get_cst_zone(tzid):
    sql_content = "SELECT windows,tzid FROM Basicinfo WHERE Excel_name = 'tz' and tzid like '%s';"%('%'+tzid+'%')
    account = get_account()
    conn,cursor = login_sql(account)
    res = cursor.execute(sql_content)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_status_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    login_out_sql(conn,cursor) 
    return Mission_status_dict    

if __name__ == '__main__':
    print('test')
    try:
        init()
    except:
        pass
    # delete_old_data()
    print('')
    upload_data()
    # get_duplicated_mission_record()
    # plans = {'0': {'Alliance': 'Finaff', 'Offer': 'Royal Cams(Done)', 'url_link': 'http', 'Country': 'US', 'Mission_Id': '10000', 'Excel': ['', 'Email']}}
    # upload_plans(plans)
    # add_key_db()
    # plans = read_plans()
    # print(plans)
    # update_key()
    # hotupdate(5)
