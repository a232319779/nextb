# -*- coding: utf-8 -*-
# @Time    :   2021/08/18 17:33:15
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   nextbbinance.py
# @Software:   Visual Studio Code
# @Desc    :   None

import pickle
import datetime
from binance.client import Client

global_proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

__doc__ = """
从币安交易平台获取数据
"""

class NextBBiance(object):
    def __init__(self, api_key, api_secret, proxies=global_proxies, increasing=True):
        self.client = Client(api_key, api_secret, {'proxies': proxies})
        if increasing:
                self.load_datas()
                self.symbols = [symbol for symbol in self.datas.get('data', [])]
        else:
            self.datas = dict()
            exchange_info = self.client.get_exchange_info()
            self.symbols = exchange_info.get('symbols', [])

    def load_datas(self):
        file_name = ''
        with open(file_name, 'rb') as f:
            self.datas = pickle.load(f)

    def dump_datas(self):
        file_name = ''
        update_time = self.datas['update_time']
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:00:00')
        if update_time[:13] != now_time[:13]:
            self.datas['update_time'] = now_time
            with open(file_name, "wb") as f:
                pickle.dump(self.datas, f, 2)

    def get_symbol(self, index):
        """
        从本地缓存币种列表，返回指定索引对应的币种名称
        """
        return self.symbols[index]

    def get_symbol_local(self, symbol_name):
        """
        从本地缓存币种列表，返回指定索引对应的币种名称
        """
        for sn in self.symbols:
            if symbol_name in sn.get('symbol', ''):
                return sn

    def get_symbol_info(self, symbol):
        """
        从币安API接口，返回指定币种信息
        """
        data = self.client.get_symbol_info(symbol=symbol)
        return data

    def get_symbols(self):
        """
        从本地缓存返回币种列表
        """
        return self.symbols

    def get_klines(self, symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=500):
        """
        从币安API接口，返回指定币种的K线图
        """
        data = None
        if symbol.get('status', '') == 'TRADING' and 'SPOT' in symbol.get('permissions', []):
            if symbol.get('quoteAsset', '') == 'USDT':
                symbol_name = symbol.get('symbol', '')
                if not symbol_name.endswith('DOWNUSDT') and \
                    not symbol_name.endswith('UPUSDT') and \
                        symbol_name not in ('USDCUSDT', 'BUSDUSDT', 'PAXUSDT', 'TUSDUSDT', 'USDSBUSDT', 'SUSDUSDT'):
                    data = self.client.get_klines(symbol=symbol_name, interval=interval, limit=limit)

        return data

    def get_klines_inc(self, symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=500):
        """
        从币安API接口，返回指定币种的K线图
        """
    
        data = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)

        return data[0]

    def get_binance_klines_datas(self, interval=Client.KLINE_INTERVAL_1HOUR, limit=500):
        """
        获取所有币种的K线图数据
        """
        datas = list()
        i = 0
        for sn in self.symbols:
            symbol = sn.get('symbol')
            data = self.get_klines(symbol, interval=interval, limit=limit)
            if data:
                tmp = {
                    "symbol": symbol,
                    "symbol_index": i,
                    "data": data
                }
                datas.append(tmp)
            i += 1

        self.datas['data'] = datas
        self.dump_datas()
        return datas

    def get_binance_klines_datas_inc(self, interval=Client.KLINE_INTERVAL_1HOUR, limit=500):
        """
        获取所有币种的K线图数据
        """
        datas = self.datas.get('data')
        i = 0
        for sn in self.symbols:
            symbol = sn.get('symbol')
            data = self.get_klines_inc(symbol, interval=interval, limit=limit)
            if data:
                datas[i]['data'].append(data)
            i += 1

        self.datas['data'] = datas
        self.dump_datas()
        return datas

    def get_asset_balance(self, symbol='USDT'):
        """
        从币安API接口，返回指定账户的余额
        """
        account = self.client.get_asset_balance(symbol)
        return account

    def get_symbol_ticker(self, symbol):
        """
        从币安API接口，返回指定币种的当前价格
        """
        price_data = self.client.get_symbol_ticker(symbol=symbol)

        return price_data

    def order_limit_buy(self, symbol, price, quantity):
        """
        限价买入单
        """
        result = self.client.order_limit_buy(symbol=symbol, price=price, quantity=quantity)

        return result
    
    def order_limit_sell(self, symbol, price, quantity):
        """
        限价卖出单
        """
        result = self.client.order_limit_sell(symbol=symbol, price=price, quantity=quantity)
        return result

    def order_market_buy(self, symbol, quantity):
        """
        市价买入单: taker
        """
        result = self.client.order_market_buy(symbol=symbol, quantity=quantity)

        return result

    def order_market_sell(self, symbol, quantity):
        """
        市价卖出单: maker
        """
        result = self.client.order_market_sell(symbol=symbol, quantity=quantity)

        return result

    def get_order(self, symbol, orderId):
        """
        获取订单状态
        """
        order_status = self.client.get_order(symbol=symbol, orderId=orderId)

        return order_status

    def cancel_order(self, symbol, orderId):
        """
        取消订单
        """
        order_status = self.client.cancel_order(symbol=symbol, orderId=orderId)

        return order_status

    def get_my_trades(self, symbol, limit=5):
        """
        获取订单状态
        """
        order_status = self.client.get_my_trades(symbol=symbol, limit=limit)

        return order_status
