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
            '10003'      : '',  # UK Swipe  Done
            '10004'      : '',  # Ad1   opinion outpost   Done
            '10005'      : '',  # Adsmain Cam4  Done           
            '10006'      : '',         # adgaem 1.2   GUARDIANS OF AMBER  Done        
            '10007'      : '',         # Best Obama Care affprofile Done
            '10008'      : '',         # CashRequestOnline Done
            '10009'      : '',         # Stripchat  
            '10010'      : '',         # rifu  chajian Done
            '10011'      : '',         # Auto Insurance  dead
            '10012'      : '',         # affprofile   cindmatch  
            '10013'      : '',         # IKARIAM             '10006'      : '',         # LP            
            '10014'      : '',         # bbw
            '10015'      : '',         # IKARIAM
            '10016'      : '',         # IKARIAM             '10006'      : '',         # LP            
            '10017'      : '',         # IKARIAM
            '10018'      : '',         # IKARIAM
            '10019'      : '',         # IKARIAM             '10006'      : '',         # LP            
            '10020'      : '',         # IKARIAM
            '10021'      : '',         # IKARIAM
            '10022'      : '',         # IKARIAM                                               
            '10023'      : '',         # IKARIAM
            '10024'      : '',         # IKARIAM
            '10025'      : '',          # IKARIAM              
            '10026'      : '',         # IKARIAM
            '10027'      : '',         # IKARIAM
            '10028'      : '',         # IKARIAM              
            '10029'      : '',         # IKARIAM
            '10030'      : '',         # IKARIAM
            '10031'      : ''          # IKARIAM              
        },
        'Email_list':{
            'hotmail.com'    : 1, # 1 means use this email,0 means not
            'outlook.com'    : 1,
            'yahoo.com'      : 1,
            'aol.com'        : 1
        }
    }
    return Configs['Delay'],Configs['Config'],Configs['Mission_conf'],Configs['Email_list']



