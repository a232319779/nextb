# -*- coding: utf-8 -*-
# @Time    :   2021/08/18 16:43:20
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   parsecmd.py
# @Software:   Visual Studio Code
# @Desc    :   None


import argparse

def nextb_cmd_parse():
    epilog = r"""
    Use like:
        1. set config.ini file and robot name
        python main.py -c config.ini -n core1
        """


    parser = argparse.ArgumentParser(prog='Leek Quantitative Trading Tools',
                                        description='A digital leek quantitative trading tool. Version 1.0.0',
                                        epilog=epilog,
                                        formatter_class=argparse.RawDescriptionHelpFormatter
                                        )
    parser.add_argument('-c', '--config', help='set config.ini file',
                        type=str, dest='config', action='store', default='./nextb/configs/config.ini')
    parser.add_argument('-n', '--name', help='set robot name',
                        type=str, dest='name', action='store', default='LeekRobot0')
    parser.add_argument('-d', '--db', help='use postgresql',
                        dest='db', action='store_true')

    args = parser.parse_args()

    return args
