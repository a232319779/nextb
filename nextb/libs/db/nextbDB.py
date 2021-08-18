# -*- coding: utf-8 -*-
# @Time    :   2021/08/18 19:02:13
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   nextbDB.py
# @Software:   Visual Studio Code
# @Desc    :   None


from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import INTEGER


Base = declarative_base()
metadata = Base.metadata

def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}
Base.to_dict = to_dict


class NextBTrades(Base):
    __tablename__ = 'nextb_trades'

    id = Column(INTEGER(), primary_key=True, unique=True, autoincrement=True)
    robto_name = Column(String(32))


class NextBDB(object):
    def __init__(self):
        pass
