#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 手机键盘事件操作

Authors: Turinblueice
Date: 2016/7/26
"""

import time

from base import base_frame_view
from base import thread_device_pool
from util import config_initial, log


class KeyEventAction(object):

    def __init__(self, driver):
        self.__driver = driver
        self.__base_app = base_frame_view.BaseFrameView(self.__driver)
        self.__model_config = config_initial.config_parser

        # ******************多设备相关变量**********************

        self.__thread_number = thread_device_pool.ThreadDeviceInfoPool.get_current_thread_number()

    def back(self, activity_name=None, wait_time=5):
        """
            Summary:
                硬件后退
            Args:
                activity_name: 后退到某页面的页面名称
        """
        log.logger.info("点击硬件的后退键")
        keycode = 4
        if activity_name:
            while not self.__driver.current_activity == activity_name:
                self.__driver.keyevent(keycode)
                time.sleep(wait_time)
        else:
            self.__driver.keyevent(keycode)
        log.logger.info("后退完毕")

    def send_char(self, char, wait_time=5):
        """
            Summary:
                输入字符
        """
        log.logger.info("输入字符键")
        keycode = ord(char) - ord('a') + 29  # keycode:a~z,29~54
        self.__driver.keyevent(keycode)
        time.sleep(wait_time)
        log.logger.info("输入完毕")

    def send_string(self, string, wait_time=2):
        """
            输入字符串,暂不支持中文和大写英文字母
        Args:
            string:
            wait_time:

        Returns:

        """
        log.logger.info("开始输入字符串\"{}\"".format(string))
        for char in list(string):
            self.send_char(char, wait_time)
        log.logger.info("\"{}\"输入完毕".format(string))

    def send_proud_key(self, wait_time=3):
        """
            Summary:
                发送井号键
        Returns:

        """
        log.logger.info("发送井号键")
        keycode = 18
        self.__driver.keyevent(keycode)
        time.sleep(wait_time)
        log.logger.info("发送完毕")

