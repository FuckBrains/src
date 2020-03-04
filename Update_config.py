import json
import db
import traceback


def read_offer_num():
    Offer_configs = {}
    with open(r'ini\Offer_num.ini') as f:
        lines = f.readlines()
        for line in lines:
            if ',' in line:
                Offer_config = {} 
                configs = line.replace('\n','').split(',')
                Offer_config['Mission_Id'] = str(configs[0])
                Offer_config['Excel'] = ['','']
                # print('Configs:',configs)
                if '+' in configs[2]:
                    excels = configs[2].split('+')
                    for excel in excels:
                        if excel != 'Email':
                            Offer_config['Excel'][0] = excel
                        else:
                            Offer_config['Excel'][1] = excel

                else:
                    if configs[2] != 'Email':
                        Offer_config['Excel'][0] = configs[2]
                    else:
                        Offer_config['Excel'][1] = configs[2]
                Offer_configs[configs[1]] = Offer_config
    # print(Offer_configs)
    return Offer_configs

    # change__delay_config()

def change__delay_config():
    file_Offer_config = r'ini\Offer_config.ini'
    Offer_config = Read_Ini(file_Offer_config)
    Offer_config['Delay'] = {}
    Offer_config['Delay']['up'] = 3
    Offer_config['Delay']['down'] = 5
    Offer_config['Delay']['threads']= 5
    Offer_config['Email_list'] = {}
    Offer_config['Email_list']['hotmail.com'] = 1
    Offer_config['Email_list']['outlook.com'] = 1
    Offer_config['Email_list']['yahoo.com'] = 1
    Offer_config['Email_list']['aol.com'] = 1
    Write_Ini(file_Offer_config,Offer_config)



def get_offer_name():
    Offer_configs = read_offer_num()
    Mission_offer = {}
    for offer in Offer_configs:
        index = Offer_configs[offer]['Mission_Id']
        Mission_offer[index] = offer
    return Mission_offer


def Read_Alliance_num():
    Mission_offer = get_offer_name()
    with open(r'ini\Alliance_num.ini') as f:
        lines = f.readlines()
        alliances = {}
        for line in lines:
            if ',' in line:
                alliance = []
                configs = line.replace('\n','').split(',')
                if '+' in configs[1]:
                    Missions = configs[1].split('+')                
                    for Mission in Missions:
                        try:
                            offer_name = Mission_offer[Mission]
                            alliance.append(offer_name)
                        except Exception as e:
                            print(str(e))
                else:
                    offer_name = Mission_offer[configs[1]]
                    alliance.append(offer_name)                    
                alliances[configs[0]] = alliance
    # print(alliances)
    return alliances

def Read_Ini(file):
    submits = []
    with open(file,'r') as f:
        jss = f.readlines()
        # print(jss)
        for js in jss:
            submit = json.loads(js)
            submits.append(submit)
            # print(submit)
    if len(submits) >= 1:
        return submits[-1]
    else:
        return []

def Write_Ini(file,content):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    content = json.dumps(content) 
    with open(file,'w') as f:
        # content += '\n'
        f.write(content)


def Write_Offer_config():
    try:
        Offer_configs = read_offer_num()
        print(Offer_configs)
    except Exception as e:
        content = traceback.format_exc()  
        print('traceback.format_exc():' ,content)          
    file_Offer_config = r'ini\Offer_config.ini'
    # print(Offer_configs)
    # return Offer_configs
    Write_Ini(file_Offer_config,Offer_configs)
    # change__delay_config()

def Write_Alliance_config():
    Alliance_configs = Read_Alliance_num()
    file_Offer_config = r'ini\Offer.ini'
    # print(Alliance_configs)
    # return Alliance_configs
    Write_Ini(file_Offer_config,Alliance_configs)


def upload_config_db():
    Offer_configs = Write_Offer_config()
    db.upload_offer_config(Offer_configs)

def upload_alliance_config_db():
    offers = db.get_offer_config()
    # Offer_configs = Write_Alliance_config()
    # db.upload_offer_config(Offer_configs)
    for alliance in Offer_configs:
        Offer_configs[alliance] = [offers[name] for name in Offer_configs[alliance]]
    # print(Offer_configs)
    db.upload_Allinace_config(Offer_configs)

def get_alliance_config():
    # db.get_alliance_config() 
    alliances = db.get_alliance_config()    
    # print(alliances)
    return alliances

def download_alliance_config():
    alliances = get_alliance_config()
    contents = ''
    for key in alliances:
        contents +=  key + ',' + alliances[key] +'\n'
    # print(contents)
    return contents

def download_offer_config():
    res = db.get_offer_config()
    # Offer_configs = Write_Alliance_config()
    print(res)
    contents = ''
    Missoin_config = list(res[0])
    Missoin_config = sorted(Missoin_config,key=by_mission_id)
    # print(Missoin_config)
    for config in Missoin_config:
        excel_config = config[1].split(',')
        excel = excel_config[0]+excel_config[1]
        contents += config[0]+','+config[2]+','+excel+'\n'
    print(contents)
    return contents    

def by_mission_id(t):
    return int(t[0]) 

def update_config():
    alliance_config = download_alliance_config()
    file = r'ini\Alliance_num.ini'
    with open(file,'w') as f:
        f.write(alliance_config)
    offer_config = download_offer_config()
    file = r'ini\Offer_num.ini'    
    with open(file,'w') as f:
        f.write(offer_config)
    Write_Offer_config()
    # Write_Alliance_config()        



def main():
    # Write_Offer_config()
    # Write_Alliance_config()
    # upload_alliance_config_db()
    upload_offer()

if __name__ == '__main__':
    main()