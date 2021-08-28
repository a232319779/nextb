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
from sqlalchemy.sql.sqltypes import INTEGER, FLOAT, BIGINT, Integer

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
    count = Column(Integer())

class NextBTrade(Base):
    __tablename__ = 'nextb_trade'

    id = Column(INTEGER(), primary_key=True, unique=True, autoincrement=True)
    recommond_id = Column(INTEGER())
    robot_name = Column(String(32))
    symbol = Column(String(1024))
    order_id = Column(BIGINT())
    buy_price = Column(FLOAT(32))
    buy_quantity = Column(FLOAT(32))
    buy_time = Column(DateTime())
    buy_quote = Column(FLOAT(32))
    sell_price = Column(FLOAT(32))
    sell_quantity = Column(FLOAT(32))
    sell_time = Column(DateTime())
    sell_quote = Column(FLOAT(32))
    profit = Column(FLOAT(32))
    profit_ratio = Column(FLOAT(32))
    status = Column(INTEGER())
    tickSize_index = Column(INTEGER())
    stepSize_index = Column(INTEGER())

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
        new_recommend.count = data.get('count', '')
        self.session_maker.add(new_recommend)
        self.session_maker.commit()

    def search_data(self, robot_name):
        datas = self.session_maker.query(NextBRecommend).filter(NextBRecommend.robot_name == robot_name).order_by(NextBRecommend.id.desc()).limit(1)
        if datas.count():
            return datas[0].to_dict()
        else:
            return []
    
    def search_datas(self, robot_name):
        datas = self.session_maker.query(NextBRecommend).filter(NextBRecommend.robot_name == robot_name).order_by(NextBRecommend.id.desc()).limit(28)
        if datas.count():
            return datas
        else:
            return []
    
    def add_trade(self, trade):
        new_trade = NextBTrade()
        recommond_id = trade.get('recommond_id', 0)
        new_trade.robot_name = trade.get('robot_name', '')
        new_trade.recommond_id = recommond_id
        new_trade.order_id = trade.get('order_id', 0)
        new_trade.buy_time = trade.get('buy_time', '')
        new_trade.sell_time = trade.get('sell_time', '')
        new_trade.buy_price = trade.get('buy_price', 0.0)
        new_trade.buy_quantity = trade.get('buy_quantity', 0.0)
        new_trade.buy_quote = trade.get('buy_quote', 0.0)
        new_trade.symbol = trade.get('symbol', '')
        new_trade.status = trade.get('status', 0)
        new_trade.symbol = trade.get('symbol', '')
        new_trade.status = trade.get('status', 0)
        new_trade.tickSize_index = trade.get('tickSize_index', 0)
        new_trade.stepSize_index = trade.get('stepSize_index', '')
        self.session_maker.add(new_trade)
        self.session_maker.commit()

    def update_trade(self, trade):
        recommond_id = trade.get('recommond_id', '')
        self.session_maker.query(NextBTrade).filter(NextBTrade.recommond_id == recommond_id).update(trade)
        self.session_maker.commit()
    
    def search_trade(self, robot_name):
        data = self.session_maker.query(NextBTrade).filter(NextBTrade.robot_name == robot_name).order_by(NextBTrade.id.desc()).limit(1)
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
    