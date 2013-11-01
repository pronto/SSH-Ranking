#!/usr/bin/env python2.6
from flask import Flask, render_template, send_from_directory, request
import socket,os,sys
from datetime import datetime,timedelta
from datetime import date as ddate
from ConfigParser import SafeConfigParser
par = SafeConfigParser()
#will be /etc/ssh-rank.ini or whereever you want it
par.read(os.getcwd()+"/config.ini")
from flask.ext.sqlalchemy import SQLAlchemy
import code

from sqlclass import *

mysqluser=par.get("sshrank","mysqluser")
mysqlserv=par.get("sshrank","mysqlserv")
mysqlpass=par.get("sshrank","mysqlpass")
user_cnt=int(par.get("sshrank","user_cnt"))
total_ip=par.get("sshrank","total_ip")
stats_ip=par.get("sshrank","stats_ip")
socket.setdefaulttimeout(3)


def getlastattempt(ip):
    Session.query(ips.datetime).filter(ips.ip==ip).order_by(-ips.pk).limit(1).scalar()
    date=datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S')
    return date.strftime('%Y-%m-%d %H:%M:%S')


app=Flask(__name__)
#app.debug=True

#date=Session.query(ips.dtime).filter(ips.ip==a[0]).order_by(-ips.pk).limit(1).scalar()
#date=datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S')
#date=date.strftime('%Y-%m-%d %H:%M:%S')
#

@app.route('/')
def main():
    userlist=[]
    datelist=[]
    deltime=[]
    uniq_ips=Session.query(ips.ip,func.count(ips.ip).label('total')).group_by(ips.ip).order_by('total DESC').limit(int(total_ip)).all()
    for ip in uniq_ips:
        users = Session.query(ips.user,func.count(ips.user).label('total')).filter(ips.ip==str(ip[0])).group_by(ips.user).order_by('total DESC').limit(user_cnt).all()
        date=Session.query(ips.dtime).filter(ips.ip==ip[0]).order_by(-ips.pk).limit(1).scalar()
        date=datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S')
        date=date.strftime('%Y-%m-%d %H:%M:%S')
        #ip.append(date)
        datelist.append((ip[0],date))
        deltime.append(date)
        for user in users:
            userlist.append((ip,user[0],user[1]))
    alldns=Session.query(rdns).all()
    newest=max(deltime)
    return render_template('main.html',uniq_ips=uniq_ips,userlist=userlist,alldns=alldns,datelist=datelist,newest=newest)



@app.route('/new')
def new():
    #things
    return render_template('new.html')


@app.route('/week')
def week():
    userlist=[]
    datelist=[]
    deltime=[]
    lastweek=datetime.today()-timedelta(7)
    uniq_ips=Session.query(ips.ip,func.count(ips.ip).label('total')).group_by(ips.ip).\
            order_by('total DESC').filter(ips.dtime >= lastweek).limit(int(total_ip)).all()
    for ip in uniq_ips:
        users = Session.query(ips.user,func.count(ips.user).label('total')).filter(ips.ip==str(ip[0])).group_by(ips.user).order_by('total DESC').limit(user_cnt).all()
        date=Session.query(ips.dtime).filter(ips.ip==ip[0]).order_by(-ips.pk).limit(1).scalar()
        date=datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S')
        date=date.strftime('%Y-%m-%d %H:%M:%S')
        #ip.append(date)
        datelist.append((ip[0],date))
        deltime.append(date)
        for user in users:
            userlist.append((ip,user[0],user[1]))
    alldns=Session.query(rdns).all()
    newest=max(deltime)
    return render_template('week.html',uniq_ips=uniq_ips,userlist=userlist,alldns=alldns,datelist=datelist,newest=newest)



if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
