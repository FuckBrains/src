from wrapt_timeout_decorator import *
import xlrd
from xlutils.copy import copy
from time import sleep
import sys
# sys.path.append("../..")
import os
import time
import json
from urllib import request, parse
import psutil
# from modules_add.Allin_config import Cam4_allin
# from modules_add.Cam4 import Cam4_reg
import poplib
import imaplib, string, email
import re
import threading
import threadpool


pool = threadpool.ThreadPool(30)


def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log_mylocalflirt.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()


def submit_Dict(submit1):
    submit = {}
    submit['pwd'] = submit1[1]
    submit['Email_emu'] = submit1[2]
    submit['Email_emu_pwd'] = submit1[3]
    submit['Email_emu_assist'] = submit1[4]
    submit['ua'] = submit1[5]
    submit['status'] = submit1[6]
    submit['city'] = submit1[7]
    return submit


def test_Mail(i, path):       
    path_excel = path
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    rows = sheet.nrows
    # print(rows)
    # list_rows = random.sample(range(rows),rows)    
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    book2 = copy(workbook)
    sheet2 = book2.get_sheet(0)   
        # if i <= 303:
        #     continue
    if i == 0:
        pass    
    submit1 = sheet.row_values(i)
    try:
        submit = submit_Dict(submit1)
        # print(submit)
    except Exception as msg:
        # writelog('submit get wrong',msg)
        print('submit get wrong') 
    stat = Email_emu_getlink(submit) 
    if stat == 1:
        sheet2.write(i,6,'Email_emu login success')
        print('Num '+str(i)+' login success')
        book2.save(path)
        return 1
    else:
        sheet2.write(i,0,'bad Email_emu')
        sheet2.write(i,6,'login fail')
        print('Num '+str(i)+' login failed')
        book2.save(path)
        return 0       





def login_server(submit):
    print(submit['Email_emu'])
    if 'outlook' in submit['Email_emu']:
        server = "imap-mail.outlook.com"
    elif 'aol' in submit['Email_emu']:
        server = 'imap.aol.com'
    elif 'hotmail' in submit['Email_emu']:
        server = "imap-mail.outlook.com"
    elif 'yahoo' in  submit['Email_emu']:
        server = 'imap.mail.yahoo.com'
    elif 'gmx' in  submit['Email_emu']:
        server = 'imap.gmx.com'        
    else:
        print('bad Email_emu')
        return ''  
    print(server)
    print('Logging IMAP4_SSL')
    box = imaplib.IMAP4_SSL(server)
    return box    

@timeout(30)
def Email_emu_getlink(submit,keyword = ''):
    # PwolxuYjthksa@outlook.com----1o61vdu545QR 
    # try:
    box = login_server(submit)
    # except Exception as e:
        # print('====================')
        # print(str(e))
        # print('logging email server failed')
        # return -1
    print('email server login success....')
    msg_content = ''    
    try:
        box.login(submit['Email_emu'], submit['Email_emu_pwd'])
        print(submit['Email_emu'],'login success.....')
        print(box.list())
        # for item in box.list()[1]:
        #     print(item)
        #     box_selector = item.decode().split(' \"/\" ')[-1]
        #     if  re.match(r'.*?(Sent|Delete|Trash|Draft).*?',box_selector,re.M|re.I):
        #         continue
        #     print(box_selector)    
        #     box.select(box_selector)
        #     # 如果是查找收件箱所有邮件则是box.search(None, 'ALL')
        #     typ, data = box.search(None, 'from', 'mailer-daemon@googlemail.com')
        #     typ, data = box.search(None, 'ALL') 
        #     print(data[0].split())        
        #     while True:
        #         i = 0
        #         for num in data[0].split():
        #             if i >=1:
        #                 break
        #             print(num)  
        #             try:
        #                 box.store(num, '+FLAGS', '\\Deleted')
        #             except:
        #                 pass
        #             i += 1
        #         box.expunge()
        #         sleep(3)
        #         typ, data = box.search(None, 'ALL') 
        #         print(data[0].split())            
        #         if len(data[0].split()) == 0:
        #             break
        box.select("INBOX")
        box.close()        
        print('Email good')
        box.logout()  
        print('Logging out imap server success')        
        return 1
    except Exception as e:
        print('login error: %s'%e)
        try:
            box.select("INBOX")
            box.close()
            box.logout()
            print('Logging out imap server success')
        except Exception as e:
            print(str(e))
        return 0


def multi_tests(submit):
    import db
    flag = Email_emu_getlink(submit)
    print('finish loop......')
    if flag == 0:
        print('Bad email:',submit['Email_emu'])
        db.updata_email_status(submit['Email_Id'],0)
    else:
        print("Good email")
        db.updata_email_status(submit['Email_Id'],1)        


def test_1():
    import db
    emails = db.get_all_emails()
    # print(emails[0])
    emails = [email for email in emails if 'hotmail' in email['Email_emu']]
    # print(emails[1])
    # multi_tests(emails[1])
    submits = []
    for i in range(30):
        print(i,'..........')
        Mission_list = ['10000']
        Excel_name = ['','Email']
        Email_list = ['hotmail.com']
        submit = db.read_one_excel(Mission_list,Excel_name,Email_list)
        submits.append(submit)
    print(len(emails))
    # return
    requests = threadpool.makeRequests(multi_tests, emails)
    [pool.putRequest(req) for req in requests]
    pool.wait()     
    # submit = {}
    # submit= {
    # 'Email_Id': '2ee711fa-d9ed-11e9-b05e-000ae8256789', 
    # 'Email_emu': 'WestecbbmkOljhsfrq@hotmail.com', 
    # 'Email_emu_pwd': 'v3gZUnl72i'
    # }   
    # multi_tests(submit)     
        # print(submit)    

def get_account():
    '''
    get account for sql db,read a config file in res folder
    eg:submit = {'password':...}
    requies nothing
    return the sql db account
    '''
    file = r'..\res\gmx.txt' 
    submits = []
    with open(file,'r') as f:
        lines = f.readlines()
        for line in lines:
            

        

def main():
    emails = get_account()


if __name__=='__main__':
    main()
