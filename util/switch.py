#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 开关模块，控制工程在何种模式下运行。debug模式：可在编译器内单个执行；release模式：运行clients_main.py脚本执行

Authors: Turinblueice
Date: 2016/7/28
"""
import os
import ConfigParser


class Switch(object):
    """
        Summary:
            开关类
    """
    def __init__(self):
        self.__switch_config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../configs/switch.conf')
        )
        self.__model_config = ConfigParser.ConfigParser()
        self.__model_config.read(self.__switch_config_path)

    @property
    def debug(self):
        mode = self.__model_config.get('mode', 'debug')
        return True if mode == 'True' else False

switch = Switch()
