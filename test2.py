import db

def test_1():
    Mission_Id =10095
    pages = db.get_page_flag(Mission_Id)
    print(pages)

def main():
    test_1()

if __name__ == '__main__':
    main()