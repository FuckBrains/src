
import requests
import re
import pymysql
import random
import traceback
import uuid
import numpy as np


def gen_uuid(num):
    uuids = []
    for i in range(num):
        uuid_sin = str(uuid.uuid1())     
        uuids.append(uuid_sin)
    # print(len(uuids))
    # print(len(set(uuids)))
    return uuids

def final_yellow_page(char_num,num_range=1):
    url = 'https://www.dasoertliche.de/Personensuche/Nachnamen-%s'%char_num
    print(url)
    content = pickup(url)
    # print(content)
    if content == '':
        print('Nothing found')
        return
    pattern = r'<li><a href="(https.*?)">(.*?)</a></li'
    names = re.findall(pattern,content,re.S)
    print(len(names),'names find with %s'%char_num)
    for i in range(len(names)):
        if i < num_range*20 :
            continue
        if i >(num_range+1)*20:
            return
        infos = []
    # for i in range(2):
        # if i <17:
        #     continue
        content = pickup(names[i][0])
        # url_test = 'https://www.dasoertliche.de/Personen/Wolfgang-Bittner'
        # content = pickup(url_test)         
        links_third = get_third_page(content)  
        print('Name %d'%(i+1),':',names[i][1],len(links_third),'urls found in first page')           
        for j in range(10000):
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
    file_dir = r'..\yellowpage\de\%s.npy'%filename
    a = np.array(content)
    np.save(file_dir,a) # 保存为.npy格式

def read_data(filename):
    file_dir = r'..\yellowpage\de\%s.npy'%filename    
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
            # print(resp.encoding)
            flag = 1
            break
        except:
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
 # www.germany-agents.de&nbsp;&nbsp;                    
    # reg_contents_pattern = r'<dl>(.*?)</dl>'
    # reg_contents= re.findall(reg_contents_pattern,content,re.S)
    # reg_contents = [reg.strip() for reg in reg_contents]
    # if num == 1:
    #     reg_url_pattern = r'<dt><a href="(.*?)"'
    #     reg_url= re.findall(reg_url_pattern,content,re.S)
    #     reg_url = [reg.strip() for reg in reg_url]
    #     # print(reg_url)
    #     # print(len(reg_url))
    #     infos = []
    #     if len(reg_url) == 0:
    #         return -1
    #     print('Total %d urls found'%len(reg_url))
    #     for url in reg_url:
    #         info = pickup(url,2)
    #         print(' '*4,info)
    #         infos.append(info)
    #     upload_infos(infos)
    # else:
    #     info = get_info_2(content)
    #     return info

def get_info_2(content):
    # print(content)
    info = {}
    keys = ['Year_Established','Contact','Telphone','Fax','MobilePhone','Web_Site','Zip','Province','City','Address']
    reg_patterns = [r'Year Established:</td><td><a href=".*?">(.*?)</a></td>',r'Contact:</td><td>(.*?)</td>',r'Telphone:</td><td>(.*?)</td>',r'Fax</td><td>(.*?)</td>',r'MobilePhone:</td><td>(.*?)</td>',r'Web Site:</td><td><a href=".*?_blank>(.*?)</a>',r'Zip:</td><td><a href=".*?">(.*?)</a></td>',r'Province/State:</td><td><a href=".*?">(.*?)</a>',r'City:</td><td><a href=".*?">(.*?)</a>', r'Address:</td><td>(.*?)</td>']  
    for i in range(len(keys)):
        info[keys[i]] = ''
        values = re.findall(reg_patterns[i],content,re.S)
        if len(values) != 0:
            info[keys[i]] = values[0].replace('&nbsp; &nbsp;','').strip()
    return info

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
    
def get_city():
    citys = []
    pattern = r'([\u0020-\u007e\u00a0-\u00ff\u0100-\u017F]+)'
    with open('citys_de.txt',encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        city = re.findall(pattern,line)
        # print(city)
        num = re.findall('\d+',city[0])
        if len(num) == 0:
            if city[0] != '-':
                city_clean = city[0]
            else:
                city_clean = city[1]
            a = city_clean.find('(')
            if a != -1:
                city_clean = city_clean[:a]
            if city_clean.strip()=='':
                continue
            citys.append(city_clean)                
        else:
            print(num)
    citys.append('Freiberg')
    print(len(citys))
    # print(citys)
    return citys

def account_gen():
    result = []
    for i in range(0, 10):
        result.append(random.choice('1234567890'))
    random.shuffle(result)
    account = "".join(result)
    return account

def blz_choose():
    blzs = ['66020500','37020500','10020500','85020500','70020500','20020500','50020500','55020500','57020500','67020500','81020500','86020500']    
    num = random.randint(0,8)
    return blzs[num]

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

def get_info(content):
    info = {}
    # iban
    reg_pattern = r'">IBAN: (.*?)</span>'
    iban = re.findall(reg_pattern,content,re.S)
    if len(iban)==0:
        print(content) 
        return None
    iban = [reg.strip() for reg in iban][0]    
    # bic
    reg_pattern = r"copyBicBtn.addEventListener\(\'click\',function\(event\){copyTextToClipboard\(\'(.*?)\'\)"    
    bic = re.findall(reg_pattern,content,re.S)
    bic = [reg.strip() for reg in bic][0]      
    # bank
    reg_pattern = r'<b>Bank:</b>(.*?)</p>'
    bank = re.findall(reg_pattern,content,re.S)
    bank = [reg.strip() for reg in bank][0] 
    info['Bank'] = bank
    info['Iban'] = iban
    info['Bic'] = bic
    return info     

def get_bank_info():
    blz = blz_choose()
    account = account_gen()
    data = {
        'tx_intiban_pi1[country]': 'DE',
        'tx_intiban_pi1[blz]': str(blz),
        'tx_intiban_pi1[kontonr]': str(account),
        'tx_intiban_pi1[fi]': 'fi',
        'no_cache': '1',
        'tx_intiban_pi1[a]': 'Calculate IBAN'
    }
    url = 'https://www.ibancalculator.com/bic_und_iban.html'
    content = pickup_post(url,data)
    # print(content)
    info = get_info(content)
    info['BLZ'] = blz
    info['Account'] = account
    print(info)

def get_whole_info(content):
    info = {}
    # dateofbirth
    pattern = r'<th width="30%">Geburtsdatum</th>.*?<td>(.*?)</td>'
    dateofbirth = re.findall(pattern,content,re.S)    

    # id number
    pattern = r'Ausweisnummer</th>.*?<td style="max-width:50px; word-wrap:break-word;">(.*?)</td>'
    id_number = re.findall(pattern,content,re.S)    

    # expeire
    pattern = r'<th width="30%">Ablaufdatum</th>.*?<td>(.*?)</td>'
    expeire = re.findall(pattern,content,re.S)    
    info['dateofbirth'] = dateofbirth[0].replace('/','.')
    info['id_number'] = id_number[0].replace('&lt;','<').replace('\n','')
    info['expeire'] = expeire[0].replace('/','.')
    return info

def pwd():
    result = []
    length = random.randint(9,15)
    for i in range(0, length):
      if i % 4 == 0:
          result.append(random.choice('1234567890'))
      if i % 4 == 1:
          result.append(random.choice('abcdefghijklmnisabella.wiedemann1997@outlook.deopqrstuvwxyz'))
      if i % 4 == 2:
          result.append(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
      if i % 4 == 3:
          result.append(random.choice('!$%()+,-.:;>?@[]`{}'))
    random.shuffle(result)
    pwd = "".join(result)
    return pwd

def get_idcard():
    url = 'https://identinator.com/'
    content = pickup(url)
    # print(content)
    pattern = r'col-md-6(.*?)Exp</th>'
    cards = re.findall(pattern,content,re.S)
    print(len(cards),'cards find.')
    # print(card[0])
    infos = []
    for card in cards:
        info = get_whole_info(card)
        print(info['dateofbirth'])
        year = int((info['dateofbirth']).split('.')[2])
        if year<1995:
            continue
        else:
            infos.append(info)
    if len(infos) != 0:
        for info in infos:
            print(info)
    # bank = [reg.strip() for reg in card][0]     
    # print(bank)
    # Ausweisnummer</th>.*?<td style="max-width:50px; word-wrap:break-word;">(.*?)</td>
    #             </tr>
    #             <tr>
    #                 <th width="30%">Ablaufdatum</th>
    #                 <td>04/09/2024</td>

    #                 <th width="30%">Geburtsdatum</th>
    #                 <td>04/09/1991</td>                    

def test():
    # content = ['asdasdas',{'a':123,'b':213},{'c':123,'d':213}]
    # filename = '1'
    # save_data(content,filename)
    read_data('A1')

def main_yellowpage():
    '''
    '''
    url = 'https://www.dastelefonbuch.de/Personen/%s/%s'%('Schulz','Berlin')
    url_real = r'https://adresse.dastelefonbuch.de/Berlin/1-Krankenh%C3%A4user-Hospiz-und-PalliativVerband-Berlin-e-V-HOSPIZDIENSTE-Berlin-Brabanter-Str.html'
    content = pickup(url_real)
    # print(content)
    get_white_page_info(content)

    return
    num = [chr(i) for i in range(65, 91)]
    print(num)
    names = {}
    for string in num:
        print('collecting names start from',string)
        url = 'https://personensuche.dastelefonbuch.de/Nachnamen-%s'%string
        content = pickup(url)
        # print(content)
        reg_contents_pattern = r'<li><a href="https://personensuche\.dastelefonbuch\.de/Nachnamen/.*?" title=".*?">(.*?)</a></li>'
        reg_contents= re.findall(reg_contents_pattern,content,re.S)
        reg_contents = [reg.strip() for reg in reg_contents]           
        print(len(reg_contents),'names found in %s'%string)
        names[string] = reg_contents
        break
    [print(key,len(names[key])) for key in names]
    citys = get_city()
    for city in citys:
        # identinator
        # url = 'https://identinator.com/'
        # url = 'http://www.business-yellowpages.com/details/579730/germany/Kyopo-Shinmun'
        content = pickup(url)
        print(content)
        return
        if flag == -1:
            break

def main(num_range):
    num = [chr(i) for i in range(65,91)]
    print(num)
    names = {}
    for string in num:
        # if string in ['A','B','C','D','E','F','G','H','I','J','K','L']:
        #     continue
        print('Start from %s'%string)
        final_yellow_page(string,num_range)

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

def get_city(zipcode):
    url = 'https://www.nowmsg.com/findzip/de_postalcode.asp?CityName=%s'%str(zipcode)
    try:
        content = pickup(url,decoding='utf-8')
    except:
        content = ''
    # print(content)
    return content

def test():
    info = read_data('A10000')
    print(info)

if __name__ == '__main__':
    import sys
    paras=sys.argv
    i = int(paras[1])
    # main(i)
    if i != 0:
        main(i)
    else:
        upload_data()
    # test()