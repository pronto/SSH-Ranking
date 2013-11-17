SSH-Ranking
===========

SSH Ranking system! (re-write of ssh-fail-watcher)

Demo of the webUI (when working) at: http://vps3.pronto185.com

Project website: https://github.com/pronto/SSH-Ranking

This script will take your ssh connection logs and log them to MySQL, continuously watch authlog for new connection attempts, then rank them among previous authorization attempts.

status:
<pre>
Get info from auth.log.*           YES

Toss in MySQL                      YES (but still reworking how DB works)

Get RDNS and save RDNS history     Gets rdns, displays it. but not history

GeoIP                              NO

easy install method                kinda; read this..

watch for new things               YES

</pre>

# Installation Instructions
## Debian/Ubuntu
This was made on Linux debian 3.2.0-4-amd64 #1 SMP Debian 3.2.51-1 x86_64 GNU/Linux
should still work on other distros; you just won't be able to blindly follow this readme.
$ cat /etc/debian_version 
7.2
```
user@debian:~$ su
Password: 
root@debian:/home/user# apt-get install git python-pip mysql-server python-mysqldb 
>hit yes for install

>During this you will get asked for mysql-server root password; set that 

root@debian:/ # easy_install flask-sqlalchemy
>You might get a lot of warnings and such but if you see the below; you should be good

>Adding MarkupSafe 0.18 to easy-install.pth file

>Installed /usr/local/lib/python2.7/dist-packages/MarkupSafe-0.18-py2.7.egg
Finished processing dependencies for flask-sqlalchemy
root@debian:/ # 
```

## Red Hat/CentOS/Fedora
This was tested on CentOS 6.4 minimal but should work with all version 6 branches. Version 5.x may take some tweaking to make it work.

Install required packages
```
[root@centos ~]# yum install git mysql-server MySQL-python python-setuptools-devel -y
```
Now install required Python modules
```
[root@centos ~]# easy_install flask-sqlalchemy argparse
>You might get a lot of warnings and such but if you see the below; you should be good

>Adding MarkupSafe 0.18 to easy-install.pth file
>Installed /usr/lib/python2.6/site-packages/MarkupSafe-0.18-py2.6.egg
>Finished processing dependencies for flask-sqlalchemy
```
Now startup MySQL server. During this procedure you will be asked to set your mysql-server root password. Other than entering a root password, you can accept the defaults.
We also want to make sure mysqld starts next time the server starts.

```
[root@centos ~]# /etc/init.d/mysqld start
[root@centos ~]# mysql_secure_installation
[root@centos ~]# chkconfig mysqld on
 
```

## Configure MySQL 

```
root@debian:/# mysql -u root -p
>Enter password: 

mysql> CREATE USER 'sshrank'@'localhost' IDENTIFIED BY 'blargpass';
>Query OK, 0 rows affected (0.01 sec)

mysql> CREATE DATABASE db_sshrank;
>Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON db_sshrank.* TO sshrank@localhost;
>Query OK, 0 rows affected (0.00 sec)

mysql> exit
Bye

```

## SSH-Rank Configuration and Download
Clone SSH-Rank directly from github or download to your system via the project website

```
user@debian:~$ mkdir git
user@debian:~$ cd git
user@debian:~/git$ git clone https://github.com/pronto/SSH-Ranking && cd SSH-Ranking
Cloning into 'SSH-Ranking'...
remote: Counting objects: 453, done.
remote: Compressing objects: 100% (244/244), done.
remote: Total 453 (delta 233), reused 422 (delta 202)
Receiving objects: 100% (453/453), 158.32 KiB, done.
Resolving deltas: 100% (233/233), done.
user@debian:~/git/SSH-Ranking$ 

```

Now edit config.ini <br />
Change sqlclassPath variable to match where you downloaded SSH-Rank. Include the trailing /

```
sqlclassPath=/home/user/git/SSH-Ranking/
```

Modify the authlogpath and logname to point to the path and log name of the ssh log you want to watch. Include the trailing / <br />
For Debian-based systems you probably want auth.log. For Red Hat systems try secure

```
authlogpath=/var/log/
logname=auth.log
```

Change the following lines to match your SQL environment. Right now only MySQL is supported for sqlservertype.

```
sqlservertype=mysql
sqluser=sshrank
sqlsvr=localhost
sqlpass=blargpass

```
Now at the command line:

```
user@debian:~/git/SSH-Ranking$ python
Python 2.7.3 (default, Jan  2 2013, 13:56:14) 
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from sqlclass import *
>>> Base.metadata.create_all(eng)
>>> exit ()

```

### Verify the MySQL tables were created:

```
user@debian:~$ mysql -u sshrank -A db_sshrank -p
Enter password: 
mysql> show tables;
+----------------------+
| Tables_in_db_sshrank |
+----------------------+
| ips_alc2             |
| rdns_tbl             |
+----------------------+
2 rows in set (0.00 sec)

mysql> exit;

```

## Run SSH-Rank
For the moment you have to run sshrank.py under a utility like tmux or screen. 
Screen is probably in your package manager; simply run apt-get install screen if you're on a Debian-based distribution or yum install screen for Red Hat. 
You can download tmux from http://tmux.sourceforge.net/

```
root@debian:/home/user/git/SSH-Ranking# python ./sshrank.py -f on -w on
root
doing 1st run! yay!
Elapsed time was 5.91278e-05 seconds


==========Now Watching the logfile========
['::1', 'klfsjakl', '2013-11-13 12:59:01']
['::1', 'klfsjakl', '2013-11-13 12:59:05']
['192.168.1.50', 'kjskfjask', '2013-11-13 12:59:37']
['192.168.1.50', 'kjskfjask', '2013-11-13 12:59:41']

```
Those four entries are tests I did. As users try to connect with incorrect passwords, you'll see new entries show up. To test, attempt to ssh in to your server with an unknown user/pass and you should see it show up in this list.


## WebUI Setup
To run the web server portion, you can either run it on port 80 as root (not really recommended) or you can run it on an unprivileged port (default is port 5000). Change this in config.ini to suit your needs

```
webUI_port=5000

```
For persistence, the WebUI should also be run under a screen/tmux session

```
user@debian:~/git/SSH-Ranking$ python web/serv.py 
 * Running on http://0.0.0.0:5000/

```

Now you should be able to go to the IP:port and see the webUI.
 http://<ip_of_server>:<port>

eg: http://127.0.0.1:5000/

