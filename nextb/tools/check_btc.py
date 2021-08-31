# -*- coding: utf-8 -*-
# @Time    :   2021/08/23 21:36:07
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   statics.py
# @Software:   Visual Studio Code
# @Desc    :   None


import sys
import pickle
import datetime


def run():
    time_dlt = int(sys.argv[1])
    file_name = '/home/pi/NextB/base.data'
    with open(file_name, 'rb') as f:
        base_data = pickle.load(f)

    datas = base_data.get('data')
    for data in datas:
        if data.get('symbol').lower().startswith('btcusdt'):
            btc_datas = data.get('data')[-time_dlt:]
    print('时间,涨跌幅,总涨跌幅,成交量,吃单量,吃单占比,交易量')
    base_price = float(btc_datas[0][1])
    for i in range(0, time_dlt):
        c_time = datetime.datetime.fromtimestamp(btc_datas[i][6]/1000).strftime('%Y-%m-%d %H')
        ratio = (float(btc_datas[i][4]) - float(btc_datas[i][1])) / float(btc_datas[i][1]) * 100
        qty = float(btc_datas[i][7])
        taker = float(btc_datas[i][10])
        taker_ratio = taker/qty * 100
        trades = int(btc_datas[i][8])
        total_ratio = (float(btc_datas[i][4]) - base_price) / base_price * 100
        print('%s,%.2f%%,%.2f%%,%.2f,%.2f,%.2f%%,%d' % (c_time, ratio, total_ratio, qty, taker, taker_ratio, trades))


if __name__ == "__main__":
    run()
