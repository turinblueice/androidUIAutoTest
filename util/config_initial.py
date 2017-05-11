#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 数据model

Authors: Turinblueice
Date:    16/4/19 12:00
"""

import ConfigParser
import os

from util import option


class ModelConfig(object):

    def __init__(self, online=False):
        self.__model_config = ConfigParser.ConfigParser()

        self.__model_file = 'qatest_stat_model.conf' if not online else 'online_stat_model.conf'
        self.__model_config.read(os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '../configs/'+self.__model_file
            )
        ))

    def get_config_parser(self):

        return self.__model_config

config_parser = ModelConfig(option.args_parser.online if option.args_parser else False).get_config_parser()
