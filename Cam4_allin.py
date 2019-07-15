#911 country select US = 0 ,CA = 1
Country_list = ['US','UK','FR','DE']
IP_country   = Country_list[0]
IP_state     = 'All'
IP_city      = ''

# sleep time
Sleep_time_up = 2
Sleep_time_down = 6

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
            '10000'      : 'http://www.baidu.com',  # Finaff    Royal Cams  Done
            '10001'      : 'http://www.baidu.com',  # Adgaem    star stable Done
            '10002'      : '',  # Adpump    GETAROUND
            '10003'      : '',  # UK Swipe 
            '10004'      : '',  # Ad1   opinion outpost   
            '10005'      : 'http://www.baidu.com',  # Adsmain Cam4  Done           
            '10006'      : '',         # adpump GETAROUND  https://adpgtrack.com/click/5b73d90a6c42607b3b6c4323/199595/subaccount/url=example.com            
            '10007'      : '',         # IKARIAM
            '10008'      : 'http://www.baidu.com',         # IKARIAM
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



