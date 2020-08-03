import db
import json

def write_page_flag(Mission_Id):
    page = db.get_page_flag(Mission_Id,1)
    print(page)
    file_name = '%s_page_flag'%Mission_Id    
    save_data(page,file_name)

def write_page_config(Mission_Id):
    for i in range(10):
        config = db.get_page_config(Mission_Id,i,1)
        if len(config)==0:
            print('No config in page %d'%i)
            continue
        file_name = '%s_page_config_page%s'%(Mission_Id,str(i))
        save_data(config,file_name)


def save_data(content,filename):
    # 保存
    file_dir = r'..\config\%s.npy'%filename
    # makedir_account(file_dir)
    with open(file_dir,'w') as f:
        for info in content:
            item = json.dumps(info)
            f.write(item)
            f.write('\n') 

def read_data(filename):
    infos = []
    file_dir = r'..\config\%s.npy'%filename
    with open(file_dir,'r') as f:
        lines = f.readlines()
    for line in lines:
        if line=='\n':
            continue
        info = json.loads(line)
        infos.append(info)
    # print(infos)
    return infos

def write_mission_config():
    Mission_Id = '10002'
    write_page_flag(Mission_Id)
    write_page_config(Mission_Id)

if __name__ == '__main__':
    write_mission_config()
