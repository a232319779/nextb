# -*- coding: utf-8 -*-
# @Time    :   2021/08/18 16:42:40
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   parseini.py
# @Software:   Visual Studio Code
# @Desc    :   None


import configparser


class NextBParseINI(object):
    def __init__(self, config_name):
        self.config = configparser.ConfigParser()
        self.config.read(config_name)
    
    def get_robot_config(self, config_index):
        robot_x = self.config['LEEK_ROBOT_%d' % config_index]
        config_dict = {}
        for key in robot_x:
            config_dict[key] = robot_x[key]
        
        return config_dict
