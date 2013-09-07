#!/usr/bin/env python2.6
#this.
#this will do the rdns look up+store
#might look into making htis a class or something?that'd be neat

#okay, lets get this started.
import MySQLdb,os, argparse,socket
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

def rdns_get(addr):
    try:
        return socket.gethostbyaddr(addr)[0]
    except socket.herror:
        return 'NO DNS HERE'

def ipcheck(ip,dns):
    #print "\t" + str(ip) + "\t" + dns
    try:
        dns_ip=socket.gethostbyname_ex(dns)[2]
    except socket.gaierror:
        return "deleted"
    if ip not in dns_ip:
        return "bad"
    else:
        return "good"


#its gonna look kinda similar to hte outputdata.py sinceit pulls from same sources

#this is gonna be controlled by the stats_ip config


con =MySQLdb.connect(mysqlserv,mysqluser,mysqlpass,"db_sshrank")
x=con.cursor()
#get the IPs
x.execute("""SELECT ip, count(*) AS cnt FROM ips_tbl GROUP BY ip ORDER BY cnt DESC LIMIT %s""" %stats_ip)
data=x.fetchall()

#do a loopdaloop; check to see if the ip is alarady in the rdns_tbl
#if it is; check to see when it was last updated; update if old
#if it is not;do rdns, then if:
#                   thre is rdns, check the IP of the name to see if its the same as IP

for a in data:
    print a[0]
    x.execute("""SELECT * FROM rdns_tbl WHERE ip='%s'""" % a[0])
    rdns_data=x.fetchall()
    #if list is empty lets do some things!
    if not rdns_data:
        print 'no daters :('
        #so lets add some
        #take IP, check for rdns:
        rdns=rdns_get(a[0])
        print "\t rdns: " + rdns
        #now make sure its good
        if rdns != 'NO DNS HERE':
            rcheck=ipcheck(a[0],rdns)
        else:
            rcheck='-'
        timenow=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #toss in mysql hell
        x.execute("""INSERT INTO rdns_tbl (ip,rdns,good,datetime) VALUES (%s,%s,%s,%s)""",(a[0],rdns,rcheck,timenow))
        print "========================="
    else:
        print 'YAY DATA'

#code.interact(local=locals())
