from emaiUtil import EmailUtil
import re
from wrapt_timeout_decorator import *

def test_re():
    target = '(https://opinionoutpost.com/Membership/Intake?signuptoken=50151618-0e11-4086-85ba-58d521702ae7&resp=1618848872)\n'
    re_str = r'.*?(https://opinionoutpost.com/Membership/Intake\?signuptoken=.*?\&resp=([0-9]{5,15}))'
    # re_str = r'https://opinionoutpost.com/Membership/Intake\?.*?'
    pattern = re.compile(re_str)
    co = pattern.match(target.replace('\r\n','').replace('\n',''))
    print(co.group(1))
    if co:
        print('find email-web-link ok:',co.group(1))
        return co.group(1)
    else:
        pass


def main():
    '''提供邮件收取、发送功能'''
    # print(EmailUtil.getLink('thomas_land@163.com', 'shouquanma1',('请验证您的会员资格',),r'.*?(https://lifepointspanel.com/doi-by-email/account\?domain.*?)\".*?'))
    # EmailUtil.sendEmail("测试发送 <BerthaThomasFZ@aol.com>", 'SUw9UgLh',
    #                       ["测试接收1 <47029316@qq.com>", "测试接收2 <285765981@qq.com>"],
    #                       "标题", "内容")
    # EmailUtil.sendEmail("测试发送 <lid0lv72@21cn.com>", 'Dhu4368969',
    #                                           ["测试接收1 <lid0lv72@21cn.com>"],
    #                                           "标题", "内容")
    pass    



@timeout(120)
def get_email(email,pwd,title = ('title',),pattern=r'http',findAll=False,debug=0):
    print('Getting into EmailUtil..........')
    site = EmailUtil.getLink(email,pwd,title,pattern,findAll,debug) 
    return  site

if __name__=='__main__':
    get_email()

