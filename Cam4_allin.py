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
            '10000'      : '', 
            # 'http://eleftdating.com/click.php?c=8&key=aws43i04846wfzzibkf6uv9w',        # Finaff    Royal Cams  Done
            '10001'      : '' ,
            # 'http://eleftdating.com/click.php?c=9&key=rm355bo37ah0i1wl88t0je5s',
            # 'http://eleftdating.com/click.php?c=9&key=rm355bo37ah0i1wl88t0je5s',         # Adgaem    star stable Done
            '10002'      : '',
            # 'https://adpgtrack.com/click/5b73d90a6c42607b3b6c4323/199595/subaccount/url=example.com',         # Adpump    GETAROUND
            '10003'      : '',         #UK Swipe   http://im.datingwithlili.com/im/click.php?c=9&key=u5c8f966q7p5u1e2q3978521
            '10004'      : 'http://ares.goldmaketing.com/c/10655/a?clickid=[clickid]&bid=[bid]&siteid=[siteid]&countrycode=[cc]&operatingsystem=[operatingsystem]&campaignid=[campaignid]&category=[category]&connection=[connection]&device=[device]&browser=[browser]&carrier=[carrier]',         # Ad1   opinion outpost   
            '10005'      : '', 
            # 'http://im.datingwithlili.com/im/click.php?c=10&key=sn4qbn9l70tsb1qc14188hly',         # Adsmain Cam4  Done           
            '10006'      : '',         # adpump GETAROUND  https://adpgtrack.com/click/5b73d90a6c42607b3b6c4323/199595/subaccount/url=example.com            
            '10007'      : '',         # IKARIAM
            '10008'      : '',         # IKARIAM
            '10009'      : '',         # IKARIAM  
            '10010'      : '',
            # 'http://im.datingwithlili.com/im/click.php?c=13&key=iz714i80d2sjq9njldkky4f5',
            # 'http://gkd.cooldatingz.com/c/11377/4?clickid=[clickid]&bid=[bid]&siteid=[siteid]&countrycode=[cc]&operatingsystem=[operatingsystem]&campaignid=[campaignid]&category=[category]&connection=[connection]&device=[device]&browser=[browser]&carrier=[carrier]',         # LP            
            '10011'      : '',         # IKARIAM
            '10012'      : '',         # IKARIAM
            '10013'      : '',        # IKARIAM             '10006'      : '',         # LP            
            '10014'      : '',         # IKARIAM
            '10015'      : '',         # IKARIAM
            '10016'      : '',         # IKARIAM             '10006'      : '',         # LP            
            '10017'      : '',         # IKARIAM
            '10018'      : '',         # IKARIAM
            '10019'      : '',         # IKARIAM             '10006'      : '',         # LP            
            '10020'      : '',         # IKARIAM
            '10021'      : '',         # IKARIAM
            '10022'      : ''         # IKARIAM                                               
        }
    }
    return Configs['Delay'],Configs['Config'],Configs['Mission_conf']



