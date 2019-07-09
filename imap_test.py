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



def Email_emu_getlink(account,keyword = ''):
    # PwolxuYjthksa@outlook.com----1o61vdu545QR 
    if 'outlook' in account['Email_emu']:
        server = "imap-mail.outlook.com"
    elif 'aol' in account['Email_emu']:
        server = 'imap.aol.com'
    elif 'hotmail' in account['Email_emu']:
        server = "imap-mail.outlook.com"
    elif 'yahoo' in  account['Email_emu']:
        server = 'imap.mail.yahoo.com'
    else:
        writelog('bad Email_emu')
        return ''  
    try:             
        M = imaplib.IMAP4_SSL(server)
    except Exception as msg:
        writelog(account['Email_emu'] + ' login failed : ',str(msg))
        return 0        
    msg_content = ''    
    try:
        M.login(account['Email_emu'],account['Email_emu_pwd'])
        # print([str(x,'gb2312') for x in  M.list()])
        # print(M.list())
        a,b = M.list()
        # print(b)
        print('login success')
        return 1
    except Exception as e:
        print('login error: %s'%e)
        # M.close()
        return 0


if __name__=='__main__':
    path = 'Email_emu_all.xlsx'
    path_excel = path
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    rows = sheet.nrows    
    for i in range(rows-1):
        if i >= 0:
            test_Mail(i+1,path)   
