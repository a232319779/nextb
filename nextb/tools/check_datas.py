# -*- coding: utf-8 -*-
# @Time    :   2021/08/30 14:32:42
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   check_datas.py
# @Software:   Visual Studio Code
# @Desc    :   None


import datetime
import pickle

from nextb.libs.utils.parsecmd import nextb_cmd_parse
from nextb.libs.utils.parseini import NextBParseINI
from nextb.libs.platform.nextbbinance import NextBBiance

def run():
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
    nbb = NextBBiance(
        api_key=api_key, api_secret=api_secret, proxies=proxies, increasing=True
    )
    live_datas = nbb.get_klines_inc('BTCUSDT', limit=100)
    file_name = '/home/pi/NextB/base.data'
    with open(file_name, 'rb') as f:
        base_data = pickle.load(f)
    datas = base_data.get('data')
    now = datetime.datetime.now()
    for data in datas:
        if data.get('symbol').lower().startswith('btcusdt'):
            offline_datas = data.get('data')[-100:]
    for i in range(1, 100):
        if offline_datas[100-i][1] == live_datas[100-i-1][1]:
            # dlt = datetime.timedelta(hours=i+1)
            # loss_time = now - dlt
            # print('%s数据没有缺失' % loss_time.strftime('%Y-%m-%d %H'))
            continue
        else:
            dlt = datetime.timedelta(hours=i+1)
            loss_time = now - dlt
            print('!!!缺失索引: %d, 缺失时间: %s, 上一个数据: %s, 下一个数据: %s!!!' % (
                i, loss_time.strftime('%Y-%m-%d %H'), offline_datas[100-i+1][1], offline_datas[100-i][1]))
            

if __name__ == "__main__":
    run()
