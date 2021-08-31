# -*- coding: utf-8 -*-
# @Time    :   2021/08/24 00:01:41
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   show_base_data.py
# @Software:   Visual Studio Code
# @Desc    :   None


import sys
from nextb.libs.utils.basedata import BaseData

def run():
    file_name = '/home/pi/NextB/base.data'
    bd = BaseData(file_name)
    symbol = sys.argv[1]
    index = int(sys.argv[2])
    datas = bd.get_symbol_data(symbol)
    print(datas.get('data')[-index:])
            

if __name__ == "__main__":
    run()
