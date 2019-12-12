


Input_Config ={
    'firstname' : ['get_name_real'],
    'lastname'  : ['func1','func2'],
    'address'   : [],
    'homephone' : ['get_phone'],
    'zip'       : ['get_zip']
}


def get_input_config(key):
    global Input_Config
    if key in Input_Config:
        print('Input_Config[key]:',Input_Config[key])
        return Input_Config[key]
    else:
        print('Input_Config[key]:=====[]')        
        return []
