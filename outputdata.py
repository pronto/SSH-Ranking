#!/usr/bin/env python2.6
import MySQLdb,os, argparse
from ConfigParser import SafeConfigParser
from datetime import datetime
import code


par = SafeConfigParser()
#will be /etc/ssh-rank.ini or whereever you want it
par.read(os.getcwd()+"/config.ini")

mysqluser=par.get("sshrank","mysqluser")
mysqlserv=par.get("sshrank","mysqlserv")
mysqlpass=par.get("sshrank","mysqlpass")

user_cnt=int(par.get("sshrank","user_cnt"))
total_ip=par.get("sshrank","total_ip")
stats_ip=par.get("sshrank","stats_ip")



con =MySQLdb.connect(mysqlserv,mysqluser,mysqlpass,"db_sshrank")
x=con.cursor()
#get the IPs
x.execute("""SELECT ip, count(*) AS cnt FROM ips_tbl GROUP BY ip ORDER BY cnt DESC LIMIT %s""" %total_ip)
data=x.fetchall()
for a in data:
    #get the users
    x.execute("""SELECT user, count(*) as cnt FROM ips_tbl WHERE IP='%s' GROUP BY user ORDER BY cnt DESC LIMIT %s""" %(a[0], user_cnt))
    users=x.fetchall()
    x.execute("""SELECT ip,datetime from ips_tbl WHERE ip='%s' ORDER by datetime DESC LIMIT 1;""" % a[0])
    date=x.fetchall()
    date=datetime.strptime(str(date[0][1]),'%Y-%m-%d %H:%M:%S')
    date=date.strftime('%Y-%m-%d %H:%M:%S')
    print "\033[1m"+a[0] + "\033[0m attempted \033[1m" + str(a[1]) + "\033[0m Last Attempt: \033[1m"+ date+" \033[0mtimes with users: "
    print "\t",
    for b in users:
        print "\033[1m"+b[0] + "\033[0m:" + str(b[1]) + ", ",
    print ""
    #check for rdns:
    x.execute("""SELECT * FROM rdns_tbl WHERE ip='%s'""" % a[0])
    rdnsthings=x.fetchall()
    if rdnsthings:
        for rd in rdnsthings:
            if rd[1] != 'NO DNS HERE':
                print "\trDNS: \033[1m" + rd[1] +"\033[0m",
                print "and the dns is: \033[1m" + rd[2] + "\033[0m",
                print "last updated on \033[1m"+  str(rd[3]) + "\033[0m"
                #if a[0] == '203.69.37.205':
                 #   code.interact(local=locals())
        print ""
