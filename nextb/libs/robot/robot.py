# -*- coding: utf-8 -*-
# @Time    :   2021/08/21 14:55:24
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   robot.py
# @Software:   Visual Studio Code
# @Desc    :   None


__doc__ = """
这是机器人的爸爸
"""

class Robot(object):
    def __init__(self):
        pass

    @staticmethod
    def neg_convergence_quote(L):
        """
        计算L从负数方向是否收敛于0
        """
        r = [x <= y for x, y in zip(L[:-2], L[1:])]
        quote = 0
        for i in range(len(r) - 1, 0, -1):
            if r[i] == True:
                quote += 1
            else:
                break

        return quote
    
    @staticmethod
    def pos_convergence_quote(L):
        """
        计算L从正数方向是否收敛于0
        """
        r = [x >= y for x, y in zip(L[:-2], L[1:])]
        quote = 0
        for i in range(len(r) - 1, 0, -1):
            if r[i] == True:
                quote += 1
            else:
                break

        return quote

    @staticmethod
    def under_quote(L):
        """
        统计L小于0的归一化求和大小
        """
        quote = 0.0
        min_data = min(L[-25:])
        for i in range(len(L) - 1, 0, -1):
            if L[i] <= 0:
                quote += L[i] / min_data
            else:
                break

        return quote

    @staticmethod
    def upper_quote(L):
        """
        统计L大于0的归一化求和大小
        """
        quote = 0.0
        min_data = min(L[-25:])
        for i in range(len(L) - 1, 0, -1):
            if L[i] >= 0:
                quote += L[i] / min_data
            else:
                break

        return quote

    @staticmethod
    def sum_of_turnover(data, dlt=25):
        return sum(data[-dlt:])

