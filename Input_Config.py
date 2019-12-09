


Input_Config ={
    'firstname' : ['get_name_real'],
    'lastname'  : ['func1','func2'],
    'address'   : []
}


def get_input_config(key):
    global Input_Config
    if key in Input_Config:
        return Input_Config[key]
    else:
        return []
