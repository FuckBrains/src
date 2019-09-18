import sys
def hotupdate(i):
    import db
    db.hotupdate(i)

if __name__ == '__main__':
    paras=sys.argv
    i = int(paras[1])    
    hotupdate(i)