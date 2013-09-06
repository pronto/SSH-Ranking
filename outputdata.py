#!/usr/bin/env python2.6
import MySQLdb,os
from ConfigParser import SafeConfigParser


par = SafeConfigParser()
#will be /etc/ssh-rank.ini or whereever you want it
par.read(os.getcwd()+"/config.ini")

mysqluser=par.get("sshrank","mysqluser")
mysqlserv=par.get("sshrank","mysqlserv")
mysqlpass=par.get("sshrank","mysqlpass")


con =MySQLdb.connect(mysqlserv,mysqluser,mysqlpass,"db_sshrank")
x=con.cursor()
x.execute("""SELECT ip, count(*) AS cnt FROM ips_tbl GROUP BY ip ORDER BY cnt DESC LIMIT 10""")
data=x.fetchall()
for a in data:
    x.execute("""SELECT user, count(*) as cnt FROM ips_tbl WHERE IP='%s' GROUP BY user ORDER BY cnt DESC LIMIT 10""" %a[0])
    heh=x.fetchall()
    print a[0] + " attempted " + str(a[1]) + " times with users: "
    print "\t",
    for b in heh:
        print b[0] + ":" + str(b[1]) + ", ",
    print " "
