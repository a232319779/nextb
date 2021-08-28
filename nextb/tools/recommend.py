# -*- coding: utf-8 -*-
# @Time    :   2021/08/22 15:38:40
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   recommend.py
# @Software:   Visual Studio Code
# @Desc    :   None


import datetime

from nextb.libs.utils.parsecmd import nextb_cmd_parse
from nextb.libs.utils.parseini import NextBParseINI
from nextb.libs.platform.nextbbinance import NextBBiance
from nextb.libs.robot.leekrobot0 import analysis
from nextb.libs.db.nextbDB import NextBDB

def main():
    cmd_args = nextb_cmd_parse()
    robot_name = cmd_args.name
    config_path = cmd_args.config
    nbpi = NextBParseINI(config_path)
    robot_config = nbpi.get_robot_config(robot_name)
    proxies = {
        "http": robot_config.get("http_proxy", ''),
        "https": robot_config.get("https_proxy", '')
    }
    api_key = robot_config.get("api_key")
    api_secret = robot_config.get("api_secret")
    interval = robot_config.get("klines_interval")
    nbb = NextBBiance(
        api_key=api_key, api_secret=api_secret, proxies=proxies, increasing=True
    )
    datas = nbb.get_binance_klines_datas_inc(interval=interval, limit=2)

    choose_list = analysis(datas)
    if cmd_args.db:
        db = NextBDB()
        recommond_data = {'robot_name': 'LeekRobot0', 'symbols': '', 'time': datetime.datetime.now()}
        symbols = ','.join([cl.get('symbol','ddvv') for cl in choose_list])
        recommond_data['symbols'] = symbols
        if symbols:
            recommond_data['count'] = symbols.count(',') + 1
        else:
            recommond_data['count'] = 0
        db.add_data(recommond_data)

if __name__ == "__main__":
    main()
