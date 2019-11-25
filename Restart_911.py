import win32gui, win32api, win32con
import psutil
import os
from time import sleep
import tools


def kill_911():
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
        except:
            continue
        # print('pid-%s,pname-%s' % (pid, p.name()))
        if p.name() == 'chrome.exe':
            cmd = 'taskkill /F /IM chrome.exe'
            os.system(cmd)
        if 'chromedriver.exe' in p.name() :
            cmd = 'taskkill /F /IM '+p.name()
            os.system(cmd)      
        if p.name() == 'Client.exe':
            cmd = 'taskkill /F /IM Client.exe'
            os.system(cmd)
        if p.name() == 'Monitor.exe':
            cmd = 'taskkill /F /IM Monitor.exe'
            os.system(cmd)            
        if p.name() == 'MonitorGUI.exe':
            cmd = 'taskkill /F /IM MonitorGUI.exe'
            os.system(cmd)                  
        if 'Socket.exe' in p.name():
            cmd = 'taskkill /F /IM ' + p.name()
            os.system(cmd)             


def click_position(hwd, x_position, y_position, sleeps):
    """
    鼠标左键点击指定坐标
    :param hwd: 
    :param x_position: 
    :param y_position: 
    :param sleep: 
    :return: 
    """
    # 将两个16位的值连接成一个32位的地址坐标
    long_position = win32api.MAKELONG(x_position, y_position)
    # win32api.SendMessage(hwnd, win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP, long_position)
    # 点击左键
    win32api.PostMessage(hwd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
    win32api.PostMessage(hwd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
    # print('ok')

    # sleep(int(sleeps))

def login_911():
    '''
    auto login 911 after 911 client opened
    '''
    # sleep(30)
    # print('begin login_911')
    # try:
    #     kill_OK()
    # except Exception as e:
    #     writelog('',str(e))
    # print('into 911')
    # 查找911客户端
    handle = 0
    while handle == 0:
        handle = win32gui.FindWindow("ThunderRT6FormDC", None)
        # sleep(1)
    print('Find client',handle)  
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    # print(left, top, right, bottom)
    t1 = 0
    while True:
        left1, top1, right1, bottom1 = win32gui.GetWindowRect(handle)
        print('Page1',left1, top1, right1, bottom1)
        if bottom1 != bottom:
            print(left1, top1, right1, bottom1)
            break
        sleep(1) 
        t1 += 1
        if t1  >= 120:
            break
    kill_OK()  
    sleep(5) 
    subHandle = win32gui.FindWindowEx(handle, 0, "ThunderRT6CommandButton", None)   
    print(subHandle,win32gui.GetWindowText(subHandle))
    print('page2,click login button')
    click_position(subHandle,20,20,3) 
    sleep(3)
    flag = 0
    num_time = 0
    while True:
        try:
            left1, top1, right1, bottom2 = win32gui.GetWindowRect(handle)
            print('Page2',left1, top1, right1, bottom1)
            tools.killpid(['Annoucement'])
            kill_OK()
            sleep(3)
            click_position(subHandle,20,20,3)  
            sleep(3)
            num_time += 1
            if num_time >= 10:
                break
        except Exception as e:
            print(str(e))
            flag = 1
            break
    return flag
    # 查找choose server按钮
    # subHandle = 0
    # while subHandle == 0:
    #     # "ThunderRT6CommandButton"
    #     subHandle = win32gui.FindWindowEx(handle, 0, "ThunderRT6CommandButton", None)
    #     sleep(1)
    #     print(subHandle)
    # print('find login button :',subHandle)        
    # kill_OK()

    # sleep(1)
    # click_position(subHandle,20,20,3)
    # print('login_911 finished')



def kill_OK():
    '''
    click ok button after get server failed,if there is this button
    '''
    calssname = u"#32770"
    titlename = u"Client"  
    hwnd = win32gui.FindWindow(calssname,titlename)  
    handle_ok = win32gui.FindWindowEx(hwnd, 0, "Button", None)    
    # print(hwnd)
    # print(handle_ok)   
    # print('this is ok')
    if hwnd != 0:
        # print('Connect server failed or login fialed')
        click_position(handle_ok,10,10,3) 
    else:
        pass
        # print('Connect server success or login success')


def restart911():
    # print('start kill_911')
    flag = 0
    while flag == 0:    
        kill_911()
        # print('After kill_911 finished')
        os.system(r'start ..\tools\911S5\Client.exe')
        # print('After client started,begin login_911')
        flag = login_911()
        print('login_911 finished')
    # print('end')    



if __name__=='__main__':
    for i in range(1):
    #     kill_911()
        restart911()
    #     sleep(5)
    
    #     sleep(5)
