import imaplib, email,os,re
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin

from emailServer import EmailService

class EmailReceive(object):
    def __init__(self,emailAddress,authorityCode):
        self.imap_mail = None
        self.__login(emailAddress,authorityCode)

    def __login(self,address,password):
        try:
            serverInfo=EmailService.getIMAPServer(address.split('@')[-1].split('.')[0])
            if serverInfo[2]:
                self.imap_mail = imaplib.IMAP4_SSL(serverInfo[0],serverInfo[1])
            else:
                self.imap_mail = imaplib.IMAP4(serverInfo[0], serverInfo[1])
            self.imap_mail.login(address,password)
        except Exception as e:
            print(e)

    def close(self):
        self.imap_mail.close()
        self.imap_mail.logout()

    def getEmail(self,keyword=None,onlyUnsee=True,findAll=False,getAttach=False):
        result=[]
        try:
            self.imap_mail.select()
        except Exception as e:
            print(e)
            return result
        num_c=0
        # print(self.imap_mail.list()[1])
        for item in self.imap_mail.list()[1]:
            box = item.decode().split(' \"/\" ')[-1]
            if  re.match(r'.*?(Sent|Delete|Trash|Draft).*?',box,re.M|re.I):
                continue
            print(box)
            try:
                # print(num_c)
                if num_c != 0:
                    self.imap_mail.select(box)
                num_c += 1
                if onlyUnsee:
                    try:
                        state, en = self.imap_mail.search(None, 'UNSEE')
                    except Exception as e:
                        print(e)
                        state, en = self.imap_mail.search(None, 'ALL')
                else:
                    state, en = self.imap_mail.search(None,'ALL')
                print(state,en)
                # print('en',str(en))
                for num in en[0].split()[::-1]:
                    typ, data = self.imap_mail.fetch(num, '(RFC822)')
                    # print('data',data)
                    header = EmailReceive.getMailHeader(data)
                    print('header',str(header))
                    if header is None:
                        continue
                    if keyword is None:
                        result.append(EmailReceive.getOneMail(data, getAttach))
                    else:
                        flag_ = 0
                        for keyItem in keyword:
                            if keyItem in header[0] or keyItem in header[1] or keyItem in header[2] or keyItem in header[3]:
                                pass
                                # result.append(EmailReceive.getOneMail(data,getAttach))
                            else:
                                flag_ = 1
                                break
                        if flag_ == 0:
                            result.append(EmailReceive.getOneMail(data,getAttach))
                            if not findAll:
                                self.close()
                                return result

            except Exception as e:
                print(e)
        self.close()
        return result

    @staticmethod
    def getMailHeader(data):
        if data is None or data[0] is None or data[0][1] is None:
            return None
        try:
            message = email.message_from_bytes(data[0][1])
            return EmailReceive.__parseHeader(message)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getMailBody(data,getAttach=False):
        if data is None or data[0] is None or data[0][1] is None:
            return None
        try:
            message = email.message_from_bytes(data[0][1])
            return EmailReceive.__parseBody(message,getAttach)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getOneMail(data,getAttach=False):
            if data is None or data[0] is None or data[0][1] is None:
                return None,None
            try:
                message = email.message_from_bytes(data[0][1])
                header = EmailReceive.__parseHeader(message)
                body = EmailReceive.__parseBody(message,getAttach)
                return header,body
            except Exception as e:
                print(e)
                return None,None

    @staticmethod
    def __parseHeader(message):
        """ 解析邮件首部 """
        try:
            if not message.get('Subject'):
                title=''
            else:
                title = email.header.decode_header(message.get('Subject'))
                if title[0][1] is not None:
                    encodetype = title[0][1]
                    if 'unknow' in encodetype:
                        encodetype='GBK'
                    title = title[0][0].decode(encodetype)
                else:
                    title = title[0][0]
            fromAddr= email.utils.parseaddr(message.get('from'))[1]
            toAddr = email.utils.parseaddr(message.get('to'))[1]
            receiveDate = email.utils.parsedate(message.get('Date'))
            receiveDate=str(receiveDate[0])+'-'+str(receiveDate[1]).zfill(2)+'-'+str(receiveDate[2]).zfill(2)
            result = (title,fromAddr,toAddr,receiveDate)
            return result
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def __parseBody(msg,getAttach=False):
        context=[]
        try:
            for par in msg.walk():
                if par.is_multipart():
                    continue
                patch = par.get_param("name")  # 如果是附件，这里就会取出附件的文件名
                if patch:# 有附件
                    if not getAttach:
                        continue
                    if not os.path.isdir(os.path.join(os.getcwd(),'emailAttach')):
                        os.mkdir(os.path.join(os.getcwd(),'emailAttach'))
                    title = email.header.decode_header(patch)
                    if title[0][1] is not None:
                        fname = title[0][0].decode(title[0][1])
                    else:
                        fname=title[0][1]
                    if fname is None:
                        fname='no name'
                    print('附件名:', fname)
                    data = par.get_payload(decode=True)  # 解码出附件数据，然后存储到文件中
                    filename = os.path.join(os.getcwd(),'emailAttach',secure_filename(''.join(lazy_pinyin(fname))))
                    try:
                        with open(filename,'wb') as f:
                            f.write(data)
                            context.append('file:{}'.format(fname))
                    except Exception as e:
                        print(e)
                else:
                    try:
                        context.append(par.get_payload(decode=True).decode('utf-8'))
                    except Exception as e:
                        print(e)
                        try:
                            context.append(par.get_payload(decode=True).decode('gbk'))
                        except Exception as e:
                            print(e)
                            context.append(par.get_payload())
            return context
        except Exception as e:
            print(e)
            return None

if __name__=='__main__':
    # a = EmailReceive('47029316@qq.com','rvueixdphgjdbjeb')
    a = EmailReceive('KenneyBurnsK@aol.com','nz1thm5b')
    print(a.getEmail(keyword=('Subject: Activate Membership to Start Earning Rewards',),onlyUnsee=False,findAll=False))



