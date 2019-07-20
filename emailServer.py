class EmailService(object):
    EMAIL_SERVER={
        "QQ":{"SMTP":["smtp.qq.com",465,True],"POP3":["pop.qq.com",995,True],"IMAP":["imap.qq.com",993,True]},
        "GMAIL":{"SMTP":["smtp.gmail.com",465,True],"POP3":["pop.gmail.com",995,True],"IMAP":["imap.gmail.com",993,True]},
        "FOXMAIL":{"SMTP":["SMTP.foxmail.com",465,True],"POP3":["POP3.foxmail.com",995,True],"IMAP":["imap.foxmail.com",993,True]},
        "SINA":{"SMTP":["smtp.sina.com.cn",465,True],"POP3":["pop3.sina.com.cn",995,True],"IMAP":["imap.sina.com",993,True]},
        "163":{"SMTP":["smtp.163.com",465,True],"POP3":["pop.163.com",995,True],"IMAP":["imap.163.com",993,True]},
        "HOTMAIL":{"SMTP":["smtp.live.com",25,False],"POP3":["pop.live.com",995,True],"IMAP":["imap.live.com",993,True]},
        "OUTLOOK":{"SMTP":["smtp-mail.outlook.com",25,False],"POP3":["pop-mail.outlook.com",995,True],"IMAP":["imap-mail.outlook.com",993,True]},
        "AOL":{"SMTP":["smtp.aol.com",25,False],"POP3":["pop.aol.com",110,False],"IMAP":["imap.aol.com",993,True]},
        "YAHOO":{"SMTP":["smtp.mail.yahoo.com",465,True],"POP3":["pop.mail.yahoo.com",995,True],"IMAP":["imap.mail.yahoo.com",993,True]},
        "21CN": {"SMTP": ["smtp.21cn.com", 465, True], "POP3": ["pop.21cn.com", 995, True],"IMAP": ["imap.21cn.com", 143, False]},
    }

    @staticmethod
    def __getEmailServer(emailtype,servertype):
        return EmailService.EMAIL_SERVER.get(emailtype.upper()).get(servertype)

    @staticmethod
    def getSMTPServer(emailtype):
        return EmailService.__getEmailServer(emailtype.upper(),'SMTP')

    @staticmethod
    def getPOPServer(emailtype):
        return EmailService.__getEmailServer(emailtype.upper(),'POP3')

    @staticmethod
    def getIMAPServer(emailtype):
        return EmailService.__getEmailServer(emailtype.upper(),'IMAP')