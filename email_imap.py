import imaplib, string, email
import re
from email.parser import Parser
import quopri
import os
import time
import base64
import db
from time import sleep



def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()




def email_getlink(account,keyword = '',Num_Email_emu = 1):
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
        return 'bad Email_emu' 
    try:              
        M = imaplib.IMAP4_SSL(server)
    except Exception as msg:
        writelog(account['Email_emu'] + ' login failed : ',str(msg))
        return 'bad Email_emu'
    msg_content = []    
    try:
        try:
            M.login(account['Email_emu'],account['Email_emu_pwd'])
            # print([str(x,'gb2312') for x in  M.list()])
            # print(M.list())
            a,b = M.list()
            # print(b)
            print(account['Email_emu'],'login success')
        except Exception as e:
            print('login error: %s'%e)
            # M.close()
            return 'bad Email_emu'
        # M.select_folder('Junk', readonly = True)             
        # M.select()
        # result, message = M.select('"{}"'.format("Junk"))
        result, message = M.select('"{}"'.format("Bulk Mail"))
        print(result)
        if result == 'NO':
            result, message = M.select('"{}"'.format("Junk"))
            print(message)
        # print(M.check())
        typ, data = M.search(None,'ALL')
        # print(data)
        data = [str(datas,'gbk','ignore') for datas in data]
        # print(data[0].split())
        for num in data[0].split():
        # print(data[0].split()[-1])
            try:
                typ, data1 = M.fetch(num, '(RFC822)')
                # print(data1)
                msg_content1 = data1[0][1]
                msg_content1 = quopri.decodestring(msg_content1)
                if keyword in str(msg_content1,'gbk','ignore'):
                    msg_content.append(str(msg_content1,'gbk','ignore'))
                    if  Num_Email_emu == 1:
                        print('find target Email_emu')
                        M.close()
                        M.logout()                
                        return msg_content[0]
                    else:
                        pass
                        # msg_content += str(msg_content1,'gbk','ignore')
            except Exception as e:
                print('got msg error: %s' % e) 
                M.close()
                M.logout()                
                return ''                   
        result, message = M.select()
        print(message)
        # print(M.check())
        typ, data = M.search(None,'ALL')
        # print(data)
        data = [str(datas,'gbk','ignore') for datas in data]
        # print(data[0].split())
        for num in data[0].split():
            try:
                typ, data1 = M.fetch(num, '(RFC822)')
                msg_content1 = data1[0][1]
                msg_content1 = quopri.decodestring(msg_content1)
                if keyword in str(msg_content1,'gbk','ignore'):
                    msg_content.append(str(msg_content1,'gbk','ignore'))
                    if  Num_Email_emu == 1:
                        print('find target Email_emu in Junk Email_emu')
                        M.close()
                        M.logout()                
                        return msg_content[0]
                    else:
                        pass
                        # msg_content += str(msg_content1,'gbk','ignore')
            except Exception as e:
                print('got msg error: %s' % e) 
                M.close()
                M.logout()                
                return ''                   
        M.close()
        M.logout()
        if Num_Email_emu == 1:
            return ''
        else:
            return msg_content
    except Exception as  e:
        print('imap error: %s' % e)
        M.logout()
        M.close()
        return ''

def num_confirm(res):
    num = res.count('Subject: Order Confirmation from LifePoints')
    print(num)

def clean_email(submit):
    if 'outlook' in submit['Email_emu']:
        server = "imap-mail.outlook.com"
    elif 'aol' in submit['Email_emu']:
        server = 'imap.aol.com'
    elif 'hotmail' in submit['Email_emu']:
        server = "imap-mail.outlook.com"
    elif 'yahoo' in  submit['Email_emu']:
        server = 'imap.mail.yahoo.com'
    else:
        writelog('bad Email_emu')
        return 'bad Email_emu' 
    box = imaplib.IMAP4_SSL(server)    
    box.login(submit['Email_emu'], submit['Email_emu_pwd'])
    for item in box.list()[1]:
        print()
        box_selector = item.decode().split(' \"/\" ')[-1]
        if  re.match(r'.*?(Sent|Delete|Trash|Draft).*?',box_selector,re.M|re.I):
            continue
        print(box_selector)    
        box.select(box_selector)
        # 如果是查找收件箱所有邮件则是box.search(None, 'ALL')
        # typ, data = box.search(None, 'from', 'mailer-daemon@googlemail.com')
        typ, data = box.search(None, 'ALL') 
        print(data[0].split())        
        while True:
            for num in data[0].split():
                print(num)  
                try:
                    box.store(num, '+FLAGS', '\\Deleted')
                except:
                    pass
            box.expunge()
            sleep(3)
            typ, data = box.search(None, 'ALL') 
            print(data[0].split())            
            if len(data[0].split()) == 0:
                break
    box.close()
    box.logout()    


if __name__=='__main__':
    Country ='US'
    Mission_list = ['10004']
    Email_list = ['hotmail','aol.com','yahoo.com','outlook.com']
    Excel_names = ['Auto','Usloan']
    submit = db.read_one_info(Country,Mission_list,Email_list,Excel_names)
    # print(submit['Email'])
    # submit = {}
    # submit['Email'] = {'Email_Id': '6f760998-aa34-11e9-8125-0003b7e49bfc', 'Email_emu': 'RichBrooksKP@aol.com', 'Email_emu_pwd': 'fsT1Ngq2', 'Email_assist': '', 'Email_assist_pwd': '', 'Status': None}
    clean_email(submit['Email'])
    # email_getlink(submit['Email'])




             

         


