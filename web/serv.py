#!/usr/bin/env python2.6
from flask import Flask, render_template, send_from_directory, request
import MySQLdb,socket,os
from datetime import datetime
from ConfigParser import SafeConfigParser
par = SafeConfigParser()
#will be /etc/ssh-rank.ini or whereever you want it
par.read(os.getcwd()+"/config.ini")
import code
mysqluser=par.get("sshrank","mysqluser")
mysqlserv=par.get("sshrank","mysqlserv")
mysqlpass=par.get("sshrank","mysqlpass")
user_cnt=int(par.get("sshrank","user_cnt"))
total_ip=par.get("sshrank","total_ip")
stats_ip=par.get("sshrank","stats_ip")
con =MySQLdb.connect(mysqlserv,mysqluser,mysqlpass,"db_sshrank")
x=con.cursor()
socket.setdefaulttimeout(3)

from flask.ext.sqlalchemy import SQLAlchemy

app=Flask(__name__)

#dislineweird.jpg
app.debug=True


print mysqluser
@app.route('/')
def main():
    x.execute("""SELECT ip, count(*) AS cnt FROM ips_tbl GROUP BY ip ORDER BY cnt DESC LIMIT %s""" %total_ip)
    data=x.fetchall()
    return render_template('main.html',
                           data=data)
@app.route('/b')
def main2():
    x.execute("""SELECT ip, count(*) AS cnt FROM ips_tbl GROUP BY ip ORDER BY cnt DESC LIMIT %s""" %total_ip)
    data=x.fetchall()
    for a in data:
        x.execute("""SELECT user, count(*) as cnt FROM ips_tbl WHERE IP='%s' GROUP BY user ORDER BY cnt DESC LIMIT %s""" %(a[0], user_cnt))
        users=x.fetchall()
        x.execute("""SELECT ip,datetime from ips_tbl WHERE ip='%s' ORDER by datetime DESC LIMIT 1;""" % a[0])
        date=x.fetchall()
        date=datetime.strptime(str(date[0][1]),'%Y-%m-%d %H:%M:%S')
        date=date.strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template('main2.html',
                           data=data,
                           users=users,
                           date=date)


if __name__=='__main__':
    app.run(host='0.0.0.0')
