import pymysql


'''
4 accounts for 4 members.
same tables.different db name


'''



def login_sql():
	conn = pymysql.connect(host= '72.11.140.180',port=3306,user='datingwi_root',passwd='XVEp;Er$i8GD')
	cursor = conn.cursor()
	cursor.execute('use datingwi_Emu_multi;')
	# res = cursor.execute('select * from TOKENTABLE;')
	return conn,cursor

def get_tokens():
	# 创建连接
	# conn = pymysql.connect(host= '66.98.122.107',port=3306,user='public',passwd='H8jB3p73Yhy6beyb')
	conn = pymysql.connect(host= '72.11.140.180',port=3306,user='datingwi_root',passwd='XVEp;Er$i8GD')

	# 创建游标
	cursor = conn.cursor()
	# print(conn)
	# print(cursor)

	
	
	
	# 标准操作，获取database里的table
	# cursor.execute('SHOW Databases;')
	# res = cursor.fetchall()
	# for item in res:
	#     print(item)
	#     pass
	# return
	# 执行mysql语句并返回结果,选择database
	cursor.execute('use datingwi_Emu_multi;')
	
	
	# 标准操作，获取database里的table
	# res = cursor.execute('SHOW tables;')
	# res = cursor.fetchall()
	# for item in res:
	#     print(item)
	# return
	
	# 标准操作，查看player表的定义
	# res = cursor.execute('desc TOKENTABLE;')
	# print(res)
	# res = cursor.fetchall()
	# for item in res:
	#     print(item)
	# return
	
	
	
	# res = cursor.execute('select top 1 emailverify,tokentable from lpdata;')
	# res = cursor.execute('select * from emailverify where tokentable=*;')
	res = cursor.execute('select * from TOKENTABLE;')
	res = cursor.fetchall()
	# print(type(res))
	# print(len(res))
	# for item in res:
	#     print(item)
	# print(res)
	return res
	
	# # 把要执行的语句提交，否则无法保存新建或者修改数据
	# conn.commit()
	# # 关闭游标
	# cursor.close()
	# # 关闭连接
	# conn.close()

def login_out_sql(conn,cursor):
	conn.commit()
	# 关闭游标
	cursor.close()
	# 关闭连接
	conn.close()

def create_tokentable():
	conn,cursor = login_sql()
	res = cursor.execute('CREATE TABLE  IF NOT EXISTS TOKENTABLE (id INT,token VARCHAR(100));')
	res = cursor.fetchall()
	for item in res:
	    print(item)	
	login_out_sql(conn,cursor)
	
def upload_tokens(data=None):
	# data = [1111,'1111test-test-test']
	conn,cursor = login_sql()
	content = 'INSERT INTO TOKENTABLE (id,token)VALUES(%d,"%s");'%(data[0],data[1])
	# print(content)
	res = cursor.execute(content)
	res = cursor.fetchall()
	# for item in res:
	#     print(item)	
	login_out_sql(conn,cursor)	

def add_key(table,keys,values):
	conn,cursor = login_sql()
	a = type(1)
	b = type('1')
	content1 = 'CREATE TABLE  IF NOT EXISTS %s (Uuid VARCHAR(50) NULL)'%table
	res = cursor.execute(content1)
	# res.fetchall()
	print(res)
	for i in range(len(keys)):
		if type(values[i]) == b:
			content = 'ALTER table %s ADD %s varchar(50)'%(table,keys[i])
		else :
			content = 'ALTER table %s ADD %s int(30)'%(table,keys[i])
		print(content)
		res = cursor.execute(content)
	return
		# res = cursor.execute(content)
	
	# for item in res:
	#     print(item)	
	login_out_sql(conn,cursor)		

def delete_tokens(data=None):
	data = [494754,477005]
	conn,cursor = login_sql()
	content = 'DELETE FROM TOKENTABLE WHERE id = %d'%data[0]
	res = cursor.execute(content)
	res = cursor.fetchall()	
	content = 'DELETE FROM TOKENTABLE WHERE id = %d'%data[1]
	res = cursor.execute(content)
	res = cursor.fetchall()	

	for item in res:
	    print(item)	
	login_out_sql(conn,cursor)	

def upload_email(data=None):
	# data = [1111,'1111test-test-test']
	conn,cursor = login_sql()
	content = 'INSERT INTO TOKENTABLE (id,token)VALUES(%d,"%s");'%(data[0],data[1])
	# print(content)
	res = cursor.execute(content)
	res = cursor.fetchall()
	# for item in res:
	#     print(item)	
	login_out_sql(conn,cursor)	


def str_test():
	d = [1,'1',1,'1',1]
	a = 'INSERT INTO token (id'+'VALUES('
	type_str = type('1')
	type_int = type(1)
	for item in d:
		b += b


if __name__ == '__main__':
	# add_key('asd',['11','22'])
	str_test()