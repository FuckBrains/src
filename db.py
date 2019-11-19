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
    ip = 'rm-bp100p7672g0g8z9kjo.mysql.rds.aliyuncs.com'
    conn = pymysql.connect(host= ip,port=3306,user=account['username'],passwd=str(account['pwd']),charset='utf8mb4',use_unicode=True)
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
    excels_path = [os.path.join(path,file) for file in files if 'xlsx' in file]
    conn,cursor = login_sql(account)
    for path_excel in excels_path:
        # print(path_excel)
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

def read_one_excel(Mission_list,Excel_name,Email_list):
    print('     Start reading info from sql server...')
    account = get_account()
    conn,cursor=login_sql(account)
    print('     Login success')    
    res = cursor.execute('SELECT * from Mission WHERE Mission_Id="%d"'%int(Mission_list[0]))
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
    num = 0
    step = 100
    Info_dicts = {}   
    Mission_basicinfo_list = [Mission['BasicInfo_Id'] for Mission in Mission_dict]
    Mission_email_list = [Mission['Email_Id'] for Mission in Mission_dict]  
    sql_content = 'SELECT COUNT(*) FROM Basicinfo WHERE Excel_name="%s"'%Excel_name[0]
    res = cursor.execute(sql_content)
    tt = cursor.fetchall()
    print(tt)
    num_excel = tt[0][0]
    print(num_excel)
    Basicinfo_ids = []     
    if Excel_name[0] != '' :
        while True:
            # res = cursor.execute('SELECT * from BasicInfo  WHERE Excel_name = "%s" limit 0,1'%(Excel_name[0]))
            res = cursor.execute('SELECT * from BasicInfo  WHERE Excel_name = "%s" and flag_use = 0 ORDER BY rand() limit 10'%Excel_name[0])
            # res = cursor.execute('SELECT * from BasicInfo  WHERE Excel_name = "%s" and flag_use = 0 limit %d,%d'%(Excel_name[0],num,step))            
            print(res)
            desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
            BasicInfo_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
            for info in BasicInfo_dict:
                print('leninfo',len(info))
                if info['BasicInfo_Id'] not in Mission_basicinfo_list:
                    # print(Info_dicts[Excel_name[0]])
                    # print(BasicInfo_dict)
                    print(1)
                    Info_dicts[Excel_name[0]] = info
                    break
                if info['BasicInfo_Id'] not in Basicinfo_ids:
                    Basicinfo_ids.append(info['BasicInfo_Id'])

            sql_content = 'SELECT COUNT(*) FROM Basicinfo WHERE Excel_name="%s" and flag_use = 1'%Excel_name[0]
            res = cursor.execute(sql_content)
            ff = cursor.fetchall()
            print(ff)
            num_flag = ff[0][0]     
            print(num_flag,'infos flag_use = 1')           
            if len(Info_dicts) > 0:
                break            
            if len(Basicinfo_ids) == num_excel-num_flag:
                print('No available data for Mission_Id:',str(Mission_list[0]))
                return
        sql_content = "UPDATE BasicInfo SET flag_use = 1 WHERE BasicInfo_Id = '%s'" % Info_dicts[Excel_name[0]]['BasicInfo_Id']
        res = cursor.execute(sql_content)                 
    else:
        BasicInfo_dict = {}
    if Excel_name[1] != '':
        res = cursor.execute('SELECT * from Email')
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        Email_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来       
    else:
        # Excel_name[1] = {}
        Email_dict = {}            
    Info_dict2 = {}
    if len(Email_dict) != 0:
        list_Email = random.sample(range(len(Email_dict)),len(Email_dict))
        print(len(Email_dict))
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
                print('find email unique')
                Info_dict2 = Email_dict[i]
                break
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
    print('+++++++++++++++++++++++++')
    for Mission_Id in Mission_list:
        sql_content = 'INSERT INTO Mission(Mission_Id,Alliance,Account,Email_Id,BasicInfo_Id,ua,Cookie)VALUES("%s","%s","%s","%s","%s","%s","%s")'%(Mission_Id,Alliance,Account,Email_Id,BasicInfo_Id,ua,Cookie)
        print('==============')
        print(sql_content)
        res = cursor.execute(sql_content)    
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
    sql_content = 'SELECT png FROM Log WHERE Mission_Id="%s"'%str(Mission_Id)
    # res = cursor.execute(sql_content)  
    res = cursor.execute(sql_content)  
    print(res)
    # fout = open('quchu1.png','wb')
    s = cursor.fetchall()
    for pic in s:
        print(type(pic))
        print(len(pic))
        num = random.randint(0,99999)
        name = str(Mission_Id)+'_'+str(num)+'.png'
        pic_ = os.path.join(folder,str(name))
        with open(pic_,'wb') as f:
            f.write(pic[0][1:-1])
    login_out_sql(conn,cursor) 
    print('Total %d pics for Mission %d'%(len(s),int(Mission_Id)))        


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
    print(account)
    conn,cursor = login_sql(account)
    for sql_content in sql_contents:
        print('\n\n\n')
        print(sql_content)
        res = cursor.execute(sql_content)
        response = cursor.fetchall()
        print(response)
    login_out_sql(conn,cursor)

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
    return excels,emails,Missions

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
    print('     Start reading info from sql server...')
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
    return Mission_dict

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

def update_flag_use(id_):
    sql_content = "UPDATE BasicInfo SET flag_use = 0 WHERE BasicInfo_Id = '%s'" % id_
    Execute_sql([sql_content])

def update_flag_use_all():
    sql_content = "UPDATE BasicInfo SET flag_use = 0 "
    Execute_sql([sql_content])

def get_ports_set():
    print('     Start reading info from sql server...')
    account = get_account()
    vc_range = account['vc_range']
    conn,cursor=login_sql(account)
    res = cursor.execute('SELECT * from plans')
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    plans = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    # print(len(Mission_dict))
    # print(Mission_dict)
    # print(plans[0])
    print(len(plans))
    plans = [plan for plan in plans if int(plan['Plan_Id'])>=vc_range[0] and int(plan['Plan_Id'])<=vc_range[1]]
    print(len(plans))    
    ports_set = [plan['port_lpm'] for plan in plans]
    return ports_set    

def get_luminati_submit(Config): 
    Email_list = {"hotmail.com": 1, "outlook.com": 1, "yahoo.com": 1, "aol.com": 1}
    Mission_Ids,Excels_dup = [Config['Mission_Id']],Config['Excel']
    print(Excels_dup)
    submit = read_one_excel(Mission_Ids,Excels_dup,Email_list)
    # print(submit)
    submit['ip_lpm'] = Config['ip_lpm']
    submit['port_lpm'] = Config['port_lpm']
    if Excels_dup[0] == '':
        submit['state_'] = ''
    else:
        submit['state_'] = submit[Excels_dup[0]]['state']
    submit['Mission_Id'] = Config['Mission_Id']
    submit['Country'] = Config['Country']
    submit['Site'] = Config['url_link']
    submit['Excels_dup'] = Excels_dup
    submit['Alliance'] = Config['Alliance']
    submit['Account'] = Config['Account']
    submit['Offer'] = Config['Offer']
    print(submit['Site'])
    submit['Mission_dir'] = Config['Mission_dir']    
    # print(submit)
    uas = Chrome_driver.get_ua_all()
    ua = Chrome_driver.get_ua_random(uas)
    print(ua)  
    submit['ua'] = ua
    return submit

def update_cookie(submit):
    print('Uploading cookie')
    print('Mission_Id:',submit['Mission_Id'])
    print('Email_Id:',submit['Email']['Email_Id'])
    print('Cookie:',submit['Cookie'])
    sql_content = "UPDATE Mission SET Cookie = '%s' WHERE Mission_id = '%s' and Email_Id = '%s'" % (submit['Cookie'],submit['Mission_Id'],submit['Email']['Email_Id'])
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
    sql_content = "SELECT windows,tzid FROM Basicinfo WHERE Excel_name = 'tz' and find_in_set('%s',tzid)"%(tzid)
    account = get_account()
    conn,cursor = login_sql(account)
    res = cursor.execute(sql_content)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    Mission_status_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来    
    login_out_sql(conn,cursor) 
    return Mission_status_dict    

if __name__ == '__main__':
    print('test')
    # try:
    #     init()
    # except:
    #     pass
    # delete_old_data()
    upload_data()
    # get_duplicated_mission_record()
    # plans = {'0': {'Alliance': 'Finaff', 'Offer': 'Royal Cams(Done)', 'url_link': 'http', 'Country': 'US', 'Mission_Id': '10000', 'Excel': ['', 'Email']}}
    # upload_plans(plans)
    # add_key_db()
    # plans = read_plans()
    # print(plans)
    # update_key()
    # hotupdate(5)
