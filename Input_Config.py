


Input_Config ={
    'firstname' : ['get_name_real'],
    'first_name' : ['get_name_real'],    
    'lastname'  : ['get_name_real'],
    'last_name'  : ['get_name_real'],    
    'address'   : ['apt_get'],
    'homephone' : ['get_phone'],
    'zip'       : ['get_zip'],
    'dateofbirth' : ['get_birthday_mm','get_birthday_dd','get_birthday_year','get_birthday_all'],    
    'email'     : ['select_email_type'],
    'cvv'          : ['cvv_get'],
    'katou'     : ['get_zip']
}

Select_Config ={
    'state'       : ['get_name_real'],
    'dateofbirth' : ['get_birthday_mm','get_birthday_dd','get_birthday_year','get_birthday_all'],
}

Geberate_Config = {
    'dateofbirth' : ['get_birthday_mm','get_birthday_dd','get_birthday_year'],    
    'pwd'         : ['password_get','password_get_Nostale'],        
    'height'      : ['get_height_ft','get_height_inch','get_height_weight']    
}


def get_input_config(key):
    global Input_Config
    print('Input_Config:',Input_Config)
    if key in Input_Config:
        print('Input_Config[key]:',Input_Config[key])
        return Input_Config[key]
    else:
        print('Input_Config[key]:=====[]')        
        return []


def get_select_config(key):
    global Select_Config
    if key in Select_Config:
        print('Input_Config[key]:',Select_Config[key])
        return Select_Config[key]
    else:
        # print('Input_Config[key]:=====[]')        
        return []

def get_generate_config(key):
    global Geberate_Config
    if key in Geberate_Config:
        print('Input_Config[key]:',Geberate_Config[key])
        return Geberate_Config[key]
    else:
        # print('Input_Config[key]:=====[]')        
        return []

def get_generate_items():
    global Geberate_Config
    return Geberate_Config    