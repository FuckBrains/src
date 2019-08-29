import tools
import Chrome_driver
from time import sleep
import zipfile
import os
import shutil
from shutil import copyfile


def get_code():
    account_coding = read_account()
    chrome_driver = Chrome_driver.get_chrome()
    url_back = r'https://emu_multi.coding.net/signin?redirect=%2Fuser'
    url_code = r'https://emu_multi.coding.net/p/src/git/archive/master'
    chrome_driver.get(url_back)
    chrome_driver.find_element_by_xpath('//*[@id="userName"]').send_keys(account_coding['name'])
    chrome_driver.find_element_by_xpath('//*[@id="password"]').send_keys(account_coding['pwd'])
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div[2]/form/div[3]/button').click()
    sleep(2)
    chrome_driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[1]').click()
    sleep(2)
    for i in range(20):
        chrome_driver.refresh()
        Chrome_driver.clean_download()        
        chrome_driver.get(url_code)
        sleep(10)
        for i in range(100):
            flag = 0
            modules = Chrome_driver.download_status()
            if len(modules) > 0:
                for module in modules:
                    if '.zip' in module:
                        flag = 1
                        break
            else:
                sleep(2)
            if flag == 1:
                break
        try:
            delete_folder()
            unfold_zip()
            chrome_driver.close()
            chrome_driver.quit()
            break
        except Exception as e:
            print(str(e))
            continue

def unfold_zip():
    path_download = Chrome_driver.get_dir()
    module = 'emu_multi-src-master.zip'
    zipfile_name = os.path.join(path_download,module)
    print(zipfile_name)
    zFile = zipfile.ZipFile(zipfile_name, "r")
    #ZipFile.namelist(): 获取ZIP文档内所有文件的名称列表
    for fileM in zFile.namelist(): 
        zFile.extract(fileM, path_download)
    zFile.close()
    print('zipfile ok,not bad zip......................')
    path_folder = os.path.join(path_download,'src-master')
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
    [os.remove(file) for file in modules_file if '.' in file and  'Auto_update' not in file and '.git' not in file]    
    for folder in modules_folder:
        file_folder = os.listdir(folder)
        file_folder_path = [os.path.join(folder,file) for file in file_folder]
        [os.remove(file) for file in file_folder_path]
    [os.rmdir(folder) for folder in modules_folder]



def main():
    path_download = Chrome_driver.get_dir()
    makedir_account(path_download)
    tools.killpid()
    get_code()

def read_account():
    path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    path_config = os.path.join(path,r'res\Coding.txt')
    print(path_config)
    account_coding = {}
    with open(path_config) as f:
        line = f.readline()
        account = line.split(',')
        account_coding['name'] = account[0]
        account_coding['pwd'] = account[1]
    return account_coding


def makedir_account(path=r'c:\emu_download'):
    isExists=os.path.exists(path)
    if isExists:
        return
    else:
        os.makedirs(path)



def test():
    # source_path = os.getcwd()
    # target_path = 'ini\\'
    # move_folder(source_path,source_path)    
    delete_folder()




if __name__ == '__main__':
    main()