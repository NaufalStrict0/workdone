#!/usr/bin/env python
#juliver_sihombing@pinisi-elektra.com
#14-02-2014
#---------------

import sys
import os
import datetime

import csv
import MySQLdb

#set penamaan file (format Victoria_(Day-1).csv)
now=datetime.datetime.now()
now -= datetime.timedelta(days=1)
tTime=now.strftime("%Y%m%d")
FILENAME="/home/data/ichibansushitm_pgk_" + tTime + ".csv"

#set konfigurasi database
hostname="192.168.8.138"
dbuser="bri"
dbpass="bri"
dbname="db_ichiban"

#set Query String
#SELECTQ="select pscd,trdt,trno,rvnamt,svchgamt,taxamt from iafjrndt where active='1' and svchgamt>'0' and taxamt>'0' and date(trdt)=curdate() - interval 1 day order by pscd"
#SELECTQ="select id_nota, tgl_nota, jam_pesan, sub_tot, dis, service, tax, grand from nota where date(tgl_nota)>=curdate() - interval 41 day order by tgl_nota asc"
#SELECTQ="select * from tbl_transactions"
SELECTQ="select invoice_id,closedTime,subtotal,discountAmount,serviceChargeAmount,tax1Amount from tbl_transactions where date(closedTime)between subdate(curdate(),3) AND subdate(curdate(),1) order by closedTime desc"

#SELECTQ="select invoice_id,closedTime,subtotal,discountAmount,serviceChargeAmount,tax1Amount from tbl_transactions where year(closedTime)=2024 and month(closedTime)=06 order by closedTime desc"

#open connection to database
db = MySQLdb.connect(host=hostname, user=dbuser, passwd=dbpass, db=dbname, port=3306)

#prepare csv file
dump_writer = csv.writer(open(FILENAME,'w'), delimiter=',',quotechar="'")
cursor = db.cursor()
#execute query, fetching data row
cursor.execute(SELECTQ)
result = cursor.fetchall()

#get column names
field_names = [i[0] for i in cursor.description]
dump_writer.writerow(field_names)
#dump to csv
#data = [row[0] for row in cursor.fetchall()]
for record in result:
    dump_writer.writerow(record)

#close connection
db.close()

