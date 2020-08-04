import json
import os
import requests
import re
# # import pymysql
import random
# import numpy as np
# from numpy import array,load,save
import xlrd,xlwt
from xlutils.copy import copy
import sys

class Collector: 
    def __init__(self,para1=0,para2='A'):
        self.para1 = para1
        self.para2 = para2

    def final_yellow_page(self):
        char_num = self.para2
        names = []
        url = 'https://www.dasoertliche.de/Personensuche/Nachnamen-%s'%char_num
        # print(url)
        content = self.pickup(url)
        
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
            content = self.pickup(url)
            pattern = r'<li><a href="(https.*?)">(.*?)</a></li'
            names_more = re.findall(pattern,content,re.S)
            print(len(names_more),'names find with %s'%name)
            names += names_more
        print('==============================')
        print('==============================')    
        print('Total',len(names),'names find')
        # return
        num = self.get_modules(char_num)    
        # names = names[num:]
        print('Start from last one: %d of %s'%(num,char_num))
        self.get_second_page_info(names,char_num,num)
    
    def get_second_page_info(self,names,char_num,num):
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
            content = self.pickup(names[i][0])
            
            # url_test = 'https://www.dasoertliche.de/Personen/Wolfgang-Bittner'
            # content = pickup(url_test)         
            links_third = self.get_third_page(content)  
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
                    content_second = self.pickup(link)
                    
                    links_third_part = self.get_third_page(content_second)
                    print('        ',len(links_third_part),'infos find in next page')
                    for link_part in links_third_part:
                        links_third.append(link_part)
            print('        Total %d infos found in %d pages'%(len(links_third),num_max))
            for link_num in range(len(links_third)):
                print('            looking up %dth info'%link_num)
                # name,email,street,building,zipcode,city,state
                decoding='utf-8'
                content = self.pickup(links_third[link_num],decoding=decoding)
                
                # print(content)
                info = self.get_third_info(content)
                if len(info) != 0:
                    info['name'] = names[i][1]
                    infos.append(info)
            self.save_data(infos,char_num+str(i))
        # upload_infos(infos)
    
    def save_data(self,content,filename):
        # 保存
        file_dir = r'yellowpage\de\%s.npy'%filename
        # makedir_account(file_dir)
        with open(file_dir,'w') as f:
            for info in content:
                item = json.dumps(info)
                f.write(item)
                f.write('\n')                
        # a = array(content)
        # save(file_dir,a) # 保存为.npy格式
    
    def get_modules(self,char_num):
        path_de = r'yellowpage\de'
        self.makedir_account(path_de)
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
    
    def makedir_account(self,path):
        isExists=os.path.exists(path)
        if isExists:
            return
        else:
            os.makedirs(path)
    
    def read_data(self,filename):
        infos = []
        file_dir = r'yellowpage\de\%s'%filename    
        with open(file_dir,'r') as f:
            lines = f.readlines()
        for line in lines:
            if line=='\n':
                continue
            info = json.loads(line)
            infos.append(info)
        print(infos)
        return infos
    
    def get_third_info(self,content=''):
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
    
    def get_third_page(self,content):
        links_pattern = r'<h2><a href="(.*?)"'
        links_third = re.findall(links_pattern,content,re.S)
        return links_third    
    
    def pickup(self,url,num=1,decoding=''):
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
    
    def pickup_post(self,url,data_):
        session = requests.session()
        for i in range(5):
            try:
                resp = session.post(url,data=data_)
                break
            except:
                # traceback.print_exc()
                print('try',i,'time')
                pass
        # print(resp.text) 
        session.close()    
        content = resp.text    
        # print(content)    
        return  content 
    
    def write_status(self,infos_all,on=0):
        print(infos_all)
        book2 = copy(self.workbook)
        sheet2 = book2.get_sheet(0) 
        if on != 0:
            row = self.sheet.nrows
        else:
            row = 0
        for i in range(len(infos_all)):
            sheet2.write(row+i,0,infos_all[i]['name'])
            sheet2.write(row+i,1,infos_all[i]['city'])
            sheet2.write(row+i,2,infos_all[i]['street'])
            sheet2.write(row+i,3,infos_all[i]['building'])
            sheet2.write(row+i,4,infos_all[i]['zipcode'])
            sheet2.write(row+i,5,infos_all[i]['phone'])
            sheet2.write(row+i,6,infos_all[i]['email'])
        book2.save(self.path_excel)
    
    def get_excel(self):
        try:
            for i in range(1000):            
                self.workbook = xlrd.open_workbook(self.path_excel)
                self.sheet = self.workbook.sheet_by_index(0)
                self.nrow = self.sheet.nrows
                if self.nrow<=50000:
                    break                  
                self.path_excel = 'de_collect%d.xlsx'%i
        except:
            print('data too big for excel,gen a new one')
            """创建一个excel对象"""
            self.workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
            """创建sheet"""
            self.sheet = self.workbook.add_sheet('test',cell_overwrite_ok=True)            
            self.sheet.write(0,0,'name')
            self.sheet.write(0,1,'city')
            self.sheet.write(0,2,'street')
            self.sheet.write(0,3,'building')
            self.sheet.write(0,4,'zipcode')
            self.sheet.write(0,5,'phone')
            self.sheet.write(0,6,'email')
            self.workbook.save(self.path_excel)
            self.workbook = xlrd.open_workbook(self.path_excel)
            self.sheet = self.workbook.sheet_by_index(0)        

    def clean_excel(self): 
        book2 = copy(self.workbook)
        sheet2 = book2.get_sheet(0) 
        row = 0
        nrow = self.sheet.nrows
        for i in range(nrow):
            sheet2.write(row+i+1,0,'')
            sheet2.write(row+i+1,1,'')
            sheet2.write(row+i+1,2,'')
            sheet2.write(row+i+1,3,'')
            sheet2.write(row+i+1,4,'')
            sheet2.write(row+i+1,5,'')
            sheet2.write(row+i+1,6,'')
        book2.save(self.path_excel)        
    
    def collect(self):
        path_de = r'yellowpage\de'
        modules = os.listdir(path_de)  
        print(modules)  
        infos_all = []

        # self.clean_excel()
        try:
            modules_exist = []
            with open('yellowpage\history.txt','r') as f:
                lines = f.readlines()
            for line in lines:
                file_see = line.replace('\n','')
                if file_see != '':
                    modules_exist.append(file_see)
        except:
            with open('yellowpage\history.txt','w') as f:
                f.write('')
        files = []
        self.path_excel = 'de_collect0.xlsx'
        for file in modules:
            if file in modules_exist:
                continue
            files.append(file)
            a = self.read_data(file)
            infos = []
            phones = []
            for info in a:
                if info['phone'] not in phones:
                    phones.append(info['phone'])
                    infos.append(info)
            print(len(infos),'unique infos out of %d'%(len(a)))
            infos_all += infos
            if len(infos_all)>= 1000:
        # print(infos_all)
        # print('Total %d unique infos collected'%len(infos_all))
                self.get_excel()
                on = 1
                self.write_status(infos_all,on)
                infos_all = []
                with open('yellowpage\history.txt','a') as f:
                    content = ''
                    for file_ in files:
                        content += file_+'\n'
                    f.write(content)   
        with open('yellowpage\history.txt','a') as f:
            content = ''
            for file_ in files:
                content += file_+'\n'
            f.write(content)                           
        self.get_excel()
        on = 1
        self.write_status(infos_all,on)                


def test():
    collector = Collector(1,'A')
    content = []
    for i in range(10):
        info = {}
        info['phone'] = '1234'+str(i)
        info['name'] = 'asdasd'
        info['email'] = 'asdasdasdasd@asdd.com'
        content.append(info)
    filename = 'A1'
    collector.save_data(content,filename)    


def test2():
    collector = Collector(1,'A')    
    filename = 'A1'
    collector.read_data(filename)    



if __name__ == '__main__':
    test2()
#     paras=sys.argv
#     i = int(paras[1])  
#     try:
#         param = paras[2]  
#     except:
#         pass
#     if i == 0:
#         print('ready to sort')
#         collect()
#         print('Sort data finished!!')
#     else:
#         main(param)