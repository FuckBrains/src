hotupdate_content = {
	1 : ["ALTER TABLE Mission ADD Alliance VARCHAR(100) AFTER Mission_Id;","ALTER TABLE Mission ADD Account VARCHAR(100) AFTER Mission_Id;","ALTER TABLE Plans ADD Account VARCHAR(50) AFTER Alliance;"],
	2 : ['delete from email WHERE status = "Bad"'],
	3 : ["ALTER TABLE Mission ADD ua VARCHAR(500) DEFAULT '' AFTER BasicInfo_Id"],
	4 : ["ALTER TABLE Mission ADD activate3 VARCHAR(100) DEFAULT '' AFTER create_time" ,"ALTER TABLE Mission ADD activate2 VARCHAR(100) DEFAULT '' AFTER create_time","ALTER TABLE Mission ADD activate1 VARCHAR(100) DEFAULT '' AFTER create_time"],
	5 : ["ALTER TABLE plans CHANGE prot_lpm port_lpm VARCHAR(50)"],











}


def get_contents(i):
	return hotupdate_content[i]


if __name__ == '__main__':
	content1 = get_contents(1)
	print(content1)