import random
import time
import datetime
import calendar
import db


def get_month_config():
    year = datetime.datetime.now().year    
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day    
    # print(year,month,day)    
    monthRange = calendar.monthrange(year,month)
    # print(monthRange)
    # days = calendar.mdays
    # print(datetime.datetime.now().weekday()+1)
    return monthRange[1]


    # print(calendar.mdays)

def time_choose():
    time.time()


def gen_num(num):
    plans = []
    for i in range(num):
        plan = random.randint(3,13)
        plans.append(plan)
    return plans

def main():
    plans = gen_num(2)
    print(plans)

def get_city():
    pass

def country_hour_config():
    hour_config = {
    'de':[0,1,2,3,4,5,6,14,15,16,17,18,19,20,21,22,23]
    }
    return hour_config

def get_mission_config():
    # mission_config = {
    # '10081':{'Execute_time_all':'0,6','Execute_time_daily':'2','Price':'15,75'},
    # '10082':{'Execute_time_all':'0,6','Execute_time_daily':'2','Price':'60'},    
    # '10083':{'Execute_time_all':'0,6','Execute_time_daily':'2','Price':'45'},        
    # }
    alliance = 'aklamio'
    account = 'de4'
    links = db.get_plan_config(alliance,account)
    # print(links)
    mission_ids = []
    for item in links:
        mission_id = item['mission_id']
        mission_ids.append(mission_id)
    offer_configs = db.get_offer_config_all()
    # print(offer_configs[0])
    mission_config = {}
    for mission_id in mission_ids:
        for item in offer_configs:
            if item['Mission_Id'] == mission_id:
                mission_config[mission_id] = item
    print(mission_config)
    return mission_config

def get_plan_config():
    pass


def gen_plan():
    plan = {}
    mission_config = get_mission_config()
    days = get_month_config()   
    for mission_id in mission_config:
        # print(plan)
        if mission_config[mission_id]['Execute_time_all'] == None:
            continue
        if ',' in mission_config[mission_id]['Execute_time_all']:
            exe_time_range = mission_config[mission_id]['Execute_time_all'].split(',')
            mission_exe_time = random.randint(int(exe_time_range[0]),int(exe_time_range[1]))
            print(mission_id,mission_exe_time)
            for i in range(mission_exe_time):
                day = random.randint(1,int(days))
                if str(day) not in plan:
                    plan[str(day)] = {}
                    plan[str(day)][mission_id] = 1
                else:
                    if mission_id not in plan[str(day)]:
                        plan[str(day)][mission_id] = 1
                        continue
                    if plan[str(day)][mission_id]>=int(mission_config[mission_id]['Execute_time_daily']):
                        continue
                    else:
                        plan[str(day)][mission_id] = +1
    hour_config = country_hour_config()
    for day in plan:
        for mission_id in plan[day]:
            hours = hour_config['de']
            hour_config_exe = []
            for num_mission_id in range(plan[day][mission_id]):
                time_hour = random.randint(0,len(hours)-1)
                minute = random.randint(0,5)
                # print(hours[time_hour])
                hour_config_exe.append({str(hours[time_hour]):minute})
            plan[day][mission_id] = hour_config_exe 
    # plan = {
    # '2':{'10081':1,'10082':0,'10083':1},    
    # '3':{'10081':1,'10082':0,'10083':1},
    # '4':{'10081':1,'10082':1,'10083':0},
    # }
    print(plan)
    plans = {}
    for i in sorted(plan.keys()) : 
        print(i)
        # print((i, plan[i]), end =" ") 
        plans[str(i)] = plan[i]
    print('==================')
    print(plans)
    print('==================')    
    price = 0
    for day in plan:
        for mission_id in plan[day]:
            price_set = mission_config[mission_id]['Price']
            if ',' in price_set:
                price_set = price_set.split(',')[0]
            price += float(price_set)*len(plan[day][mission_id])
    print(price)

def takeStep(elem):
    return elem['Step']

if __name__ == '__main__':
    gen_plan()