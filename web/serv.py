#!/usr/bin/evn python2.6
from flask import Flask, render_template, send_from_directory, request
import MySQLdb,socket,os
from ConfigParser import SafeConfigParser
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
socket.setdefaulttimeout(3)

#dislineweird.jpg
app=Flask(__name__)
app.debug=True

print mysqluser
@app.route('/')
def main():
    x.execute("""SELECT ip, count(*) AS cnt FROM ips_tbl GROUP BY ip ORDER BY cnt DESC LIMIT %s""" %total_ip)
    data=x.fetchall()
    return render_template('main.html',
                           data=data)

if __name__=='__main__':
    app.run(host='0.0.0.0')
