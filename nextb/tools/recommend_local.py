# -*- coding: utf-8 -*-
# @Time    :   2021/08/22 15:38:40
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   recommend.py
# @Software:   Visual Studio Code
# @Desc    :   None


import sys
import datetime

from nextb.libs.robot.leekrobot0 import analysis
from nextb.libs.db.nextbDB import NextBDB
from nextb.libs.utils.basedata import BaseData

def run():
    bd = BaseData()
    time_dlt = int(sys.argv[1])
    insert_time = datetime.datetime.now() + datetime.timedelta(hours=time_dlt)
    datas = bd.get_all_data(time_dlt)
    choose_list = analysis(datas)
    db = NextBDB()
    recommond_data = {'robot_name': 'LeekRobot0', 'symbols': '', 'time': insert_time}
    symbols = ','.join([cl.get('symbol','ddvv') for cl in choose_list])
    recommond_data['symbols'] = symbols
    if symbols:
        recommond_data['count'] = symbols.count(',') + 1
    else:
        recommond_data['count'] = 0
    db.add_data(recommond_data)

if __name__ == "__main__":
    run()
