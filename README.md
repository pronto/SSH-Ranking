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
