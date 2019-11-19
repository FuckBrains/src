import os
from time import sleep
from shutil import copyfile


def rename_file(file):
    path = os.getcwd()
    path = os.path.join(path,'__pycache__/')
    new_file = file.split('.')
    file = os.path.join(path,file)
    new_file = new_file[0]+'.'+new_file[2]
    new_file = os.path.join(path,new_file)
    os.rename(file,new_file)

def get_modules():
    modules = os.listdir('__pycache__/')
    # print(modules)
    path = os.path.join(os.getcwd(),'__pycache__')
    modules_path = [os.path.join(path,file) for file in modules]
    return modules_path

def get_Mission_files():
    modules = os.listdir('./')
    modules = [file for file in modules if 'Mission' in file ]
    print(modules)
    path = os.getcwd()
    Mission_path = [os.path.join(path,file) for file in modules]
    print(Mission_path)
    return Mission_path    

def get_folder_files(folder_name):
    modules = os.listdir(folder_name)
    # print(modules)
    path = os.path.join(os.getcwd(),folder_name)
    modules_path = [os.path.join(path,file) for file in modules]
    return modules_path


def main():
    # get all file abs path in dir'__pycache__'/
    modules_path = get_modules()
    print(modules_path)

    # delete them all
    [os.remove(file) for file in modules_path]
    sleep(1)

    # compile the src dir
    os.system('python -m compileall')
    sleep(2)

    # get all compiled file abs path in dir'__pycache__'/    
    modules_path = get_modules()    
    # remove mission files
    [os.remove(file) for file in modules_path if 'Mission' in file]
    sleep(1)

    # get all file names in dir '__pycache__'/
    modules = os.listdir('__pycache__/')
    # rename all these files so that they can run everywhere
    [rename_file(module) for module in modules]
    sleep(2)

    # move file in cash into Coding
    src = r'C:\Coding\src'
    driver = r'C:\Coding\src\driver'
    ini = r'C:\Coding\src\ini'
    lp = r'C:\Coding\src\lp'
    ui = r'C:\Coding\src\ui'
    modules_path_src = get_folder_files(src)
    [os.remove(file) for file in modules_path_src if '.' in file and '.git' not in file]
    modules_path_driver = get_folder_files(driver)
    [os.remove(file) for file in modules_path_driver]
    modules_path_ini = get_folder_files(ini)
    [os.remove(file) for file in modules_path_ini]
    modules_path_lp = get_folder_files(lp)
    [os.remove(file) for file in modules_path_lp ]
    modules_path_ui = get_folder_files(ui)
    [os.remove(file) for file in modules_path_ui]


    # __pycache__
    modules_path = get_modules()
    for file in modules_path:
        dirname,filename = os.path.split(file)
        src_file = os.path.join(src,filename)
        copyfile(file,src_file)

    # src
    Mission_path = get_Mission_files()
    for file in Mission_path:
        dirname,filename = os.path.split(file)
        src_file = os.path.join(src,filename)
        copyfile(file,src_file)        

    # driver
    Mission_path = get_folder_files('driver')
    for file in Mission_path:
        dirname,filename = os.path.split(file)
        src_file = os.path.join(driver,filename)
        copyfile(file,src_file) 

    # ini
    Mission_path = get_folder_files('ini')
    for file in Mission_path:
        dirname,filename = os.path.split(file)
        src_file = os.path.join(ini,filename)
        copyfile(file,src_file) 

    # lp
    Mission_path = get_folder_files('lp')
    for file in Mission_path:
        dirname,filename = os.path.split(file)
        src_file = os.path.join(lp,filename)
        copyfile(file,src_file)                 

    # ui
    Mission_path = get_folder_files('ui')
    for file in Mission_path:
        dirname,filename = os.path.split(file)
        src_file = os.path.join(ui,filename)
        copyfile(file,src_file)  



    # [copyfile(file,src) for file in modules_path]
    print('Compile finished.........')
    # modules = [module.strip('.py') for module in modules] 
    command = '..\StartGit.bat'
    os.system(command)


if __name__ == '__main__':
    main()
