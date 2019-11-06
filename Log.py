import db
import json
import datetime

def Read_Ini(file):
    submits = []
    with open(file,'r') as f:
        jss = f.readlines()
        # print(jss)
        for js in jss:
            js = js.strip('\n')
            submit = json.loads(js)
            submits.append(submit)
            # print(submit)
    if len(submits) >= 1:
        return submits
    else:
        return []

def Write_Ini(file,contents):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    content_ = ''
    with open(file,'w+') as f:
        for content in contents:
            content_ += json.dumps(content) 
            content_ += '\n'
        f.write(content_)

def read_plans_tolog(month):
    path_log = r'../Log.txt'
    plans_log = Read_Ini(path_log)
    # print(plans_log)
    a = len(plans_log)
    print('Already ',a,'plans in log')
    plans = db.read_plans(-1)
    # print(plans[0])
    plans = [plan for plan in plans if plan['Alliance'] != 'Test']
    for plan in plans:
        plan['create_time'] = str(plan['create_time'])
    urls = []
    for plan in plans_log:
        if plan['url_link'] not in urls:
            urls.append(plan['url_link'])
    for plan in plans:
        if plan['url_link'] not in urls:
            print('New added plan',plan)
            plans_log.append(plan)
    print('Total:',len(plans_log) - a,'plans added')
    Write_Ini(path_log,plans_log)


def main():
    month = 11
    read_plans_tolog(month)

if __name__ == '__main__':
    main()