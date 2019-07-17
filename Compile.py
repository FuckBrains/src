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
        
def main():
    modules_path = get_modules()
    print(modules_path)
    [os.remove(file) for file in modules_path]
    sleep(1)
    os.system('python -m compileall')
    sleep(2)
    modules_path = get_modules()    
    [os.remove(file) for file in modules_path if 'Mission' in file]
    sleep(1)
    modules_path = get_modules()
    [os.remove(file) for file in modules_path if 'Cam4_allin' in file]
    sleep(2)
    modules = os.listdir('__pycache__/')
    [rename_file(module) for module in modules]
    sleep(2)
    src = r'C:\Coding\src'
    modules_path = get_modules()
    for file in modules_path:
    	dirname,filename = os.path.split(file)
    	src_file = os.path.join(src,filename)
    	copyfile(file,src_file)
    # [copyfile(file,src) for file in modules_path]
    print('Compile finished.........')
    # modules = [module.strip('.py') for module in modules] 



if __name__ == '__main__':
    # get_modules()
    main()
