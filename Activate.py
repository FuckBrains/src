import os
import Changer_windows_info as changer
import ip_test
import importlib
import sys
sys.path.append('..')
import threadpool



pool = threadpool.ThreadPool(5)


def killpid():
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
        except:
            continue
        kill_list = ['chrome.exe','chromedriver.exe','Client.exe','Monitor.exe','MonitorGUI.exe','Socket.exe']
        for key in kill_list:
            if p.name() == key:
                cmd = 'taskkill /F /IM '+key
                try:
                    os.system(cmd)            
                except:
                    pass
  

def multi_activate(module):
    Module = import_Module(module)
    print(module)
    try:
        Module.activate()
    except Exception as e:
        print(str(e))
    # global Falg_threads
    # Falg_threads += 1
    # print('Falg_threads:',Falg_threads)

def import_Module(module):
    module_name = importlib.import_module(module)
    return module_name

def main(country='US',Module_list=[]):
    modules = ['Mission_'+str(num) for num in Module_list]
    # Module_list = get_modules(modules)
    for num_ip in range(6):
        try:
            city = ip_test.ip_Test('','',country=country)
            if  city != 'Not found':
                break
            if num_ip == 5:
                print('Net wrong...!!!!!!')
                changer.Restart()
                return
        except:
            changer.Restart()
    requests = threadpool.makeRequests(multi_activate, modules)
    [pool.putRequest(req) for req in requests]
    pool.wait() 


if __name__ == '__main__':
    country = 'US'
    Module_list = [10005,10009]
    main(country,Module_list)



