# -*- coding: utf-8 -*-
# @Time    :   2021/08/23 21:36:07
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   statics.py
# @Software:   Visual Studio Code
# @Desc    :   None


import pickle
from nextb.libs.db.nextbDB import NextBDB


def main():
    db = NextBDB()
    datas = db.search_datas('LeekRobot0')

    file_name = '/home/pi/NextB/base.data'
    with open(file_name, 'rb') as f:
        symbol_datas = pickle.load(f)
    
    print('买入时间\t买入币种\t买入价格\t1小时涨跌幅\t2小时涨跌幅\t3小时涨跌幅\t4小时涨跌幅\t最大亏损\t最大盈利')
    low_sum = 1000.0
    high_sum = 1000.0
    for i in range(-1, -25, -1):
        buy_time = datas[i].to_dict().get('time').strftime('%Y-%m-%d %H:00:00')[:13]
        recommond_symbols = datas[i].to_dict().get('symbols')
        if recommond_symbols:
            buy_symbol = recommond_symbols.split(',')[0]
            if not buy_symbol.endswith('USDT'):
                buy_symbol += 'USDT'
            for sd in symbol_datas.get('data'):
                if buy_symbol != sd.get('symbol'):
                    continue
                buy_price = float(sd.get('data')[-29-i][4])
                buy_price_1 = float(sd.get('data')[-29-i+1][4])
                buy_price_2 = float(sd.get('data')[-29-i+2][4])
                buy_price_3 = float(sd.get('data')[-29-i+3][4])
                buy_price_4 = float(sd.get('data')[-29-i+4][4])
                high_price_1 = float(sd.get('data')[-29-i+1][2])
                high_price_2 = float(sd.get('data')[-29-i+2][2])
                high_price_3 = float(sd.get('data')[-29-i+3][2])
                high_price_4 = float(sd.get('data')[-29-i+4][2])
                low_price_1 = float(sd.get('data')[-29-i+1][3])
                low_price_2 = float(sd.get('data')[-29-i+2][3])
                low_price_3 = float(sd.get('data')[-29-i+3][3])
                low_price_4 = float(sd.get('data')[-29-i+4][3])
                lowest_price = min([low_price_1, low_price_2, low_price_3, low_price_4])
                highest_price = max([high_price_1, high_price_2, high_price_3, high_price_4])
                low_sum = low_sum + low_sum * (lowest_price - buy_price)/buy_price
                high_sum = high_sum + high_sum * (highest_price - buy_price)/buy_price
                # print('%s时\t%s\t%.5f\t%.2f%%,%.2f%%,%.2f%%\t%.2f%%,%.2f%%,%.2f%%\t%.2f%%,%.2f%%,%.2f%%\t%.2f%%,%.2f%%,%.2f%%\t%.5f\t%.5f' % (
                #     buy_time, buy_symbol.replace('USDT', ''), buy_price,
                #     (low_price_1-buy_price)/buy_price*100,
                #     (buy_price_1-buy_price)/buy_price*100,
                #     (high_price_1-buy_price)/buy_price*100,
                #     (low_price_2-buy_price)/buy_price*100,
                #     (buy_price_2-buy_price)/buy_price*100,
                #     (high_price_2-buy_price)/buy_price*100,
                #     (low_price_3-buy_price)/buy_price*100,
                #     (buy_price_3-buy_price)/buy_price*100,
                #     (high_price_3-buy_price)/buy_price*100,
                #     (low_price_4-buy_price)/buy_price*100,
                #     (buy_price_4-buy_price)/buy_price*100,
                #     (high_price_4-buy_price)/buy_price*100,
                #     lowest_price-buy_price,
                #     highest_price-buy_price))
                print('%s时\t%s\t%.5f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.5f\t%.5f' % (
                    buy_time, buy_symbol.replace('USDT', ''), buy_price,
                    (buy_price_1-buy_price)/buy_price*100,
                    (buy_price_2-buy_price)/buy_price*100,
                    (buy_price_3-buy_price)/buy_price*100,
                    (buy_price_4-buy_price)/buy_price*100,
                    lowest_price-buy_price,
                    highest_price-buy_price))
                break
        else:
            print('%s时\t没有推荐\t0' % (buy_time))
    print('最大亏损: %.5f, 最大盈利:%.5f' % (low_sum, high_sum))

if __name__ == "__main__":
    main()
