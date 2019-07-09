from urllib import request, parse
import time
import re





def login():
    token = '01122813556244e3d8a9495977393a5bb036419d5501'
    get_account_info_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token='+token 
    # data = {'username':submit['name']}
    # data = parse.urlencode(data).encode('gbk')
    req = request.Request(get_account_info_url)
    # page = '' 
    try: 
        page = request.urlopen(req,timeout=20.0).read()  
        if 'success' in str(page,encoding='utf-8'):
            print(page)
    except Exception as e:
        print(str(e))


def send_data(url):
    req = request.Request(url)
    page = request.urlopen(req,timeout=20.0).read()  
    return str(page,encoding='utf-8')





def get_phone_single():
    token = '01122813556244e3d8a9495977393a5bb036419d5501'
    TIMESTAMP = int(time.time())
    itemid = 659
    TIMESTAMP = int(time.time())
    get_phone_single_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token='+token+'&itemid='+str(itemid)+'&excludeno=170&timestamp='+str(TIMESTAMP)
    response = send_data(get_phone_single_url)
    print(response)
    phone = re.findall('\d+',response)[0]
    return phone,TIMESTAMP
    # print(response)
    # print(TIMESTAMP)


def get_text(phone,TIMESTAMP = None):
    '''
    release为1代表获取到短信后自动释放手机号
    5秒调用1次，调用60秒以上
    '''
    token = '01122813556244e3d8a9495977393a5bb036419d5501'
    itemid = 659
    TIMESTAMP = int(time.time())
    # phone = get_phone_single(token,TIMESTAMP)
    # print(phone)
    get_text_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token='+token+'&itemid='+str(itemid)+'&mobile='+str(phone)+'&release=1&timestamp='+str(TIMESTAMP)
    response = send_data(get_text_url)
    print(response)   
    text = re.findall('\d+',response)[0]
    # free_phone(phone,token)
    return text



def free_phone(phone):
    token = '01122813556244e3d8a9495977393a5bb036419d5501'    
    itemid = 659
    free_phone_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token='+token+'&itemid='+str(itemid)+'&mobile='+str(phone)
    response = send_data(free_phone_url)
    print(response)    








if __name__ == '__main__':
    # 16532027149   17860879174  18454064239
    get_phone_single()
    # get_text(token,'13284901857','1561570185')
    # free_phone('18454064239')
    get_text('13070892179')
