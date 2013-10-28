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
    __tablename__ = 'ips_alc'
    ip = Column(VARCHAR)
    USER = Column(TEXT)
    datetime = Column(DATETIME)
    pk = Column(Integer,Sequence('pk'), primary_key=True)

    def __init__(self,ip,USER,datetime):
        self.ip = ip
        self.user = USER
        self.date = datetime

    def __repr__(self):
        return "<ip('%s','%s', '%s')>" % (self.ip, self.user, self.date)


