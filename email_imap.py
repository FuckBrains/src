import imaplib, string, email
import re
from email.parser import Parser
import quopri
import os
import time
import base64



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



if __name__=='__main__':
    submit={}
    submit['ua'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    submit['name'] = 'Mondde522'
    submit['pwd'] = r'lzbA#7o^uj'
    submit['Email_emu'] = 'KingDavidgHvUu@yahoo.com'
    # 'KarolWhiteyf@aol.com' 
    submit['Email_emu_pwd'] = 'lBI8356I4'
    # 'Gcih4QpP'  
    submit['city'] = 'Bochum'
    # RobillardNyieshalJD@yahoo.com   jZbR8r31q
# EthelMoore3y@aol.com    oweR0tkk

# LlwthdKlhcvr@hotmail.com----glL9jPND4nDp    
    # site='http://www.baidu.com'
    # web_Submit(submit)
    msg = Email_emu_getlink(submit,'E-Certificate',2)
    print(msg)
    num_confirm(msg)
    # base64.b64decode(msg)



             

         


