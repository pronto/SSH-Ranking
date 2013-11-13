SSH-Ranking
===========

SSH Ranking system! :D (re-write of ssh-fail-watcher)


web-ui (when working) at: http://vps3.pronto185.com

this script will take you auth logs and toss them in sql, then watch authlog for new things
then ranks them with other things

status:
<pre>
Get info from auth.log.*           YES

Toss in MySQL                      YES (but still reworking now DB works)

Get RDNS and save RDNS history     Gets rdns, displays it. but not history

GeoIP                              NO

easy install method                kinda; read this..

watch for new things               YES

</pre>

# How To install:
### this was made on Linux debian 3.2.0-4-amd64 #1 SMP Debian 3.2.51-1 x86_64 GNU/Linux
should still work on other distros; you just wont be able to blindly follow this
$ cat /etc/debian_version 
7.2
```
user@debian:~$ su
Password: 
root@debian:/home/user# apt-get install git python-pip mysql-server python-mysqldb 
>|things, hit yes for install|

>durning this you will get asked for mysql-server root password; set that 

root@debain:/ # easy_install flask-sqlalchemy
>you might get a lot of warnings and such but if you see the below; you should be good

>Adding MarkupSafe 0.18 to easy-install.pth file

>Installed /usr/local/lib/python2.7/dist-packages/MarkupSafe-0.18-py2.7.egg
Finished processing dependencies for flask-sqlalchemy
root@debain:/ # 
```


###set up mysql part

```
root@debian:/# mysql -p
>Enter password: 

mysql&#62; CREATE USER 'sshrank'@'localhost' IDENTIFIED BY 'blargpass';
>Query OK, 0 rows affected (0.01 sec)

mysql&#62; CREATE DATABASE db_sshrank;
>Query OK, 1 row affected (0.00 sec)

mysql&#62; GRANT ALL PRIVILEGES ON db_sshrank.* TO sshrank@localhost;
>Query OK, 0 rows affected (0.00 sec)

mysql> exit
Bye
```

### now for git/pythong/andmoresql

```
user@debian:~$ cd
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


Now edit the sqlclass.py
looking for line:
```python
eng = sqlalchemy.create_engine('mysql://sshrank:blargpass@localhost')
```
change it so its ('enginetype://username:password@sqlloc')  for more info look up SQL-Alchemy

now do:
```
user@debian:~/git/SSH-Ranking$ python
Python 2.7.3 (default, Jan  2 2013, 13:56:14) 
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from sqlclass import *
>>> exit
```


### check the mysql tables:
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
```


## Now you should be able to start watching!
for now you have to run sshrank.py under tmux/screen
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
those four entries are just test ones i did



## now for the webUI
the very last line on  web/serv.py you might need to edit if you dont want to run the web script as root
```python
    app.run(host='0.0.0.0',debug=False, port=80)
```


    just get rid of the ', port=80' part


    this should also be run under screen/tmux
```
user@debian:~/git/SSH-Ranking$ cp sqlclass.py web
user@debian:~/git/SSH-Ranking$ python web/serv.py 
 * Running on http://0.0.0.0:5000/
```

    now if you get all this you sould be able to go to http://<ip of serve>:<port>
    eg http://127.0.0.1:5000/

    and you should see the webui! :D 
