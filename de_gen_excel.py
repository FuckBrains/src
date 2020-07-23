import os
import requests
import re
# import pymysql
import random
import traceback
import uuid
import numpy as np
import xlrd
from xlutils.copy import copy
import sys

def gen_uuid(num):
    uuids = []
    for i in range(num):
        uuid_sin = str(uuid.uuid1())     
        uuids.append(uuid_sin)
    # print(len(uuids))
    # print(len(set(uuids)))
    return uuids

def final_yellow_page(char_num,num_range=1):
    names = []
    url = 'https://www.dasoertliche.de/Personensuche/Nachnamen-%s'%char_num
    # print(url)
    content = pickup(url)
    # print(content)
    if content == '':
        print('Nothing found')
        return
    pattern = r'<li><a href="(https.*?)">(.*?)</a></li'
    names_first = re.findall(pattern,content,re.S)
    names += names_first
    print(len(names),'names find with %s'%char_num)
    pattern = r'<li class="more"><a href="(.*?)">Mehr...</a></li>'
    urls_more = re.findall(pattern,content,re.S)
    for name in urls_more:
        url = 'https://www.dasoertliche.de/Personensuche/'+name    
        print(' ',url)
        content = pickup(url)
        pattern = r'<li><a href="(https.*?)">(.*?)</a></li'
        names_more = re.findall(pattern,content,re.S)
        print(len(names_more),'names find with %s'%name)
        names += names_more
    print('==============================')
    print('==============================')    
    print('Total',len(names),'names find')
    # return
    num = get_modules(char_num)    
    # names = names[num:]
    print('Start from last one: %d of %s'%(num,char_num))
    get_second_page_info(names,char_num,num)

def get_second_page_info(names,char_num,num):
    for i in range(len(names)):
        if num != 0:
            if i <= num:
                continue
        # if i < num_range*20 :
        #     continue
        # if i >(num_range+1)*20:
        #     return
        infos = []
    # for i in range(2):
        # if i <17:
        #     continue
        content = pickup(names[i][0])
        # url_test = 'https://www.dasoertliche.de/Personen/Wolfgang-Bittner'
        # content = pickup(url_test)         
        links_third = get_third_page(content)  
        print('Name %d'%(i+1),':',names[i][1],len(links_third),'urls found in first page')           
        for j in range(100000):
            if 'Seite %s'%str(j+1) in content:
                # print('        Seite %s'%str(j+1))
                continue
            else:
                num_max = j
                break
        if num_max>1:
            links_second_pattern = r'<a href="(https://www\.dasoertliche\.de/\?wntHit.*?)"'
            links_second = re.findall(links_second_pattern,content,re.S)
            # print(links_second)
            for link in links_second:
                content_second = pickup(link)
                links_third_part = get_third_page(content_second)
                print('        ',len(links_third_part),'infos find in next page')
                for link_part in links_third_part:
                    links_third.append(link_part)
        print('        Total %d infos found in %d pages'%(len(links_third),num_max))
        for link_num in range(len(links_third)):
            print('            looking up %dth info'%link_num)
            # name,email,street,building,zipcode,city,state
            decoding='utf-8'
            content = pickup(links_third[link_num],decoding)
            # print(content)
            info = get_third_info(content)
            if len(info) != 0:
                info['name'] = names[i][1]
                infos.append(info)
        save_data(infos,char_num+str(i))
    # upload_infos(infos)

def save_data(content,filename):
    # 保存
    file_dir = r'yellowpage\de\%s.npy'%filename
    # makedir_account(file_dir)
    a = np.array(content)
    np.save(file_dir,a) # 保存为.npy格式

def get_modules(char_num):
    path_de = r'yellowpage\de'
    makedir_account(path_de)
    modules = os.listdir(path_de)
    # print(modules)
    # path = os.path.join(os.getcwd(),path_de)
    # modules_path = [os.path.join(path,file) for file in modules]
    modules_string = [int(file.split('.')[0][1:]) for file in modules if char_num in file]
    if len(modules_string) != 0:
        num = max(modules_string)
    else:
        num = 0
    return num

def makedir_account(path):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)

def read_data(filename):
    file_dir = r'yellowpage\de\%s'%filename    
    a = np.load(file_dir,allow_pickle=True)
    a = a.tolist()        
    # print(a)
    # print(type(a))
    return a

def get_third_info(content=''):
    info = {}

    # address
    pattern = r'class="det_address">(.*?)\&nbsp;(.*?)<br />.*?(\d{5}) (.*?)<a href="'    
    address = re.findall(pattern,content,re.S)
    if len(address) == 0:
        return {}
    address = address[0]        
    info['street'] = address[0].replace('\r','').replace('\t','').replace('\n','').strip()
    info['building'] = address[1]
    info['zipcode'] = address[2]
    info['city'] = address[3]
    # print('    address:',info['street'],info['building'],info['zipcode'],info['city'])

    # phone
    pattern = r'<td class="first">Telefon:</td>.*?<td>.*?<span class=".*?">(.*?)</span></td>'
    phone = re.findall(pattern,content,re.S)
    if len(phone) == 0:
        return {}    
    else:
        phone = phone[0]
        if phone == '':
            return {}
    info['phone'] = phone    
    # print('        phone:',phone)

    # email
    pattern = r'contact_email":  encodeURI\("(.*?)"\)'
    emails = re.findall(pattern,content,re.S)
    if len(emails) == 0:
        email = ''
    else:
        email = emails[0]
    info['email'] = email
    # print('        email:',email)
    return info

def get_third_page(content):
    links_pattern = r'<h2><a href="(.*?)"'
    links_third = re.findall(links_pattern,content,re.S)
    return links_third    

def pickup(url,num=1,decoding=''):
    session = requests.session()
    flag = 0
    for i in range(5):
        try:
            resp=session.get(url,timeout=30)
            # print(resp.text)
            # print(resp.status_code)
            flag = 1
            break
        except Exception as e:
            print(str(e))
            print('try',i,'time')
            pass
    # print(resp.text) 
    session.close()  
    if flag == 1:  
        if decoding != '':
            content = resp.text.encode(resp.encoding).decode(decoding)            
        else:
            content = resp.text    
    else:
        content = ''
    # print(content)    
    return  content

def get_info1(content):
    info = {}
    keys = ['name','products','phone','fax','web_address','create_year','zip_code','address']
    for key in keys:
        info[key] = ''

    # name
    reg_name_pattern = r'<dt><a href=".*?">(.*?)</a></dt>'    
    reg_name = re.findall(reg_name_pattern,content,re.S)
    reg_name = [reg.strip() for reg in reg_name]
    print(reg_name)
    print(len(reg_name))
    if len(reg_name) != 0:
        info['name'] = reg_name[0]

    # products
    reg_name_products_pattern = r'<span>Main Products:</span>(.*?)</dd>'
    reg_name_products = re.findall(reg_name_products_pattern,content,re.S)
    reg_name_products = [reg.strip() for reg in reg_name_products]
    print(reg_name_products)
    print(len(reg_name_products))
    if len(reg_name_products) != 0:
        info['products'] = reg_name_products[0]    

    # phone
    reg_phone_pattern = r'<span>Tel:</span>(.*?)</dd>'    
    reg_phone = re.findall(reg_phone_pattern,content,re.S)
    reg_phone = [reg.strip() for reg in reg_phone]
    print(reg_phone)
    print(len(reg_phone))
    if len(reg_phone) != 0:
        info['phone'] = reg_phone[0]                            
    # fax
    reg_fax_pattern = r'<span>Fax:</span>(.*?)</dd>'
    reg_fax = re.findall(reg_fax_pattern,content,re.S)
    reg_fax = [reg.strip() for reg in reg_fax]
    print(reg_fax)
    print(len(reg_fax))    
    if len(reg_fax) != 0:
        info['fax'] = reg_fax[0]                         

    # web_address
    reg_web_address_pattern = r'<span>Web Address:</span>(.*?)</dd>'
 # www.germany-agents.de&nbsp;&nbsp;                    
    reg_web_address = re.findall(reg_web_address_pattern,content,re.S)
    reg_web_address = [reg.strip().replace('&nbsp;&nbsp','') for reg in reg_web_address]
    print(reg_web_address)
    print(len(reg_web_address))  
    if len(reg_web_address) != 0:
        info['web_address'] = reg_web_address[0]        

    # create_year
    reg_create_year_pattern = r'<span>Create Year:</span>(.*?)</dd>'
    reg_create_year = re.findall(reg_create_year_pattern,content,re.S)
    reg_create_year = [reg.strip() for reg in reg_create_year]
    print(reg_create_year)
    print(len(reg_create_year))   
    if len(reg_create_year) != 0:
        info['create_year'] = reg_create_year[0]          

    # zip_code
    reg_zip_code_pattern = r'<span>ZIP Code:</span>(.*?)</dd>'
    reg_zip_code = re.findall(reg_zip_code_pattern,content,re.S)
    reg_zip_code = [reg.strip() for reg in reg_zip_code]
    print(reg_zip_code)
    print(len(reg_zip_code)) 
    if len(reg_zip_code) != 0:
        info['zip_code'] = reg_zip_code[0]          


    # address
    reg_address_pattern = r'<span>Address:</span>(.*?)</dd>'
    reg_address = re.findall(reg_address_pattern,content,re.S)
    reg_address = [reg.strip() for reg in reg_address]
    print(reg_address)
    print(len(reg_address))  
    if len(reg_address) != 0:
        info['address'] = reg_address[0]     
    return info  

def login_sql(create = False):
    '''
    Login sql and create EMU db if not exist
    choose emu db
    return the cursor and conn
    '''
    ip = '192.168.188.243'
    conn = pymysql.connect(host= ip,port=3306,user='root',passwd=str('root'),charset='utf8mb4',use_unicode=True)
    cursor = conn.cursor()
    try:
        cursor.execute('use %s;'%'emu')
    except:
        pass
    # print('Login db success.')
    # res = cursor.execute('select * from TOKENTABLE;')
    return conn,cursor

def login_out_sql(conn,cursor):
    '''
    commit and close connection
    '''
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

def upload_infos(infos):
    sql_contents = []
    uuids = gen_uuid(len(infos))
    for i in range(len(infos)):
        info = infos[i]
        Basicinfoid = uuids[i]
        # Country = 'DE'
        # Province = info['Province']
        City = info['city']
        Name = info['name']
        Street = info['street']
        Building = info['building']
        Zipcode = info['zipcode']
        Email = info['email']
        Phone = info['phone']        
        # sql_content = (int(Mission_Id),Page,pymysql.escape_string(Flag_xpath),pymysql.escape_string(Flag_text))      
        sql_content = 'INSERT INTO de_basic(Basicinfoid,name,city,phone,street,building,zipcode,email)VALUES("%s","%s","%s","%s","%s","%s","%s","%s")'%(Basicinfoid,Name,City,Phone,Street,Building,Zipcode,Email)
        sql_contents.append(sql_content)
    # sql_content = 'INSERT IGNORE INTO Page_Flag(Mission_Id,Page,Flag_xpath,Flag_text)VALUES("%d","%s","%s","%s")'%(Mission_Id, Page,Flag_xpath,Flag_text)
    Execute_sql(sql_contents)
    return 1

def Execute_sql(sql_contents):

    # print(account)
    conn,cursor = login_sql()
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

def pickup_post(url,data_):
    session = requests.session()
    for i in range(5):
        try:
            resp = session.post(url,data=data_)
            break
        except:
            traceback.print_exc()
            print('try',i,'time')
            pass
    # print(resp.text) 
    session.close()    
    content = resp.text    
    # print(content)    
    return  content 

def main(string):
    # num = [chr(i) for i in range(65,91)]
    # print(num)
    # names = {}
    # for string in num:
        # if string in ['A','B','C','D','E','F','G','H','I','J','K','L']:
        #     continue
        # print('Start from %s'%string)
    final_yellow_page(string)

def upload_data():
    infos = []
    # for item in ['A','B','C','D','E','F','G','H','I','J','K','L']:
    num = [chr(i) for i in range(65,91)]
    print(num)
    names = {}
    for item in num:    
        for i in range(10000):
            try:
                info = read_data(item+str(i))
                infos += info
            except:
                break
    print(len(infos))
    upload_infos(infos)

def write_status(path,workbook,infos_all):
    book2 = copy(workbook)
    sheet2 = book2.get_sheet(0) 
    for i in range(len(infos_all)):
        sheet2.write(i+1,0,infos_all[i]['name'])
        sheet2.write(i+1,1,infos_all[i]['city'])
        sheet2.write(i+1,2,infos_all[i]['street'])
        sheet2.write(i+1,3,infos_all[i]['building'])
        sheet2.write(i+1,4,infos_all[i]['zipcode'])
        sheet2.write(i+1,5,infos_all[i]['phone'])
        sheet2.write(i+1,6,infos_all[i]['email'])
    book2.save(path)

def get_excel(path):
    path_excel = path
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    return sheet,workbook  

def collect():
    path_de = r'yellowpage\de'
    modules = os.listdir(path_de)  
    print(modules)  
    infos_all = []
    for file in modules:
        a = read_data(file)
        infos = []
        phones = []
        for info in a:
            if info['phone'] not in phones:
                phones.append(info['phone'])
                infos.append(info)
        print(len(infos),'unique infos out of %d'%(len(a)))
        infos_all += infos
    print(infos_all)
    print('Total %d unique infos collected'%len(infos_all))
    path_excel = 'de_collect.xlsx'
    sheet,workbook  = get_excel(path_excel)
    write_status(path_excel,workbook,infos_all)


if __name__ == '__main__':
    paras=sys.argv
    i = int(paras[1])  
    try:
        param = paras[2]  
    except:
        pass
    if i == 0:
        print('ready to sort')
        collect()
        print('Sort data finished!!')
    else:
        main(param)