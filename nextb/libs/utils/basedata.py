# -*- coding: utf-8 -*-
# @Time    :   2021/08/30 16:36:14
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   basedata.py
# @Software:   Visual Studio Code
# @Desc    :   None


import pickle

class BaseData(object):
    def __init__(self, file_name='/home/pi/NextB/base.data'):
        with open(file_name, 'rb') as f:
            self.datas = pickle.load(f)

    def get_all_data(self, index):
        datas = self.datas.get('data')
        for data in datas:
            del data['data'][index:]
        return datas

    def get_symbol_data(self, symbol):
        datas = self.datas.get('data')
        for data in datas:
            if data.get('symbol').lower().startswith(symbol.lower()):
                return data

    def get_symbol_qty(self, symbol, limit=5):
        datas = self.get_symbol_data(symbol)
        qty = 0.0
        for data in datas.get('data')[-limit:]:
            qty += float(data[10])

        return qty

def main():
    bd = BaseData()
    print(bd.get_symbol_qty('bnbusdt', 10))


if __name__ == "__main__":
    main()
