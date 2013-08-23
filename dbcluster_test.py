#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys,string,time,random

#query interval in second
query_interval=0.00

#User input
if len(sys.argv)!=5:
	print sys.argv[0]+" IP/Domainname user password dbname"
	exit(0)
db_host=sys.argv[1]
db_user=sys.argv[2]
db_password=sys.argv[3]
db_name=sys.argv[4]

#Create a random table
db_table=''.join(random.sample(string.ascii_letters + string.digits, 16))
con = mdb.connect(db_host,db_user,db_password,db_name)
cur = con.cursor()
if cur.execute("SHOW TABLES LIKE '"+db_table+"'"):
	print "FATAL:Table '"+db_table+"' has aready existed in database '"+db_name+"', can not continue safely. Please check and drop test.test manually"	
	exit(1)
ret=cur.execute("CREATE TABLE IF NOT EXISTS "+db_table+"(id int(16),name varchar(32))")

#Start testing
fail_count = 0
for i in range(1,1000):
	rand_value=''.join(random.sample(string.ascii_letters + string.digits, 16))
	cur.execute("insert into "+db_table+" values('"+str(i)+"','"+rand_value+"')")
	con.commit()
	con1 = mdb.connect(db_host,db_user,db_password,db_name)
	cur1 = con1.cursor()
	sql = "select * from "+db_table+" where name='"+rand_value+"'"
	time.sleep(query_interval)
	cur1.execute(sql)
	#print cur1.fetchone()
	if not cur1.fetchone():
		print str(i)+": NO"
		fail_count += 1

#Clean up
cur.execute("drop table "+db_table+"")
con.commit()
con.close()
con1.close()

#Print result in terms of failures per k queries
print "%d/1000 queries failed " % fail_count
