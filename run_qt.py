import sys,getopt,threadpool,re,os,shutil,time
from functools import wraps
from urllib import request
sys.path.append('.')
sys.path.append('..')
from src.offer.offer_lifePoints.mainPage import MainPage
from src.offer.offer_lifePoints.register import RegisterPage
from src.offer.offer_lifePoints.lifeRequest import LifeReq
from src.offer.offer_lifePoints.dealCard import DealCard

from src.LogMoule import logger
from src.util.computerInfo import ComputerUtil
from src.util.proxyAgent import AgentUtil

def ip_info_change_required(*dargs, **dkargs):
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            if not kwargs.get('stayIP'):
                while not AgentUtil.changeIP(city=dkargs.get('city'), state=dkargs.get('state'), country=dkargs.get('country')):
                    logger.error('ip change failure')
                    time.sleep(1)
            func(*args, **kwargs)
            if not kwargs.get('stayInfo'):
                ComputerUtil.CleanAndChangeInfo()
        return _wrapper
    return wrapper

class LifePointsRun(object):
    @staticmethod
    def writeAllToken():
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firef'}
        req = request.Request(url="http://track.rehealthylife.com/survey/config.txt", headers=header, method="GET")
        res = request.urlopen(req).read()
        pattern = re.compile('^(\d+).*?----([a-zA-Z0-9-]+)')
        for item in res.decode(encoding='utf-8').split('\r\n'):
            res = pattern.match(item)
            if res:
                LifeReq().addResearch(res.group(1), res.group(2))

    @staticmethod
    def runOneJob(information,runTime):
        MainPage(information).doJob(runTime)

    @staticmethod
    @ip_info_change_required(city='ALL',state='ALL',country='CN')
    def runJob(jobNum=1,runTime=None,threadNum=1,stayInfo=False,stayIP=False,timeoutSec=24000):
        while True:
            #清空cache
            if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),'cache')):
                shutil.rmtree(os.path.join(os.path.dirname(os.path.realpath(__file__)),'cache'))
            #清空超时任务
            LifeReq().freeTimeOutJob()
            #清空本机器控制的任务
            LifeReq().freeMachine()
            try:
                accounts = LifeReq().getAvailableJob(country=("CHN",), number=jobNum)
                for item in accounts:
                    LifeReq().busyDoJob(item['life_id'])
                # 创建多线程运行
                pool = threadpool.ThreadPool(threadNum)
                data = [((index, runTime), None) for index in accounts]
                requests = threadpool.makeRequests(LifePointsRun.runOneJob, data)
                [pool.putRequest(req) for req in requests]
                pool.wait()
                for item in accounts:
                    LifeReq().freeDoJob(item['life_id'])
            except Exception as e:
                print(e)
            finally:
                #清空本机器控制的任务
                LifeReq().freeMachine()
                if not stayInfo:
                    return None

    @staticmethod
    def registerOne(information):
        RegisterPage().doJob(information)
    @staticmethod
    def registerJob(regNumber=None,threadNum=1):
        allInfo = LifeReq().getUnRegisterInformation(("CHN",), regNumber)
        pool = threadpool.ThreadPool(threadNum)
        data = [((index,), None) for index in allInfo]
        requests = threadpool.makeRequests(LifePointsRun.registerOne, data)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    @staticmethod
    def recheckOneAccount(account):
        if account['activate_state'] == '0':
            # 检查邮箱
            email = LifeReq().getEmailByID(account['life_id'])
            if email:
                print('重新检查激活邮箱：', email['email_address'], email['email_id'])
                RegisterPage().confirmRegister(email['email_id'], email['email_address'], email['email_auth_code'],
                                               ('请验证您的会员资格',),
                                               r'.*?(https://lifepointspanel.com/doi-by-email/account\?domain.*?)\".*?')
        elif account['activate_state'] == '-1':
            # 再做一次任务，进行封号判断
            print('重新检查封号:', account['life_id'])
            info = LifeReq().getJobByID(account['life_id'])
            MainPage(info).doJob(1)

    @staticmethod
    def recheckAccounts(threadNum=1):
        #针对状态有问题的账号，重查一遍，防止遗漏，或者因为某次加载问题导致丢失账号
        allaccounts=LifeReq().getAllAccount()
        pool = threadpool.ThreadPool(threadNum)
        data = [((index,), None) for index in allaccounts]
        requests = threadpool.makeRequests(LifePointsRun.recheckOneAccount, data)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    @staticmethod
    def checkOneEmailOrder(emailInfo):
        DealCard(emailInfo).getAllOrder()
    @staticmethod
    def recheckEmailOrder(threadNum=1,allEmail=False):
        #过滤无效邮箱
        fallEmail=[]
        if allEmail:
            allEmail = LifeReq().getAllEmail()
            for item in LifeReq().getAllAccount():
                for em in allEmail:
                    if em['email_id'] == item['life_id']:
                        fallEmail.append(em)
                        break
        else:
            allError = list(filter(lambda x:x['error_type']=='0',LifeReq().getAllError()))
            for item in allError:
                em = LifeReq().getEmailByID(item['email_id'])
                if em:
                    fallEmail.append(em)
        print('检测邮箱数量：',len(fallEmail))
        pool = threadpool.ThreadPool(threadNum)
        data = [((index,), None) for index in fallEmail]
        requests = threadpool.makeRequests(LifePointsRun.checkOneEmailOrder, data)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    @staticmethod
    def checkOneEmailCard(card):
        emailInfo = LifeReq().getEmailByID(card['email_id'])
        if emailInfo:
            DealCard(emailInfo).startCheckEmail(card['order_id'])
    @staticmethod
    def checkJDCard(threadNum=1):
        allCards = LifeReq().getAllCards()
        pool = threadpool.ThreadPool(threadNum)
        data = [((index,), None) for index in allCards]
        requests = threadpool.makeRequests(LifePointsRun.checkOneEmailCard, data)
        [pool.putRequest(req) for req in requests]
        pool.wait()

if __name__=='__main__':
    try:
        options, arg = getopt.getopt(sys.argv[1:], "",['threadNum=','register=','runjob=','runTime=','timeoutSec=','stayInfo','stayIP','recheckAccount','recheckOrder','checkAll','checkCard'])
    except getopt.GetoptError:
        sys.exit()
    runType=-1
    runThread=1
    #注册参数（个数+线程数），个数为-1，表示全部做
    registerNum=None
    #做任务参数
    offerNumber=None
    offerDoTime=2
    sectimeout=24000
    keepIP=False
    keepInfo=False
    #检查订单号参数
    checkAllEmail=False
    for name,value in options:
        if name in ('--register',):
            runType=0
            if int(value)==-1:
                registerNum=None
            else:
                registerNum =int(value)
        elif name in ('--runjob',):
            runType=1
            if int(value)==-1:
                offerNumber=None
            else:
                offerNumber =int(value)
        elif name in ('--recheckAccount',):
            runType=2
        elif name in ('--recheckOrder',):
            runType=3
        elif name in ('--checkCard',):
            runType=4
        elif name in ('--threadNum',):
            runThread=int(value)
        elif name in ('--runTime',):
            offerDoTime=int(value)
        elif name in ('--timeoutSec',):
            sectimeout=int(value)
        elif name in ('--stayIP'):
            keepIP=True
        elif name in ('--stayInfo',):
            keepInfo=True
        elif name in ('--checkAll',):
            checkAllEmail=True

    if runType==0:
        LifePointsRun.registerJob(regNumber=registerNum,threadNum=runThread)
    elif runType==1:
        LifePointsRun.runJob(jobNum=offerNumber, runTime=offerDoTime, threadNum=runThread,stayInfo=keepInfo,stayIP=keepIP,timeoutSec=sectimeout)
    elif runType==2:
        LifePointsRun.recheckAccounts(threadNum=runThread)
    elif runType==3:
        LifePointsRun.recheckEmailOrder(threadNum=runThread,allEmail=checkAllEmail)
    elif runType==4:
        LifePointsRun.checkJDCard(threadNum=runThread)



