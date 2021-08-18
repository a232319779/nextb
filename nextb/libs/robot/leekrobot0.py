# -*- coding: utf-8 -*-
# @Time    :   2021/08/18 17:05:18
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   core.py
# @Software:   Visual Studio Code
# @Desc    :   None


__doc__ = """
这是韭菜0号，其核心内容为：

1. 计算MA7、MA25、MA99的值，选择MA99在最下方，MA7从下往上突破MA25的币种
2. 计算MACD，选择DIF与DEA都为负值并且DIF由下向上突破DEA的币种
3. 选择1小时作为时间间隔，如MA7表示7小时的平均值
4. 对1、2的计算结果做归一化，选择数据展示最好的那一个币种，作为买入币种
5. 当收益达到+1.5%、-2.0%、持有时间超过4小时，则卖出
"""

class LeekRobot0(object):
    def __init__(self):
        pass