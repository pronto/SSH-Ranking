#!/usr/bin/env python2.7
#this.
#this will do the rdns look up+store
#might look into making htis a class or something?that'd be neat

#okay, lets get this started.
import os, argparse,socket,time
from ConfigParser import SafeConfigParser
from datetime import datetime
import code

from sqlclass import *


par = SafeConfigParser()
#will be /etc/ssh-rank.ini or whereever you want it
par.read(os.getcwd()+"/config.ini")

mysqluser=par.get("sql","sqluser")
mysqlserv=par.get("sql","sqlserv")
mysqlpass=par.get("sql","sqlpass")

user_cnt=int(par.get("web","user_cnt"))
total_ip=par.get("web","total_ip")
stats_ip=par.get("web","stats_ip")

rdns_age =int(par.get("web","rdns_age"))

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


def insertsql_dns(i):
    rd=rdns(i[0],i[1],i[2],i[3])
    sqlsess.add(rd)
    sqlsess.commit()

def rdns_into_db(ip,run):
    #run is either 'first' or the rdns
    print "\n\n\n\t=====start of rdns into db func====="
    rdns=rdns_get(ip)
    print "\t rdns: " + rdns
    #now make sure its good
    if rdns != 'NO DNS HERE':
        rcheck=ipcheck(ip,rdns)
    else:
        rcheck='-'
    timenow=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print "\t == rcheck is:\t " + rcheck
    print "\t == run is:\t" + run
    #toss in mysql hell
    if run == 'first':
        insertsql_dns((ip,rdns,rcheck,timenow))
    else:
        if rdns != run:
            #x.execute("""INSERT INTO rdns_tbl (ip,rdns,good,datetime) VALUES (%s,%s,%s,%s)""",(a[0],rdns,rcheck,timenow))
            #insert=rdns(ip,rdns,rcheck,timenow)
            insertsql_dns((ip,rdns,rcheck,timenow))
    print "========================="

#do a loopdaloop; check to see if the ip is alarady in the rdns_tbl
#if it is; check to see when it was last updated; update if old
#if it is not;do rdns, then if:
#                   thre is rdns, check the IP of the name to see if its the same as IP


#data = sqlsess.query(ips).order_by(-ips.pk).limit(stats_ip).all()
data = sqlsess.query(ips.ip,ips.dtime,func.count(ips.ip).\
        label('total')).group_by(ips.ip).order_by('total DESC').limit(int(total_ip)).all()
for line in data:
    print "================== "+line.ip +" start of FOR LOOP==========================="
    #x.execute("""SELECT * FROM rdns_tbl WHERE ip='%s'""" % a[0])
    #rdns_data=x.fetchall()
    #
    rdns_data=sqlsess.query(rdns).order_by(-rdns.pk).filter(rdns.ip==line.ip).limit(1).scalar()
    print rdns_data
    #if list is empty lets do some things!
    if not rdns_data:
        print 'no daters :('
        print str(line.ip) + "======================="
        #so lets add some
        #take IP, check for rdns:
        rdns_into_db(line.ip,'first')
    else:
        print 'okay'
        print '---;---;;'
        #so there's already an entry for rdns
        #we wanna get when it was last updated and compare :D
        elasped=int(time.time()) -  int(rdns_data.dtime.strftime("%s"))
        #print elasped +","+rdns_age
        if elasped > rdns_age:
            print 'update bro'
            rdns_into_db(line.ip,rdns_data.rdns)
        print "=============================+"
        #comparethedate

#code.interact(local=locals())

