from sqlalchemy import create_engine, Table, Column, BigInteger, String, MetaData, Date, DateTime, ForeignKey, func, \
    UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

ENGINE = create_engine('mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4', pool_recycle=3600)
print(ENGINE)

BASE = declarative_base()


class Item(BASE):
    __tablename__ = 'items'
    id = Column(BigInteger(), primary_key=True)
    title = Column(String(255), nullable=False, unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f' <Item({self.title})>'


ITEM = Item("Москва-Санкт-Петербург")
BASE.metadata.create_all(ENGINE)
SESSION = sessionmaker(bind=ENGINE)
SESS_OBJ = SESSION()
SESS_OBJ.add(ITEM)
SESS_OBJ.commit()

class Parameter(BASE):
    __tablename__ = 'parameters'
    item_id = Column(BigInteger(), ForeignKey('item_id'))
    created_on = Column(DateTime(), default=datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    date = Column(Date())
    quantity = Column(BigInteger())
    distance = Column(BigInteger())

    def __init__(self, created_at, date, quantity, distance):
        self.title = created_at
        self.title = date
        self.title = quantity
        self.title = distance

    def __repr__(self):
        return f' <Parameter({self.created_at}, {self.date}, {self.quantity}, {self.distance})>'


PARAMETER = Parameter("13.04.2022 17:30", "13.04.2022", "7", "712")
BASE.metadata.create_all(ENGINE)
SESSION = sessionmaker(bind=ENGINE)
SESS_OBJ = SESSION()


SESS_OBJ.add(PARAMETER)
SESS_OBJ.commit()
