# -*- coding: utf-8 -*-
# @Time    :   2021/08/18 19:02:13
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   nextbDB.py
# @Software:   Visual Studio Code
# @Desc    :   None


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import INTEGER

from nextb.configs.db_config import db_config


Base = declarative_base()
metadata = Base.metadata

def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}
Base.to_dict = to_dict

class NextBRecommend(Base):
    __tablename__ = 'nextb_recommond'

    id = Column(INTEGER(), primary_key=True, unique=True, autoincrement=True)
    robot_name = Column(String(32))
    time = Column(DateTime())
    symbols = Column(String(1024))

class NextBDB:
    def __init__(self):
        self.engine = self.init_db_connection(**db_config)
        self.session_maker = None
        self.create_session()

    @staticmethod
    def init_db_connection(address, port, username, password, db_name):
        values = {
            'address': address,
            'port': port,
            'username': username,
            'password': password,
            'db_name': db_name
        }
        template_conn_str = "postgresql+psycopg2://{username}:{password}@{address}:{port}/{db_name}"
        conn_str = template_conn_str.format(**values)
        engine = create_engine(conn_str)
        return engine

    # DRbmfj86yJ3sqv21X5fo9A
    def create_session(self):
        if self.session_maker is None:
            self.session_maker = scoped_session(sessionmaker(autoflush=True, autocommit=False,
                                                             bind=self.engine))
    
    def add_data(self, data):
        new_recommend = NextBRecommend()
        new_recommend.robot_name = data.get('robot_name', '')
        new_recommend.time = data.get('time', '')
        new_recommend.symbols = data.get('symbols', '')
        self.session_maker.add(new_recommend)
        self.session_maker.commit()
    
    def search_data(self, robot_name):
        data = self.session_maker.query(NextBRecommend).filter(NextBRecommend.robot_name == robot_name).order_by(NextBRecommend.id.desc()).limit(1)
        if data.count():
            return data[0].to_dict()
        else:
            return {}

def main():
    # 建表
    cmd = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
        db_config.get('username'),
        db_config.get('password'),
        db_config.get('address'),
        db_config.get('port'),
        db_config.get('db_name'),
    )
    engine = create_engine(cmd,
                           client_encoding='utf-8',
                           echo=True)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()
    