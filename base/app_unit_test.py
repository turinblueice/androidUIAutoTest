# -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 商家版单测模块

Authors: Turinblueice
Date:    16/3/23 16:18
"""

import traceback
import unittest

from base import base_frame_view
from plugin.html_report_plugin import html_plugin
from util import log
from base import thread_device_pool
import os
import datetime


class AppTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(AppTestCase, self).__init__(*args, **kwargs)

    @staticmethod
    def get_current_html_reporter():
        pass

    def assert_and_save_screen_shot(self, obj, screen_shot_name, expected, actual, msg=None):
        """
        Args:
            obj: BaseFrameView对象
        Return:
        """

        try:
            super(AppTestCase, self).assertEqual(expected, actual, msg)
        except:
            if isinstance(obj, base_frame_view.BaseFrameView):
                obj.save_screen_shot(screen_shot_name)
            else:
                log.logger.error('截图失败,截图对象不是BaseFrameView类型。')
            tmp_msg = '期待结果:{},实际结果:{}。失败信息:'.format(expected, actual)
            tmp_msg += msg

            #  抛出已捕获的异常, 供上层捕获判断用例失败
            raise self.failureException(tmp_msg)

    @staticmethod
    def raise_exp_and_save_screen_shot(obj, case_name, exp):
        """
        Summary:
            截图并抛出截获的异常
        Args:
            obj: 测试framework对象，如activity、控件对象等
            case_name: 测试用例名称
            exp: 引发的异常对象
        Return:
        """
        log.logger.error(str(exp))
        log.logger.error(traceback.format_exc())
        if isinstance(obj, base_frame_view.BaseFrameView):
            obj.save_screen_shot(case_name)
        else:
            log.logger.error('截图失败,截图对象不是BaseFrameView类型。')
        raise exp

    def assertTrue(self, expr, msg=None, case_name=None):
        """
            Summary:
                重写TestCase类的assertTrue方法
        Args:
            expr:
            msg:

        Returns:

        """
        if case_name:
            try:
                super(AppTestCase, self).assertTrue(expr, msg)
                self.get_current_html_reporter().add_success(case_name)
            except self.failureException as exp:
                self.get_current_html_reporter().add_failure(case_name)
                raise exp
        else:
            super(AppTestCase, self).assertTrue(expr, msg)

    def assertEqual(self, first, second, msg=None, case_name=None):
        """
            Summary:
                重写TestCase类的assertEqual方法
        Args:
            expr:
            msg:

        Returns:

        """
        if case_name:
            try:
                super(AppTestCase, self).assertEqual(first, second, msg)
                self.get_current_html_reporter().add_success(case_name)
            except self.failureException as exp:
                self.get_current_html_reporter().add_failure(case_name)
                raise exp
        else:
            super(AppTestCase, self).assertEqual(first, second, msg)

    def assertNotEqual(self, first, second, msg=None, case_name=None):
        """
            Summary:
                重写TestCase类的assertNotEqual方法
        Args:
            expr:
            msg:

        Returns:

        """
        if case_name:
            try:
                super(AppTestCase, self).assertNotEqual(first, second, msg)
                self.get_current_html_reporter().add_success(case_name)
            except self.failureException as exp:
                self.get_current_html_reporter().add_failure(case_name)
                raise exp
        else:
            super(AppTestCase, self).assertNotEqual(first, second, msg)