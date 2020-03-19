import db
import test
import ssn_detect
import Chrome_driver
from time import sleep

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


def main():
    # test_10088()
    # test.test_write()
    # email = 'karlmalfeld@hotmail.com'
    # email=''
    # ssn_detect.validate_10088_email(email)
    # routing = '2857880817'
    # ssn_detect.validate_routing(routing)
    Address = '1234 stratford av apt 7a'
    ZipCode = 10472 
    ssn_detect.validate_address(Address,ZipCode)

if __name__ == '__main__':
    test_2()