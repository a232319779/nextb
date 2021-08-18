# -*- coding: utf-8 -*-
# @Time    :   2021/08/18 17:33:15
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   nextbbinance.py
# @Software:   Visual Studio Code
# @Desc    :   None


from binance.client import Client

global_proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

__doc__ = """
从币安交易平台获取数据
"""

class NextBBiance(object):
    def __init__(self, api_key, api_secret, proxies=global_proxies):
        self.client = Client(api_key, api_secret, {'proxies': proxies})
        exchange_info = self.client.get_exchange_info()
        self.symbols = exchange_info.get('symbols', [])

    def get_symbol(self, index):
        """
        从本地缓存币种列表，返回指定索引对应的币种名称
        """
        return self.symbols[index]

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

    def get_klines(self, symbol, interval=Client.KLINE_INTERVAL_1HOUR):
        """
        从币安API接口，返回指定币种的K线图
        """
        data = None
        if symbol.get('status', '') == 'TRADING' and 'SPOT' in symbol.get('permissions', []):
            if symbol.get('quoteAsset', '') == 'USDT':
                symbol_name = symbol.get('symbol', '')
                if not symbol_name.endswith('DOWNUSDT') and \
                    not symbol_name.endswith('UPUSDT') and \
                        symbol_name not in ('USDCUSDT', 'BUSDUSDT', 'PAXUSDT', 'TUSDUSDT', 'USDSBUSDT'):
                    data = self.client.get_klines(symbol=symbol_name, interval=interval)

        return data

    def get_binance_klines_datas(self, interval=Client.KLINE_INTERVAL_1HOUR):
        """
        获取所有币种的K线图数据
        """
        datas = list()
        i = 0
        for symbol in self.symbols:
            data = self.get_klines(symbol, interval=interval)
            if data:
                tmp = {
                    "symbol": symbol.get('symbol'),
                    "symbol_index": i,
                    "data": data
                }
                datas.append(tmp)
            i += 1

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
        现价买入单: taker
        """
        result = self.client.order_market_buy(symbol=symbol, quantity=quantity)

        return result

    def order_market_sell(self, symbol, quantity):
        """
        现价卖出单: maker
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
