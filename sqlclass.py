#classes

import sqlalchemy
from ConfigParser import SafeConfigParser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,VARCHAR,TEXT,DATETIME, Sequence,func,Boolean, ForeignKey
from sqlalchemy.orm import relationship

# Config files! Yay!
config = SafeConfigParser()
config.read('config.ini')

sqlserver = config.get('sql', 'sqlserv')
sqlservertype = config.get('sql', 'sqlservertype')
sqluser = config.get('sql', 'sqluser')
sqlpass = config.get('sql', 'sqlpass')

Base = declarative_base()
query_string = sqlservertype + '://' + sqluser + ':' + sqlpass + '@' + sqlserver
eng = sqlalchemy.create_engine(query_string,  pool_recycle=36)
eng.execute("USE db_sshrank")
eng.execute("select 1").scalar()

Session =sqlalchemy.orm.sessionmaker(bind=eng)
sqlsess = Session()

def resession():
    sqlsess.close()
    del(sqlsess)
    Session = sqlalchemy.orm.sessionmaker(bind=eng)
    sqlsess=Session()
    return sqlsess

class ips(Base):
    __tablename__ = 'ips_alc2'
    ip = Column(VARCHAR(39))
    user = Column(TEXT)
    dtime = Column(DATETIME)
    pk = Column(Integer,Sequence('pk'), primary_key=True)

    def __init__(self,ip,user,dtime):
        self.ip = ip
        self.user = user
        self.dtime = dtime

    def __repr__(self):
        return "<ip('%s','%s', '%s')>" % (self.ip, self.user, self.dtime)

class rdns(Base):
    __tablename__= 'rdns_tbl'
    pk = Column(Integer,Sequence('pk'), primary_key=True)
    ip = Column(VARCHAR(39))
    rdns = Column(TEXT)
    good = Column(VARCHAR(20))
    dtime = Column(DATETIME)

    def __init__(self,ip,rdns,good,dtime):
        self.ip = ip
        self.rdns = rdns
        self.good = good
        self.dtime = dtime

    def __repr__(self):
        return "<rdns('%s','%s','%s','%s')>" % (self.ip, self.rdns, self.good, self.dtime)

class nmapSQL(Base):
    __tablename__='nmapmysql'
    #                                       |ignored|         
    #ip, dtime, port number, State, Protocol, Owner, Service, SunRPC info, Version info
    pk = Column(Integer,Sequence('pk'), primary_key=True)
    ip = Column(VARCHAR(39))
    dtime = Column(DATETIME)
    portnum = Column(VARCHAR(5))
    state = Column(VARCHAR(10))
    proto = Column(VARCHAR(5))
    service = Column(VARCHAR(39)) 
    verinfo = Column(TEXT)
    #                   1   2      3        4       5     6         7
    def __init__(self, ip, dtime, portnum, state, proto, service, verinfo):
        self.ip = ip
        self.dtime = dtime
        self.portnum = portnum
        self.state = state
        self.proto = proto
        self.service = service
        self.verinfo = verinfo


    def __repr__(self):
        return "<nmapSQL>('%s','%s','%s','%s','%s','%s','%s')>" % ( self.ip, self.dtime, self.portnum, self.state, self.proto, self.service, self.verinfo)
        #                  1     2   3    4    5    6    7              1      2              3             4         5            6           7 


#http://stackoverflow.com/questions/8839211/sqlalchemy-add-child-in-one-to-many-relationship
#from sqlclass import *
#a=ips('127.0.0.1', 'jkldj', '2013-10-28 15:10:51')
#Session.add(a)
#Session.commit()
