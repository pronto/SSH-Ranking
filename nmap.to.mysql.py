#!/usr/bin/env python2.7
import sys,os,pwd,argparse,gzip,time
from datetime import datetime
from multiprocessing import Process
from sqlclass import *
import re
try:
    from ConfigParser import SafeConfigParser
except ImportError as exc:
        sys.stderr.write("Error: failed to import settings module ({})".format(exc))


#set up the config file things

par = SafeConfigParser()
#will be /etc/ssh-rank.ini or whereever you want it
par.read(os.getcwd()+"/config.ini")


mysqluser=par.get("sql","sqluser")
mysqlserv=par.get("sql","sqlserv")
mysqlpass=par.get("sql","sqlpass")

arg=argparse.ArgumentParser()
arg.add_argument('-f', action='store', dest='nfile', default='showhelp', help='the file name, put it here')
argres = arg.parse_args()
#def insert_portsql(ip,dtime,portnum,state,proto,service,verinfo):
def insert_portsql(insertline):
    # nmapinsert=nmapSQL(ip,dtime,portnum,state,proto,service,verinfo)
    sqlsess.add(nmapinser)
    sqlsess.commit()


gnmap=open(argres.nfile, 'r').readlines()
#port number, State, Protocol, Owner, Service, SunRPC info, Version info
ddate=re.search(r'initiated (.*?)as',gnmap[0]).group(0).replace(' as','').replace('initiated ','')
ddate=datetime.strptime(ddate,"%a %b %d %H:%M:%S %Y")
ddate=ddate.strftime('%Y-%m-%d %H:%M:%S')

ip=re.search(r'Host: (.*?)\(',gnmap[1]).group(0).replace('Host: ','').replace(' (','')
nsplit=gnmap[2].split('Ports: ')[1].split(', ')
for a in nsplit:
    b = a.split(',')
    for c in b:
        d=c.split('/')
        print "port:\t" + d[0],
        print "| state:\t" + d[1],
        print "| proto:\t" + d[2],
        print "| serv:\t" + d[4],
        print "| verinfo:\t" + d[6]
        #ip, dtime, portnum, state, proto, service, verinfo)
        insertstuff=nmapSQL(ip, ddate, d[0], d[1], d[2], d[4], d[6])
        #                   ip  time  port# state proto serv   ver
        #                   1    2     3     4     5     6       7
        #print insertstuff
        sqlsess.add(insertstuff)
sqlsess.commit()
