# -*- coding: utf-8 -*-
# @Time    :   2021/08/24 00:01:41
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   show_base_data.py
# @Software:   Visual Studio Code
# @Desc    :   None


import sys
import pickle

def run():
    symbol = sys.argv[1]
    file_name = ''
    with open(file_name, 'rb') as f:
        base_data = pickle.load(f)
    datas = base_data.get('data')
    for data in datas:
        if data.get('symbol').lower().startswith(symbol):
            print(data.get('data')[-1])
            exit(0)


if __name__ == "__main__":
    run()
