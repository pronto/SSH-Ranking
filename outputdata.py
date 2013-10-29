#!/usr/bin/env python2.6
import os
from ConfigParser import SafeConfigParser
from datetime import datetime
par = SafeConfigParser()
#will be /etc/ssh-rank.ini or whereever you want it
par.read(os.getcwd()+"/config.ini")
mysqluser=par.get("sshrank","mysqluser")
mysqlserv=par.get("sshrank","mysqlserv")
mysqlpass=par.get("sshrank","mysqlpass")
user_cnt=int(par.get("sshrank","user_cnt"))
total_ip=par.get("sshrank","total_ip")
stats_ip=par.get("sshrank","stats_ip")

from sqlclass import *

uniq_ips=Session.query(ips.ip,func.count(ips.ip).label('total')).group_by(ips.ip).order_by('total DESC').limit(int(total_ip)).all()

for a in uniq_ips:
    date=Session.query(ips.datetime).filter(ips.ip==a[0]).order_by(-ips.pk).limit(1).scalar()
    date=datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S')
    date=date.strftime('%Y-%m-%d %H:%M:%S')
    print "\033[1m"+a[0] + "\033[0m attempted \033[1m" + str(a[1]) + "\033[0m Last Attempt: \033[1m"+ date+" \033[0mtimes with users: "
    print '\t',
    users = Session.query(ips.user,func.count(ips.user).label('total')).\
            filter(ips.ip==str(a[0])).group_by(ips.user).order_by('total DESC').limit(user_cnt).all()
    for b in users:
        print "\033[1m"+b[0] + "\033[0m:" + str(b[1]) + ", ",
    print ' \n'
#code.interact(local=locals())
