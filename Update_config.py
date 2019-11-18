import json

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
    Offer_configs = read_offer_num()
    file_Offer_config = r'ini\Offer_config.ini'
    Write_Ini(file_Offer_config,Offer_configs)
    change__delay_config()

def Write_Alliance_config():
    Alliance_configs = Read_Alliance_num()
    file_Offer_config = r'ini\Offer.ini'
    Write_Ini(file_Offer_config,Alliance_configs)


def main():
    Write_Offer_config()
    Write_Alliance_config()

if __name__ == '__main__':
    main()