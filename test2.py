import db
import test
import ssn_detect

def test_1():
    Mission_Id =10095
    pages = db.get_page_flag(Mission_Id)
    print(pages)

def main():
    test.test_write()
    # email = 'lokin22@hotmail.com'
    # ssn_detect.validate_10088_email(email)
    # routing = '2857880817'
    # ssn_detect.validate_routing(routing)

if __name__ == '__main__':
    main()