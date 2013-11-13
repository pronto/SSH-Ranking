#classes

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,VARCHAR,TEXT,DATETIME, Sequence,func
Base = declarative_base()
eng = sqlalchemy.create_engine('mysql://sshrank:blargpass@localhost')
eng.execute("USE db_sshrank")
eng.execute("select 1").scalar()
Session =sqlalchemy.orm.sessionmaker(bind=eng)
Session = Session()


class ips(Base):
    __tablename__ = 'ips_alc2'
    ip = Column(VARCHAR(20))
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
    ip = Column(VARCHAR(20)
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



#from sqlclass import *
#a=ips('127.0.0.1', 'jkldj', '2013-10-28 15:10:51')
#Session.add(a)
#Session.commit()
