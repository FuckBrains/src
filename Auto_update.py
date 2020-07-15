import tools
import Chrome_driver
from time import sleep
import zipfile
import os
import shutil
from shutil import copyfile
import Changer_windows_info as changer
import db
from os.path import join, getsize
import luminati

def get_updateinfo():
    print('======get_updateinfo')
    sql_content = "select * from update_config;"
    account = db.get_account(1)
    # print(account)
    conn,cursor = db.login_sql(account)
    # for sql_content in sql_contents:
        # print('\n\n\n')
        # print(sql_content)
    res = cursor.execute(sql_content)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    update_config = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来  
    # print(update_config[0])
    db.login_out_sql(conn,cursor)    
    return update_config[0]

def get_code():
    for i in range(10):
        try:
            update_config = get_updateinfo()
            break
        except:
            pass
    chrome_driver = Chrome_driver.get_chrome()
    # print(update_config)
    url_back = update_config['url_back']
    url_code = update_config['url_code']

    for j in range(10):
        try:
            chrome_driver.get(url_back)
            chrome_driver.find_element_by_xpath(update_config['xpath_username']).send_keys('18122710376')
            chrome_driver.find_element_by_xpath(update_config['xpath_pwd']).send_keys('Ddf!@s345a1asd')
            sleep(2)
            chrome_driver.find_element_by_name(update_config['xpath_checkbox']).click()
            # chrome_driver.find_element_by_xpath(update_config['xpath_checkbox']).click()
            sleep(1)
            print('file 1.0')
            chrome_driver.find_element_by_tag_name(update_config['xpath_button']).click()
            sleep(1)  
        except Exception as e:
            print(str(e))
            continue      
        chrome_driver.refresh()
        Chrome_driver.clean_download()        
        chrome_driver.get(url_code)
        sleep(10)
        for i in range(100):
            flag = 0
            modules = Chrome_driver.download_status()
            names = update_config['zipname'].split(',')
            names = [name+'.zip' for name in names]
            module_name = ''
            for module in modules:
                if module in names:
                    module_name = module
                    print('Find zip src')
                    sleep(3)
                    flag = 1
                    chrome_driver.close()
                    chrome_driver.quit()  
                    flag_zip = test_zip(module)        
                    if flag_zip == 0:
                        return -1
                    delete_folder()
                    unfold_zip(module_name)                                      
                    break
                else:
                    sleep(2)
            if flag == 1:
                break
        if flag == 1:
            break                
            # sleep(1)
    if flag != 1:        
        chrome_driver.close()
        chrome_driver.quit()  
    return flag

def file_copy(flag):
    flag_zip = test_zip(module)        
    if flag_zip == 0:
        return -1
    delete_folder()
    unfold_zip(module_name)
    return 1

def test_zip(module):    
    path_download = Chrome_driver.get_dir()
    print(path_download)
    # module = 'emu_multi-src-master.zip'
    zipfile_name = os.path.join(path_download,module)
    size = getsize(zipfile_name)/1024/1024    
    print('The zipfile size:',size,'M')
    flag = 0
    if size>25:
        print('size ok')
        zFile = zipfile.ZipFile(zipfile_name, "r")
        #ZipFile.namelist(): 获取ZIP文档内所有文件的名称列表
        for fileM in zFile.namelist(): 
            try:
                zFile.extract(fileM, path_download)
                flag = 1        
            except:
                flag = 0
        zFile.close()
        print('zipfile open ok,not bad zip......................')        
    else:
        print('size not ok, bad zip')
    return flag

def unfold_zip(module):
    path_download = Chrome_driver.get_dir()
    # module = 'emu_multi-src-master.zip'

    files_unzip = os.listdir(path_download)
    for file in files_unzip:
        if 'src' in file and '.zip' not in file:
            file_unzip = file 
    print('folder name:',file_unzip)
    path_folder = os.path.join(path_download,file_unzip)
    modules = os.listdir(path_folder) 
    folder_ = [file for file in modules if '.' not in file]
    path_folder_file = [os.path.join(path_folder,file) for file in modules]
    duplicated_file = os.listdir(os.getcwd())
    # [shutil.copyfile(file,os.getcwd()) for file in path_folder_file if '.' in file]
    path_cur = os.getcwd()
    for file in path_folder_file:
        if '.' in file:
            try:
                print(file)
                dirname,filename = os.path.split(file)
                shutil.copyfile(file,os.path.join(path_cur,filename))
            except Exception as e:
                print('copyfile wrong:.........',file)
                print(str(e))
    folders_path = [file for file in path_folder_file if '.' not in file]
    for file_folder in folders_path:
        dirname,filename = os.path.split(file_folder)
        new_folder = os.path.join(os.getcwd(),filename)
        try:        
            shutil.copytree(file_folder,new_folder)
        except Exception as e:
            print(str(e))
            print('copyfolder wrong:.........',file_folder)

def change_version():
    file = r'ini\\VERSION.ini'
    num_db = db.get_current_version()
    num_db = str.join('.',num_db)    
    with open(file,'w') as f:
        f.write(num_db)



# def copy_zip():
#     path_download = Chrome_driver.get_dir()
#     path_zip = os.path.join(path_download,'emu_multi-src-master.zip')
#     copyfile(path_download,)


def move_all():
    path_download = Chrome_driver.get_dir()
    path_folder = os.path.join(path_download,'src-master')
    modules = os.listdir(path_folder)
    print(modules)
    files = [file for file in modules if '.' in file]
    folders = [file for file in modules if '.' not in file]
    print(files)
    print(folders)


# def move_folder(source_path,target_path):
#     # delete_folder()
#     if not os.path.exists(target_path):
#         os.makedirs(target_path)
#     if os.path.exists(source_path):
#         # root 所指的是当前正在遍历的这个文件夹的本身的地址
#         # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
#         # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
#         for root, dirs, files in os.walk(source_path):
#             for file in files:
#                 src_file = os.path.join(root, file)
#                 shutil.copy(src_file, target_path)
#                 print(src_file)    
#         pass
    
def delete_folder():
    print('Star delete folder............')
    path_src = os.getcwd()
    modules_path = os.listdir(path_src)
    modules_file = [os.path.join(path_src,file) for file in modules_path if '.'  in file]
    print(modules_path)
    modules_folder = [os.path.join(path_src,file) for file in modules_path if '.' not in file]
    [os.remove(file) for file in modules_file if '.' in file and  'Auto_update' not in file and '.git' not in file and 'chromedriver' not in file]    
    print(modules_folder)
    for folder in modules_folder:
        file_folder = os.listdir(folder)
        # file_folder_path = [os.path.join(folder,file) for file in file_folder if 'driver' not in file_folder]
        file_folder_path = [os.path.join(folder,file) for file in file_folder ]        
        # [os.remove(file) for file in file_folder_path if 'chromedriver' not in file]
        [os.remove(file) for file in file_folder_path]        
    # [os.rmdir(folder) for folder in modules_folder if 'driver' not in folder]
    [os.rmdir(folder) for folder in modules_folder]

def clean_ports():
    account = db.get_account()
    plan_id = account['plan_id']
    plans = db.read_plans(plan_id)
    print('read plan finished')
    ports = [plan['port_lpm'] for plan in plans]    
    luminati.delete_port(ports)

def main():
    tools.killpid()
    flag = get_code()
    if flag == 1:
        print('Update success')
        # flag_update = file_copy(flag)
    else:
        print('Update failed!!!!!!!!')
        return
    if flag == 1:
        change_version()
        clean_ports()
        changer.Restart()


def test():
    # source_path = os.getcwd()
    # target_path = 'ini\\'
    # move_folder(source_path,source_path)    
    delete_folder()




if __name__ == '__main__':
    main()
