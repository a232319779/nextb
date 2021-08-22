# -*- coding: utf-8 -*-
# @Time    :   2021/08/18 17:05:18
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   core.py
# @Software:   Visual Studio Code
# @Desc    :   None

import numpy as np
import talib as TA
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
from nextb.libs.robot.robot import Robot

__doc__ = """
这是韭菜0号，其核心内容为：

1. 计算MA7、MA25、MA99的值，选择MA99在最下方，MA7从下往上突破MA25的币种
	1. MA7在MA25下方的指标数量（面积，百分比求和）：K1
	2. MA7在MA25下方的收敛趋势（是否是越来越靠近，可能形成突破）：K2
2. 计算MACD，选择DIF与DEA都为负值并且DIF由下向上突破DEA的币种
	1. DIF和DEA都在0轴下方的指标数量（面积，百分比求和）：M1
	2. DIF在DEA下方的指标数量（面积，百分比求和）：M2
	3. DIF在DEA下方的收敛趋势（是否是越来越靠近，可能形成突破）：M3
3. 选择1小时作为时间间隔，如MA7表示7小时的平均值
4. 对1、2的计算结果做归一化，选择数据展示最好的那一个币种，同时统计最近24小时成交额，选择成交额最大的作为买入币种
5. 当收益达到+1.5%、-2.0%、持有时间超过4小时，则卖出
"""

class LeekRobot0(Robot):
    def __init__(self):
        pass

    def klines_analysis(self, data):
        try:
            close = [float(d[4]) for d in data]
            ma7 = TA.MA(np.array(close), timeperiod=7)
            ma25 = TA.MA(np.array(close), timeperiod=25)
            ma99 = TA.MA(np.array(close), timeperiod=99)
            ma7_25 = ma7 - ma25
            # 排除当前小时的计算
            ma7_25 = ma7_25[:-1]
            # 当ma7由下往上突破ma25时，ma7-ma25的值应该是负值
            K1 = self.under_quote(ma7_25)
            K2 = self.neg_convergence_quote(ma7_25)
        except Exception as e:
            print('klines analysis failed: %s' % str(e), flush=True)
            ma7 = None
            K1 = -1
            K2 = -1
        
        return [K1, K2]

    def macd_analysis(self, data):
        try:
            close = [float(d[4]) for d in data]
            dif, dea, macd = TA.MACD(np.array(close), fastperiod=12, slowperiod=26, signalperiod=9)
            dif_dea = dif - dea
            dif_macd = dif - macd
            # 排除当前小时的计算
            dif_dea = dif_dea[:-1]
            dif_macd = dif_macd[:-1]
            M1 = self.under_quote(dif_macd)
            # 当dif和dea都在0轴下方时，dif和dea都为负数，且dif由下往上突破dea时，dif-dea的值应该是负值
            M2 = self.under_quote(dif_dea)
            M3 = self.neg_convergence_quote(dif_dea)
        except Exception as e:
            print('macd analysis failed: %s' % str(e), flush=True)
            M1 = -1
            M2 = -1
            M3 = -1

        return [M1, M2, M3]

    def analysis(self, data):
        r_data = {'symbol': data.get('symbol'), 'symbol_index': data.get('symbol_index', -1), 'r': list()}
        data_ = data.get('data', [])
        k_data = self.klines_analysis(data_)
        r_data['r'].extend(k_data)
        m_data = self.macd_analysis(data_)
        r_data['r'].extend(m_data)
        if all(k_data) and all(m_data):
            # 添加最近25小时成交额
            turnover = [float(d[7]) for d in data_]
            sum = self.sum_of_turnover(turnover, 25)
            r_data['r'].append(sum)
            return r_data
        else:
            return None


def work(datas):
    choose_list = list()
    LR0 = LeekRobot0()
    for data in datas:
        try:
            r_data = LR0.analysis(data)
            if r_data:
                choose_list.append(r_data)
        except Exception as e:
            print('%s,error,%s' % (data.get('symbol'), e), flush=True)
    return choose_list

def analysis(datas):
    max_workers = 4
    number = len(datas)
    dlt = int(number / max_workers)
    if dlt == 0:
        dlt = number
    choose_list = list()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        all_task = [executor.submit(work, datas[k:k+dlt]) for k in range(0, number, dlt)]
        wait(all_task, return_when=ALL_COMPLETED)
        for task in all_task:
            result = task.result()
            choose_list.extend(result)
    choose_list.sort(key=lambda x:x.get('r')[-1], reverse=True)
    print('symbol,symbol_index,K1,K2,M1,M2,M3,sum')
    for r in choose_list:
        if r:
            print('%s,%d,%s' % (r.get('symbol'), r.get('symbol_index'), ','.join([str(a) for a in r.get('r', [])])))
    return choose_list
