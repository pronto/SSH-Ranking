SSH-Ranking
===========

SSH Ranking system! :D (re-write of ssh-fail-watcher)


web-ui (when working) at: http://vps3.pronto185.com:5000/

this script will take you auth logs and toss them in sql, then watch authlog for new things
then ranks them with other things

status:
<pre>
Get info from auth.log.*           YES

Toss in MySQL                      YES (but still reworking now DB works)

Get RDNS and save RDNS history     Gets rdns, displays it. but not history

GeoIP                              NO

easy install method                NO

watch for new things               NO

</pre>


to install set up mysql, create a user/pw for the project
add a database called "db_sshrank"
then run this mysql command to make the table 


<pre>
Create Table: CREATE TABLE `ips_alc2` (
  `ip` varchar(20) NOT NULL,
  `user` varchar(20) DEFAULT NULL,
  `datetime` datetime NOT NULL,
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`pk`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1
CREATE TABLE `rdns_tbl` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) NOT NULL,
  `rdns` text NOT NULL,
  `good` varchar(20) NOT NULL,
  `dtime` datetime NOT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1

</pre>
edit the config.ini for the script




python things you're gonna need(for now, more later):
sqlalchemy, argparse,ConfigParser

web ui needs: flask

screenshot: http://pronto185.com/screens/output.now.with.bold.png
atm run it as:
    ./sshrank.py -f on

then when that is done, you can do a ./outputdata.py

<pre>
116.124.x.x attempted 5153 times with users: 

        root:153,  test:108,  user:87,  minecraft:82,  nagios:81,  webadmin:81,  postgres:80,  tomcat:79,  testuser:79,  webmaster:79,   
        
153.x.x.81 attempted 3023 times with users: 

        root:1344,  test:19,  guest:18,  oracle:17,  ftp:16,  brian:14,  testing:14,  marty:14,  mailer:14,  webmaster:13,   

61.x.x.x attempted 2685 times with users: 

        ftptest:76,  userftp:76,  backup:76,  support:76,  redmine:76,  weblogic:76,  gateway:75,  testing:75,  apache:75,  zabbix:75,   

87.x.x.x attempted 823 times with users: 

        root:582,  bin:9,  haqr:9,  oracle:7,  postgres:5,  lswang:4,  nphone:4,  game1:3,  mysql:3,  ourpalm:3,   

        </pre>
