# -*- coding: utf-8 -*-
# @Time     : 2022/03/18 15:55:27
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : download_datas.py
# @Software : Visual Studio Code
# @WeChat   : NextB

import json
from nextb.libs.platform.nextbbinance import NextBBiance


def main():
    # 传入api_key可以实现下载指定币种的数据
    nb = NextBBiance(api_key='', increasing=False)
    symbols = nb.symbols
    i = 0
    # startTime = 1609459200000
    # endTime = 1640995200000
    startTime = 1640995200000
    endTime = 1648631744000
    total_datas = list()
    for symbol in symbols:
        if symbol.get('status', '') == 'TRADING' and 'SPOT' in symbol.get('permissions', []):
            if symbol.get('quoteAsset', '') == 'USDT':
                symbol_name = symbol.get('symbol', '')
                if not symbol_name.endswith('DOWNUSDT') and \
                    not symbol_name.endswith('UPUSDT') and \
                        symbol_name not in ('USDCUSDT', 'BUSDUSDT', 'PAXUSDT', 'TUSDUSDT', 'USDSBUSDT', 'SUSDUSDT'):
                        datas = list()
                        # 一年是18，一个季度是5
                        for t in range(0, 5):
                            search_time = startTime + t * 500 * 60 * 60 * 1000
                            data = nb.client.get_klines(symbol=symbol_name, interval='1h', limit=500, startTime=search_time, endTime=endTime)
                            datas.extend(data)
                        tmp = {
                            "symbol": symbol_name,
                            "symbol_index": i,
                            "data": datas
                        }
                        total_datas.append(tmp)
        i += 1
    file_name = 'base_2022_01_03.data'
    with open(file_name, "w") as f:
        f.write(json.dumps(total_datas))


if __name__ == '__main__':
    main()
