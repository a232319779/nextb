# -*- coding: utf-8 -*-
# @Time    :   2021/08/22 15:38:40
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   recommend.py
# @Software:   Visual Studio Code
# @Desc    :   None


from nextb.libs.utils.parsecmd import nextb_cmd_parse
from nextb.libs.utils.parseini import NextBParseINI
from nextb.libs.platform.nextbbinance import NextBBiance

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
    nbb.get_binance_klines_datas_update(interval=interval, limit=3)

if __name__ == "__main__":
    main()
