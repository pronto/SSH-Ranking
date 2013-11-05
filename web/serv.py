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
def killtuple(lista):
    listb=[]
    for a in lista:
        listb.append(a[0])
    return listb

#im not even sure wtf im doing...neat i think?
def tree_finder(thing):
    #lets just do it with start from ip
    list_ips=[]
    #make sure its a real ip...
    uniq_ips=killtuple(Session.query(ips.ip).distinct())
    if thing in uniq_ips:
        #get the users
        users = killtuple(Session.query(ips.user).filter(ips.ip==str(thing)).distinct())
        for user in users:
            list_ips.append([user,killtuple(Session.query(ips.ip).filter(ips.user==str(user)).distinct())])
        return list_ips
    else:
        return 'nope'


def tree_user(user):
    list_user=[]
    uniq_user=killtuple(Session.query(ips.user).distinct())
    if user in uniq_user:
        iplist = killtuple(Session.query(ips.ip).filter(ips.user==str(user)).distinct())
        for ip in iplist:
            list_user.append([ip,killtuple(Session.query(ips.user).order_by(ips.user).filter(ips.ip==str(ip)).distinct())])
        return list_user
    else:
        return 'nope'

app=Flask(__name__)
#app.debug=True

#date=Session.query(ips.dtime).filter(ips.ip==a[0]).order_by(-ips.pk).limit(1).scalar()
#date=datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S')
#date=date.strftime('%Y-%m-%d %H:%M:%S')
#

@app.route('/')
def main():
    subhead="main"
    return render_template('main.html',subhead=subhead)

@app.route('/ssh_rank/lists/<time>')
def list_test(time):
    userlist=[]
    datelist=[]
    deltime=[]
    if time == 'week':
        lastweek=datetime.today()-timedelta(7)
        uniq_ips=Session.query(ips.ip,func.count(ips.ip).label('total')).group_by(ips.ip).order_by('total DESC').filter(ips.dtime >= lastweek).limit(int(total_ip)).all()
    elif time == 'all':
        uniq_ips=Session.query(ips.ip,func.count(ips.ip).label('total')).group_by(ips.ip).order_by('total DESC').limit(int(total_ip)).all()
    elif time == '30day':
        lastweek=datetime.today()-timedelta(30)
        uniq_ips=Session.query(ips.ip,func.count(ips.ip).label('total')).group_by(ips.ip).order_by('total DESC').filter(ips.dtime >= lastweek).limit(int(total_ip)).all()
    elif time == '24hr':
        lastweek=datetime.today()-timedelta(3)
        uniq_ips=Session.query(ips.ip,func.count(ips.ip).label('total')).group_by(ips.ip).order_by('total DESC').filter(ips.dtime >= lastweek).limit(int(total_ip)).all()
    else:
        return render_template('404.html'),404

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
    return render_template('page_for_listings_main.html',uniq_ips=uniq_ips,userlist=userlist,alldns=alldns,datelist=datelist,newest=newest,subhead=time)

@app.route('/ssh_rank/users')
def all_user():
    users=killtuple(Session.query(ips.user).order_by(ips.user).distinct())
    return render_template('all_users.html',users=users, subhead='userlist')


@app.route('/ssh_rank/ip_info/<ip>')
def ip_info(ip):
    iplist=Session.query(ips.ip).distinct().all()
    if any(b[0] == ip for b in iplist):
        users = Session.query(ips.user,func.count(ips.user).label('total')).filter(ips.ip==str(ip)).group_by(ips.user).order_by('total DESC').all()
        dates=killtuple(Session.query(ips.dtime).filter(ips.ip==str(ip)).order_by(ips.dtime).all())
        return render_template('ip_info.html',subhead='ipinfo', ip=ip,users=users, dates=dates)
    else:
        return render_template('404.html'),404

@app.route('/ssh_rank/users/<user>')
def userpage(user):
    users = killtuple(Session.query(ips.user).distinct())
    if str(user) in users:
        other_ips=killtuple(Session.query(ips.ip).filter(ips.user==str(user)).distinct())
        return render_template('user_info.html',subhead='users',user=user, other_ips=other_ips)
    else:
        return render_template('404.html'),404

@app.route('/testing/<user>')
def testuser(user):
    if ',' in user:
        user_list= user.split(",")
        return render_template("test.user.html",user_list=user_list)

@app.route('/ssh_rank/tree/<ttype>/<thing>')
def tree(ttype,thing):
    if ttype == 'ip':
        tree = tree_finder(str(thing))
        if tree is not 'nope':
            return render_template('tree.html', subhead='tree',tree=tree, ip=str(thing))
        else:
            return render_template('404.html'),404
    elif ttype == 'user':
        tree = tree_user(str(thing))
        if tree is not 'nope':
            return render_template('tree_user.html', subhead='tree',tree=tree, user=str(thing))
        else:
            return render_template('404.html'),404
    else:
        return render_template('404.html'),404



@app.route('/about')
def about():
    return render_template('about.html',subhead='about')

@app.errorhandler(404)
def page404(e):
    return render_template('404.html'),404

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=False)
