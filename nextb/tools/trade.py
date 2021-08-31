# -*- coding: utf-8 -*-
# @Time    :   2021/08/24 19:20:12
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   trade.py
# @Software:   Visual Studio Code
# @Desc    :   None

import json
from time import sleep
from collections import Counter

from datetime import datetime
from nextb.libs.utils.parsecmd import nextb_cmd_parse
from nextb.libs.utils.parseini import NextBParseINI
from nextb.libs.utils.basedata import BaseData
from nextb.libs.platform.nextbbinance import NextBBiance
from nextb.libs.db.nextbDB import NextBDB

def calc(account, coin_info, price, ratio=0.11):
    """
        根据当前价格和剩余资金，计算买入数量
    """
    calc_result = None
    usdt_free = float(account['free'])
    # usdt_free = 100.0
    filters = coin_info.get('filters', [])
    # 最小价格精度
    tickSize = '0.001'
    # 最小买入买入精度
    stepSize = '0.001'
    for filter in filters:
        if 'PRICE_FILTER' == filter.get('filterType', ''):
            tickSize = filter.get('tickSize', '0.001')
        elif 'LOT_SIZE' == filter.get('filterType', ''):
            stepSize = filter.get('stepSize', '0.001')
    tickSize_index = tickSize.find('1')
    tickSize_index = 0 if tickSize_index == 0 else tickSize_index - 1
    tickSize_index = tickSize_index if tickSize_index < 5 else 4
    stepSize_index = stepSize.find('1')
    stepSize_index = 0 if stepSize_index == 0 else stepSize_index - 1
    choose_symbol = coin_info.get('symbol')
    if price:
        choose_buy_price = round(price, tickSize_index)
        choose_buy_quantity = round(((usdt_free - 0.5*float(stepSize)) / choose_buy_price - 0.5*float(stepSize)) * 0.98, stepSize_index)
        calc_result = {
            "sybmol_name": choose_symbol,
            "buy_price": choose_buy_price,
            "buy_quantity": choose_buy_quantity,
            "tickSize_index": tickSize_index,
            "stepSize_index": stepSize_index
        }
    return calc_result

def get_trade(symbol, nbb, isBuyer=True):
    trades = nbb.get_my_trades(symbol,5)
    price_list = list()
    qty = 0.0
    quoteQty = 0.0
    for trade in trades:
        if isBuyer == trade.get('isBuyer'):
            quoteQty += float(trade.get('quoteQty', '0.0'))
            qty += float(trade.get('qty', '0.0'))
            price_list.append(float(trade.get('price', '0.0')))
    result = {'quoteQty': quoteQty, 'price': sum(price_list)/len(price_list), 'qty': qty, 'time': datetime.fromtimestamp(trades[0].get('time')/1000)}
    return result

def count_symbol(new_datas):
    symbols = list()
    for nd in new_datas:
        if nd.symbols:
            symbols.extend(nd.symbols.split(','))
    return len(list(set(symbols)))

def choose_symbol_func(new_datas):
    bd = BaseData()
    symbols = list()
    for nd in new_datas:
        if nd.symbols:
            symbols.extend(nd.symbols.split(','))
    if symbols:
        symbols_counter = dict(Counter(symbols))
        symbols_counter = sorted(symbols_counter.items(), key=lambda item: item[1], reverse=True)
        max_counter = max([a[1] for a in symbols_counter])
        max_counter = max([max_counter, 3])
        symbols = [a[0] for a in symbols_counter if a[1] >= max_counter]
        choose_symbols = dict()
        for symbol in symbols:
            choose_symbols[symbol] = bd.get_symbol_qty(symbol, 5)
        choose_symbols = sorted(choose_symbols.items(), key=lambda item: item[1], reverse=True)
        symbols = [a[0] for a in choose_symbols]
        # 排除BTC和ETH，太贵，买不起
        for s in symbols:
            symbol = s+"USDT"
            if symbol in ['BTCUSDT', "ETHUSDT"]:
                continue
            return symbol

    return ''
        

def nextb_buy(robot_name, now_recommond_id, ratio, db, nbb):
    current_recommond = db.search_data(robot_name)
    recommond_id = current_recommond.get('id', 0)
    # 判断交易情况
    if now_recommond_id == recommond_id:
        # 交易完成
        print("交易已经完成，退出")
    else:
        # 等待交易，市价买入
        datas = db.search_datas(robot_name,limit=5)
        count = count_symbol(datas)
        if count > 60:
            symbol = choose_symbol_func(datas)
            if symbol:
                account = nbb.get_asset_balance('USDT')
                price_data = nbb.get_symbol_ticker(symbol)
                price = float(price_data.get('price', 0.0))
                symbol_info = nbb.get_symbol_info(symbol)
                calc_result = calc(account,symbol_info, price, ratio)
                buy_quantity = calc_result.get('buy_quantity', 0)
                buy_result = nbb.order_market_buy(symbol, buy_quantity)
                buy_status = buy_result.get('status', '')
                buy_order_id = buy_result.get('orderId', 0)
                i = 1
                while i:
                    if i > 10:
                        print('执行市价买入出错，订单信息：{0}'.format(json.dumps(buy_result, default=str)))
                        exit(0)
                    if buy_status == 'FILLED':
                        break
                    sleep(1)
                    buy_result = nbb.get_order(symbol, buy_order_id)
                    buy_status = buy_status = buy_result.get('status', '')
                    i += 1
                if buy_result.get('orderId', 0):
                    # 买单3秒以后，挂单卖出
                    sleep(3)
                    result = get_trade(symbol, nbb, isBuyer=True)
                    buy_price = result.get('price', 0)
                    sell_price = round(buy_price * ratio, calc_result.get('tickSize_index'))
                    qty = round(result.get('qty', 0.0) * 0.999 - 0.5 * pow(0.1, calc_result.get('stepSize_index')), calc_result.get('stepSize_index'))
                    sell_result = nbb.order_limit_sell(symbol, sell_price, qty)
                    orderId = sell_result.get('orderId', 0)
                    tickSize_index = calc_result.get('tickSize_index', 2)
                    stepSize_index = calc_result.get('stepSize_index', 2)
                    trade = {'robot_name': robot_name, 'recommond_id': recommond_id, 'order_id': orderId,
                    'buy_time': datetime.now(),'sell_time': datetime.now(), 'buy_price': buy_price, 'buy_quantity': result.get('qty', 0.0),
                    'buy_quote':result.get('quoteQty', 0.0), 'symbol': symbol, 'status': 0,
                    'tickSize_index': tickSize_index, 'stepSize_index': stepSize_index}
                    db.add_trade(trade)
                    print('交易成功: {0}'.format(json.dumps(trade, default=str)))
            else:
                print('没有合适的币种买入，退出')
        else:
            print('卖方市场，暂时不买入')

def main():
    cmd_args = nextb_cmd_parse()
    robot_name = cmd_args.name
    config_path = cmd_args.config
    nbpi = NextBParseINI(config_path)
    robot_config = nbpi.get_robot_config(robot_name)
    proxies = {
        "http": robot_config.get("http_proxy", ''),
        "https": robot_config.get("https_proxy", '')
    }
    api_key = robot_config.get("api_key")
    api_secret = robot_config.get("api_secret")
    ratio = float(robot_config.get("ratio"))
    sell_ratio = float(robot_config.get("sell_ratio"))
    maker_ratio = float(robot_config.get("maker_ratio"))
    hour = float(robot_config.get("hour"))
    nbb = NextBBiance(
        api_key=api_key, api_secret=api_secret, proxies=proxies, increasing=True
    )
    db = NextBDB()
    current_trade = db.search_trade(robot_name)
    status = current_trade.get('status', -1)
    recommond_id = current_trade.get('recommond_id', -1)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(20*'-' + now + 20*'-')
    if status == 0:
        cur_trade = db.search_trade(robot_name)
        symbol = cur_trade.get('symbol', '')
        # 判断当前订单交易状态
        order_id = cur_trade.get('order_id', 0)
        order_status = nbb.get_order(symbol=symbol, orderId=order_id)
        if order_status.get('status', '') == 'FILLED':
            # 交易完成
            result = get_trade(symbol, nbb, isBuyer=False)
            buy_quote = cur_trade.get('buy_quote', 0)
            sell_quote = result.get('quoteQty', 0.0)
            sell_price = result.get('price', 0.0)
            sell_qty = result.get('qty', 0.0)
            sell_time = result.get('time', datetime.now())
            profit = sell_quote - buy_quote
            profit_ratio = profit / buy_quote * 100
            trade = {'recommond_id': recommond_id, 'status': 1, 
            'sell_time': sell_time.strftime('%Y-%m-%d %H:%M:%S'), 'sell_price': sell_price, 'sell_quantity': sell_qty, 
            'sell_quote': sell_quote, 'profit': profit, 'profit_ratio': profit_ratio}
            print('当前币种: %s, 交易状态: 已卖出, 卖出价格: %.2f, 收益: %.2f, 信息: %s' % (symbol, sell_quote, profit, json.dumps(trade)))
            db.update_trade(trade)
            nextb_buy(robot_name, recommond_id, ratio, db, nbb)
        else:
            # 判断行情和持有时间
            buy_price = cur_trade.get('buy_price', '')
            buy_time = cur_trade.get('buy_time', '')
            now_time = datetime.now()
            hold_hours = (now_time - buy_time).seconds / 3600
            price_data = nbb.get_symbol_ticker(symbol)
            price = float(price_data.get('price', 0.0))
            now_ratio = (price - buy_price) / buy_price
            datas = db.search_datas(robot_name,limit=5)
            count = count_symbol(datas)
            print('当前行情: %d, 当前币种: %s, 当前涨跌幅: %.2f%%, 持有时间: %.2f小时' % (count, symbol, now_ratio * 100, hold_hours))
            if (now_ratio < sell_ratio and hold_hours > 4.0) or hold_hours > hour or count < 3 or now_ratio > maker_ratio:
                if count < 5:
                    print('买方市场，考虑卖出')
                # 取消订单
                cancel_order = nbb.cancel_order(symbol, order_id)
                if cancel_order.get('orderId', 0):
                    sleep(3)
                    # 市价卖出
                    stepSize_index = cur_trade.get('stepSize_index', 2)
                    sell_quantity = round(cur_trade.get('buy_quantity', 0) * 0.999 - 0.5 * pow(0.1, stepSize_index), stepSize_index)
                    sell_status = nbb.order_market_sell(symbol, sell_quantity)
                    if sell_status.get('status', 0):
                        result = get_trade(symbol, nbb, isBuyer=False)
                        buy_quote = cur_trade.get('buy_quote', 0)
                        sell_quote = result.get('quoteQty', 0.0)
                        sell_price = result.get('price', 0.0)
                        sell_qty = result.get('qty', 0.0)
                        sell_time = result.get('time', datetime.now())
                        profit = sell_quote - buy_quote
                        profit_ratio = profit / buy_quote * 100
                        trade = {'recommond_id': recommond_id, 'status': 1, 
                        'sell_time': sell_time.strftime('%Y-%m-%d %H:%M:%S'), 'sell_price': sell_price, 'sell_quantity': sell_qty, 
                        'sell_quote': sell_quote, 'profit': profit, 'profit_ratio': profit_ratio}
                        print('当前币种: %s, 交易状态: 已卖出, 卖出价格: %.2f, 收益: %.2f, 信息: %s' % (symbol, sell_quote, profit, json.dumps(trade)))
                        db.update_trade(trade)
                        # 进行下一次买卖
                        nextb_buy(robot_name, recommond_id, ratio, db, nbb)
    elif status in [-1, 1]:
        nextb_buy(robot_name, recommond_id, ratio, db, nbb)
    else:
        print('查询当前交易出错')

if __name__ == "__main__":
    main()
