import re
from emailReceive import EmailReceive
from emailSend import EmailSend

class EmailUtil(object):
    @staticmethod
    def getLink(address,password,title=('title',),regular=r'http',findAll=False):
        allRes = EmailReceive(address, password).getEmail(keyword=title, onlyUnsee=False, findAll=findAll)
        if  allRes is None or allRes == []:
            print('find email wrong:',title)
            return 'Good'
        print('find email ok:',title)
        print(allRes)
        pattern = re.compile(regular)
        for head,body in allRes:
            if body :
                for item in body:
                    co = pattern.match(item.replace('\r\n','').replace('\n',''))
                    if co:
                        print('find email-web-link ok:',co.group(1))
                        return co.group(1)
        print('find link wrong')
        return 'Bad'

    @staticmethod
    def getEmail(address,password,title,onlyUnsee=False,findAll=True):
        return EmailReceive(address,password).getEmail(keyword=title,onlyUnsee=onlyUnsee,findAll=findAll)


    @staticmethod
    def sendEmail(senderAddr,senderPassword,receiverList,title,body):
        return EmailSend().sendEmail(senderAddr, senderPassword,receiverList,title, body)
