#!/usr/bin/env python2.6
import sys,os,pwd,argparse,gzip,time
from datetime import datetime
from multiprocessing import Process
from sqlclass import *
try:
    from ConfigParser import SafeConfigParser
except ImportError as exc:
        sys.stderr.write("Error: failed to import settings module ({})".format(exc))


#set up the config file things

par = SafeConfigParser()
#will be /etc/ssh-rank.ini or whereever you want it
par.read(os.getcwd()+"/config.ini")

authlog=par.get("sshrank","authlogpath")
authname=par.get("sshrank","authname")
userneed=par.get("sshrank","userneed")

mysqluser=par.get("sshrank","mysqluser")
mysqlserv=par.get("sshrank","mysqlserv")
mysqlpass=par.get("sshrank","mysqlpass")

arg=argparse.ArgumentParser()
arg.add_argument('-f', action='store', dest='firstrun', default='off', help='set first run(default off), do -f on')
arg.add_argument('-w', action='store', dest='watch', default='off', help='set to start watching (default off), do -w on')
arg.add_argument('-r', action='store', dest='resume', default='off', help='if you\'ve already done -f and -w, and some reason stopped it, use -r on to have it resume. note: probably wont work if log rotate went')
year="2013"


print pwd.getpwuid(os.getuid())[0]
if userneed != pwd.getpwuid(os.getuid())[0]:
    print "please run as "+userneed
    sys.exit(1)

def datafromline(line,year):
    #returns [date, user, ip]
    returnlist=[]
    l=filter(None,line.split(" "))
    date=l[0]+" "+l[1]+" "+year+" "+l[2] #Sep 4 2013 19:31:55
    date=datetime.strptime(date,"%b %d %Y %H:%M:%S")
    date=date.strftime('%Y-%m-%d %H:%M:%S')
    user=line[line.find("user ")+5:line.find(" from")]
    ip=line[line.find("from ")+5:line.find(" port")]
    returnlist.append(ip)
    returnlist.append(user)
    returnlist.append(date)
    return returnlist


def insertsql(i):
    user=ips(i[0],i[1],i[2])
    Session.add(user)
    Session.commit()

def openfile(logfile):
    if 'gz' in logfile:
        celery = gzip.open(logfile, 'r')
    else:
        celery = open(logfile, 'r')
    return celery

def follow(thefile):
    thefile.seek(0,2)      # Go to the end of the file
    while True:
         line = thefile.readline()
         if not line:
             time.sleep(0.1)    # Sleep briefly
             continue
         yield line


argres = arg.parse_args()
if argres.firstrun == "on":
    print "doing 1st run! yay!"
    log_list=[]
    for files in os.listdir(authlog):
        if authname in files:
            log_list.append(authlog+files)

    #we gonna need to loooooopdaloop the files :3
    #i'll deal with gzip'd
    #and for this i'll just be doing one auth.log
    #disco dance!
    for afile in log_list:
        start_time = time.time()
        for line in openfile(afile):
            if "Failed password for invalid user" in line:
                data=datafromline(line,year)
                #Process(target=insertsql,args=(data,)).start()
                insertsql(data)
        end_time = time.time()
        print("Elapsed time was %g seconds" % (end_time - start_time))

if argres.resume == 'on':
    print "Resuming from last:"
    last=Session.query(ips).order_by(ips.pk.desc()).first() 
    print "\tlast entry is:" +str(last)
    print "\t "+str(last.dtime)
    for line in openfile('/var/log/auth.log'):
        if "Failed password for invalid user" in line:
            data=datafromline(line,year)
            #now take the last attempt in DB date; and if the line is newer, add to DB
            if datetime.strptime(data[2],'%Y-%m-%d %H:%M:%S') > last.dtime:
                insertsql(data)


if argres.watch == "on":
    print "\n\n==========Now Watching the logfile========"
    #later to just be a var or something, but meh
    loglines=follow(open("/var/log/auth.log"))
    for line in loglines:
        if "Failed password for invalid user" in line:
            data=datafromline(line,year)
            print str(data)
            #Process(target=insertsql,args=(data,)).start()
            insertsql(data)


