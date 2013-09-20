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


app=Flask(__name__)
#app.debug=True

@app.route('/')
def main():
    con =MySQLdb.connect(mysqlserv,mysqluser,mysqlpass,"db_sshrank")
    x=con.cursor()
    #get the IPs
    x.execute("""SELECT ip, count(*) AS cnt FROM ips_tbl GROUP BY ip ORDER BY cnt DESC LIMIT %s""" %total_ip)
    data=x.fetchall()
    craylist=[]
    for a in data:
        #get the users
        x.execute("""SELECT user, count(*) as cnt FROM ips_tbl WHERE IP='%s' GROUP BY user ORDER BY cnt DESC LIMIT %s""" %(a[0], user_cnt))
        users=x.fetchall()
        x.execute("""SELECT ip,datetime from ips_tbl WHERE ip='%s' ORDER by datetime DESC LIMIT 1;""" % a[0])
        date=x.fetchall()
        date=datetime.strptime(str(date[0][1]),'%Y-%m-%d %H:%M:%S')
        date=date.strftime('%Y-%m-%d %H:%M:%S')
        craystr=""
        craystr= "<b>"+str(a[0]) + "</b> attempted <b>" + str(a[1]) + "</b> Last Attempt: <b>"+ date+" </b>times with users: <br>"
        craystr=craystr+ "&nbsp;&nbsp;&nbsp;&nbsp;",
        craystr=str(craystr[0])
        # code.interact(local=locals())
        for b in users:
            craystr=craystr+ "<b>"+str(b[0]) + "</b>:" + str(b[1]) + ", "
        print ""
        #check for rdns:
        x.execute("""SELECT * FROM rdns_tbl WHERE ip='%s'""" % a[0])
        rdnsthings=x.fetchall()
        if rdnsthings:
            for rd in rdnsthings:
                if rd[1] != 'NO DNS HERE':
                    craystr=craystr+ "<br>&nbsp;&nbsp;&nbsp;&nbsp;rDNS: <b>" + str(rd[1]) +"</b>",
                    craystr=str(craystr[0])+  "and the dns is: <b>" + str(rd[2]) + "</b>"
                    craystr=craystr+  str("  last updated on <b>"+  str(rd[3]) + "</b>")
                    #if a[0] == '203.69.37.205':
                    #   code.interact(local=locals())
        craystr=craystr+  "<br>"
            #print craystr
        craylist.append(craystr)
    return render_template('main.html', craylist=craylist)

if __name__=='__main__':
    app.run(host='0.0.0.0')
