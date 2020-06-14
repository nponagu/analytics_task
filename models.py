import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine, \
    UniqueConstraint, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
import pandas as pd


engine = create_engine("sqlite:///mybase.db")
Base = declarative_base()


class SHERULER(Base):
    __tablename__ = 'T_CONTRACTOR_SHERULER'
    ID = Column(Integer, primary_key=True)
    ID_NAME = Column(Integer, ForeignKey('fio.ID'))
    SCHEDULE = Column(String(10), nullable=False)
    DATE_BEGIN = Column(DateTime, nullable=False)
    DATE_END = Column(DateTime, nullable=False)
    UniqueConstraint('ID_NAME', 'DATE_BEGIN')
    CheckConstraint('DATE_BEGIN <= DATE_END')


class FIO(Base):
    __tablename__ = 'fio'
    ID = Column(Integer, primary_key=True)
    NAME = Column(String(13))
    SHERULERS = relationship("SHERULER", backref="T_CONTRACTOR_SHERULER.ID")


Base.metadata.create_all(engine)
session = Session(bind=engine)
df = pd.read_csv("shedulers.csv", engine='python', sep=";")


for index, row in df.iterrows():

    name = row["ФИО"]
    human = FIO(NAME=name)
    if not session.query(FIO).filter(FIO.NAME == name).all():
        session.add(human)
        session.commit()

    ID_NAME = session.query(FIO.ID).filter(FIO.NAME == name).first()[0]
    SCHEDULE = row["Расписание"]
    DATE_BEGIN = datetime.datetime.strptime(row["Дата начала расписания"], '%d.%m.%Y %H:%M')
    DATE_END = datetime.datetime.strptime(row["Дата окончания расписания"], '%d.%m.%Y %H:%M')
    work = SHERULER(ID_NAME=ID_NAME,
                    SCHEDULE=SCHEDULE,
                    DATE_BEGIN=DATE_BEGIN,
                    DATE_END=DATE_END)


    session.add(work)
    session.commit()


session.close()