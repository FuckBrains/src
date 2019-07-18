#911 country select US = 0 ,CA = 1
Country_list = ['US','UK','FR','DE']
IP_country   = Country_list[0]
IP_state     = 'All'
IP_city      = ''

# sleep time
Sleep_time_up = 0
Sleep_time_down = 0

# threads
Threads = 5




def Config_read():
    Configs = {
        'Delay' : {
            'up'         : Sleep_time_up,
            'down'       : Sleep_time_down,
            'threads'    : Threads
        },
        'Config' : {
            'IP_country' : IP_country,    # 0 means US,1 means CA,2 means FR
            'IP_state'   : IP_state,
            'IP_city'    : IP_city
        },  
        'Mission_conf' :{
            '10000'      : '',  # Finaff    Royal Cams  Done
            '10001'      : '',  # Adgaem    star stable Done
            '10002'      : '',  # Adpump    GETAROUND Done
            '10003'      : '',  # UK Swipe 
            '10004'      : 'http://ares.goldmaketing.com/c/10655/a?clickid=[clickid]&bid=[bid]&siteid=[siteid]&countrycode=[cc]&operatingsystem=[operatingsystem]&campaignid=[campaignid]&category=[category]&connection=[connection]&device=[device]&browser=[browser]&carrier=[carrier]',  # Ad1   opinion outpost   
            '10005'      : '',  # Adsmain Cam4  Done           
            '10006'      : 'https://track.adgaem.com/click?pid=1337&offer_id=62396',         # adgaem 1.2   GUARDIANS OF AMBER         
            '10007'      : 'http://affprofile.o18.click/c?o=676208&m=1659&a=37792',         # Stripchat affprofile
            '10008'      : '',         # IKARIAM
            '10009'      : '',         # IKARIAM  
            '10010'      : '',         # rifu Done
            '10011'      : '',         # IKARIAM
            '10012'      : '',         # IKARIAM
            '10013'      : '',         # IKARIAM             '10006'      : '',         # LP            
            '10014'      : '',         # IKARIAM
            '10015'      : '',         # IKARIAM
            '10016'      : '',         # IKARIAM             '10006'      : '',         # LP            
            '10017'      : '',         # IKARIAM
            '10018'      : '',         # IKARIAM
            '10019'      : '',         # IKARIAM             '10006'      : '',         # LP            
            '10020'      : '',         # IKARIAM
            '10021'      : '',         # IKARIAM
            '10022'      : ''          # IKARIAM                                               
        },
        'Email_list':{
            'hotmail.com'    : 1, # 1 means use this email,0 means not
            'outlook.com'    : 1,
            'yahoo.com'      : 1,
            'aol.com'        : 1
        }
    }
    return Configs['Delay'],Configs['Config'],Configs['Mission_conf'],Configs['Email_list']



