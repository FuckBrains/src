import db
import test
import ssn_detect
import Chrome_driver
from time import sleep
import random

def test_1():
    Mission_Id =10095
    pages = db.get_page_flag(Mission_Id)
    print(pages)

def test_10088():
    email = 'karlmalfeld@hotmail.com'    
    ssn_detect.validate_10088_email(email)

def test_2():
    chrome_driver = Chrome_driver.get_chrome()
    url = 'http://falbk.top/click.php?c=5&key=yift22rta15kfnq9upqfowq9'
    chrome_driver.get(url)
    sleep(1000)

def test_3():
    sql_content = 'Select Basicinfo_Id,home_phone,work_phone from Basicinfo where Excel_name="Us_pd_native"'
    response = db.Execute_sql_single([sql_content])    
    # print(response)
    excels = [[key[0],key[1]] for key in response[0] if key[1]==key[2]]
    print(excels)
    print(len(excels))
    sql_contents = []
    for key in excels: 
        phone = key[1]
        for i in range(15):
            num = random.randint(0,9) 
            if int(phone[-3])!= num:
                print(phone[-3],num)
                phone = phone[:-3]+str(num)+phone[-2:]
                print(phone)
                break
        sql_content = "UPDATE Basicinfo SET work_phone = %s WHERE Basicinfo_Id = '%s'" % (phone,key[0])
        sql_contents.append(sql_content)
    db.Execute_sql(sql_contents)    
    # print(excels)
    # sql_contents = []
    # for excel in excels:
    #     sql_content = 'SELECT * from BasicInfo  WHERE Excel_name = "%s"'%excel
        
    #     response = db.Execute_sql_single(sql_content)



def main():
    # test_10088()
    # test.test_write()
    email = 'ricdevin@yahoo.com'
    # email=''
    # ssn_detect.validate_10088_email(email)
    # routing = '2857880817'
    # ssn_detect.validate_routing(routing)
    Address = '237 BURNING TREE DRIVE'
    ZipCode = 95119
    ssn_detect.validate_address(Address,ZipCode)

if __name__ == '__main__':
    main()