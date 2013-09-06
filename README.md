SSH-Ranking
===========

SSH Ranking system! :D (re-write of ssh-fail-watcher)


this script will take you auth logs and toss them in sql, then watch authlog for new things
then ranks them with other things

status:
Get info from auth.log.*           YES
Toss in MySQL                      YES (but still reworking now DB works)
Get RDNS and save RDNS history     NO
GeoIP                              NO
easy install method                NO
watch for new things               NO

to install set up mysql, create a user/pw for the project
add a database called "db_sshrank"
then run this mysql command to make the table 

CREATE TABLE ips_tbl( ip VARCHAR(20) NOT NULL, RDNS TEXT NOT NULL, USER TEXT NOT NULL, datetime DATETIME NOT NULL);


edit the config.ini for the script




python things you're gonna need(for now, more later):
    MySQLdb gzip, argparse, ConfigParser



atm run it as:
    ./sshrank.py -f on

then when that is done, you can do a ./outputdata.py


116.124.x.x attempted 5153 times with users: 
        root:153,  test:108,  user:87,  minecraft:82,  nagios:81,  webadmin:81,  postgres:80,  tomcat:79,  testuser:79,  webmaster:79,   
153.x.x.81 attempted 3023 times with users: 
        root:1344,  test:19,  guest:18,  oracle:17,  ftp:16,  brian:14,  testing:14,  marty:14,  mailer:14,  webmaster:13,   
61.x.x.x attempted 2685 times with users: 
        ftptest:76,  userftp:76,  backup:76,  support:76,  redmine:76,  weblogic:76,  gateway:75,  testing:75,  apache:75,  zabbix:75,   
218.x.x.x attempted 2626 times with users: 
        root:462,  test:86,  nagios:73,  mysql:68,  oracle:64,  postgres:62,  webadmin:61,  apache:61,  developer:60,  ftptest:59,   
109.x.5.x attempted 1891 times with users: 
        root:1699,  bin:16,  test:6,  oracle:6,  webmaster:5,  i-heart:4,  tomcat:3,  user0:3,  www:3,  diskbook:3,   
65.x.x.x attempted 1188 times with users: 
        root:1158,  bin:16,  oracle:2,  test:1,  be:1,  dinamo:1,  djmaxx:1,  karla:1,  kylix:1,  mov:1,   
124.x.3.x attempted 1087 times with users: 
        root:903,  bin:12,  oracle:7,  mp3:5,  news:5,  ftpuser:4,  bash:3,  brianmac:3,  cgi:3,  git:3,   
201.x.x.x attempted 1009 times with users: 
        root:13,  test:4,  postgres:3,  eggdrop:3,  luciana:3,  install:3,  paul:3,  com:3,  webadmin:3,  dan:3,   
12.9.x.x attempted 920 times with users: 
        root:911,  rekinu:2,  boot:1,  xxxxx:1,  celso:1,  ryback:1,  bin:1,  baietas:1,  r00t:1,   
87.x.x.x attempted 823 times with users: 
        root:582,  bin:9,  haqr:9,  oracle:7,  postgres:5,  lswang:4,  nphone:4,  game1:3,  mysql:3,  ourpalm:3,   
