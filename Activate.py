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
    try:
        tools.killpid()
    except Exception as e:
        print(str(e))
        pass    
    plans = db.read_plans(plan_id)
    print('Mission:')
    print(plans)
    requests = threadpool.makeRequests(multi_activate, plans)
    [pool.putRequest(req) for req in requests]
    pool.wait() 
    restart_time = random.randint(3,5)
    print('Mission completed.........')
    print('Sleep',restart_time,'minutes')
    sleep(restart_time*60)
    changer.Restart()

if __name__ == '__main__':
    country = 'US'
    Module_list = [10005,10009]
    main(country,Module_list)



