import imaplib, string, email
import re
from email.parser import Parser
import quopri
import os
import time
import base64
import db
from time import sleep
import threading
import threadpool


pool = threadpool.ThreadPool(100)
Falg_threads = 0

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
    flag = 0
    if submit['Status'] == 'Bad':
        return
    if 'outlook' in submit['Email_emu']:
        server = "imap-mail.outlook.com"
    elif 'aol' in submit['Email_emu']:
        server = 'imap.aol.com'
    elif 'hotmail' in submit['Email_emu']:
        server = "imap-mail.outlook.com"
    elif 'yahoo' in  submit['Email_emu']:
        server = 'imap.mail.yahoo.com'
    else:
        # writelog('bad Email_emu')
        return 'bad Email_emu' 
    try:
        box = imaplib.IMAP4_SSL(server)  
    except:
        flag = 0
        return flag
    try:  
        box.login(submit['Email_emu'], submit['Email_emu_pwd'])
    except Exception as e:
        print(str(e))
        flag = 1
        return flag
    for item in box.list()[1]:
        # print()
        box_selector = item.decode().split(' \"/\" ')[-1]
        if  re.match(r'.*?(Sent|Delete|Trash|Draft).*?',box_selector,re.M|re.I):
            continue
        # print(box_selector)    
        box.select(box_selector)
        # 如果是查找收件箱所有邮件则是box.search(None, 'ALL')
        # typ, data = box.search(None, 'from', 'mailer-daemon@googlemail.com')
        typ, data = box.search(None, 'ALL') 
        # print(data[0].split())        
        while True:
            for num in data[0].split():
                # print(num)  
                try:
                    box.store(num, '+FLAGS', '\\Deleted')
                except:
                    pass
            box.expunge()
            sleep(3)
            typ, data = box.search(None, 'ALL') 
            # print(data[0].split())            
            if len(data[0].split()) == 0:
                break
    print(submit['Email_emu'],'clean finished!')
    flag = 2
    box.close()
    box.logout() 
    return flag   

def multi_delete_email(submit):
    global Falg_threads
    Falg_threads += 1
    flag = 2
    try:
        flag=clean_email(submit)
        print(Falg_threads,'------->',submit['Email_emu'],'----->',flag)
        if flag == 1:
            try:
                db.updata_email_status(submit['Email_Id'],0)
                print('Status uploaded success:Bad email')
            except Exception as e:
                print(str(e))
        elif flag == 2:
            db.updata_email_status(submit['Email_Id'],1)
            print('Status uploaded success:Good email')            
        else:
            pass        
    except:
        pass


def main():
    submits = db.email_test()
    print('Total:',len(submits))
    requests = threadpool.makeRequests(multi_delete_email, submits)
    [pool.putRequest(req) for req in requests]
    pool.wait() 




if __name__=='__main__':
    main()



             

         


