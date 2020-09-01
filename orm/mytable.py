from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,DateTime

Base = declarative_base()

class mytable(Base):
    #表名
    __tablename__ = "my_table"
    #欄位，屬性
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    age = Column(Integer)
    birth = Column(DateTime)
    clss_name = Column(String(255))

