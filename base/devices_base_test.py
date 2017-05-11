#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 多客户端执行和管理模块

Authors: Turinblueice
Date:    16/4/19 12:00
"""

import Queue
import os
import threading

from appium import webdriver

from base import app_unit_test
from base import thread_device_pool
from devices_manager import available_ports
from util import config_initial, log
from util import switch
import re

from plugin.html_report_plugin import html_plugin


class AppiumDevicesPortsInfo(object):
    device_queue = Queue.Queue()
    ports_queue = Queue.Queue()  # 端口队列


class DevicesBaseTest(app_unit_test.AppTestCase):

    """
        Summary:
            - 多客户端执行管理类
    """
    config_model = config_initial.config_parser
    mutex = threading.Lock()
    curr_host = available_ports.AvailablePorts.get_local_ip()

    def __init__(self, *args, **kwargs):
        super(DevicesBaseTest, self).__init__(*args, **kwargs)

        self.device = None
        self.package_name = kwargs.get('package', 'com.jiuyan.infashion')  # 包名
        self.platform = kwargs.get('platform', 'android')  # 平台

        # *************运行方式控制属性*************
        self.debug_mode = switch.switch.debug

    @staticmethod
    def app_path(file_path):

        return os.path.abspath(os.path.join(os.path.dirname(__file__), file_path))

    @staticmethod
    def create_driver(debug=False):
        """
            Summary:
                创建webdriver
            Args:
                debug:调试模式
        """
        key = DevicesBaseTest.get_current_key()
        config_model = DevicesBaseTest.config_model

        if not debug:

            if key not in thread_device_pool.ThreadDeviceInfoPool.thread_device_pool:
                # 若当前线程不在全局线程字典内,则该线程入栈
                with DevicesBaseTest.mutex:
                    # 加锁,确保逐个进入线程字典,如此不会导致字典元素数量编号出错
                    thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key] = dict()

                    thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['port'] = \
                        AppiumDevicesPortsInfo.ports_queue.get_nowait() \
                        if not AppiumDevicesPortsInfo.ports_queue.empty() else None

                    device = AppiumDevicesPortsInfo.device_queue.get_nowait() \
                        if not AppiumDevicesPortsInfo.device_queue.empty() else None
                    thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['device'] = device

                    device_name = device['device_brand'] + ' ' + device['device_model'] \
                        if device else config_model.get('default_capabilities', 'device_name')
                    # 增加报告
                    thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['html_report'] = \
                        html_plugin.HtmlOutput(
                            report_file=html_plugin.get_html_report_path(device=re.sub(r'\s+', '_', device_name)))

                    thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['thread_number'] = \
                        str(len(thread_device_pool.ThreadDeviceInfoPool.thread_device_pool))  # 对当前线程进行编号

                    log.logger.info(
                        "当前线程名称为{},ID为{},编号为{}".format(
                            threading.currentThread().name,
                            threading.currentThread().ident,
                            thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['thread_number']))

            port = thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['port']
            device = thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['device']

            port = port or 4723

            device_name = device['device_brand'] + ' ' + device['device_model'] \
                if device else config_model.get('default_capabilities', 'device_name')

            platform_version = device['device_os_version'] \
                if device else config_model.get('default_capabilities', 'platform_version')

            udid = device['device_id'] if device else config_model.get('default_capabilities', 'udid')

            log.logger.info("设备名称:{},设备ID:{},使用端口:{},运行线程:{}".format(
                device_name, udid, port, threading.currentThread().ident))

            driver = webdriver.Remote(
                command_executor='http://{host}:{port}/wd/hub'.format(host=DevicesBaseTest.curr_host, port=port),
                desired_capabilities={
                    'app': DevicesBaseTest.app_path(config_model.get('default_capabilities', 'app')),
                    'platformName': config_model.get('default_capabilities', 'platform_name'),
                    'platformVersion': platform_version,
                    'deviceName': device_name,  # IOS：instruments -s devices；Android:随便写
                    'udid': udid,  # 设备号
                    'appPackage': config_model.get('default_capabilities', 'app_package'),
                    #  'appActivity': '.business.login.ui.LoginActivity'#登录页的acitivity
                    'unicodeKeyboard': True,
                    'resetKeyboard': True,
                    'appActivity': '.LaunchActivity'

                })

        else:

            device_name = config_model.get('default_capabilities', 'device_name')

            port = 4723
            driver = webdriver.Remote(
                command_executor='http://{host}:{port}/wd/hub'.format(host=DevicesBaseTest.curr_host, port=port),
                desired_capabilities={
                    'app': DevicesBaseTest.app_path(config_model.get('default_capabilities', 'app')),
                    'platformName': 'Android',
                    'platformVersion': config_model.get('default_capabilities', 'platform_version'),
                    'deviceName': device_name,  # IOS：instruments -s devices；Android:随便写
                    'appPackage': config_model.get('default_capabilities', 'app_package'),
                    'unicodeKeyboard': True,
                    'resetKeyboard': True,
                    'noReset': True,
                    'appActivity': '.LaunchActivity'

                })

            device_name = re.sub(r'\s+', '_', device_name)

            thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key] = dict()
            thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['html_report'] = \
                html_plugin.HtmlOutput(
                    report_file=html_plugin.get_html_report_path(device=device_name))
            thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['thread_number'] = '1'

        thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['driver'] = driver
        log.logger.info("该线程id:{},driver地址{}".format(threading.currentThread().ident, id(driver)))

        return driver

    @staticmethod
    def get_current_key():

        key = thread_device_pool.ThreadDeviceInfoPool.get_current_key()
        return key

    @staticmethod
    def get_current_device():

        device = thread_device_pool.ThreadDeviceInfoPool.get_current_device()
        return device

    @staticmethod
    def get_driver():

        key = DevicesBaseTest.get_current_key()
        if key in thread_device_pool.ThreadDeviceInfoPool.thread_device_pool:
            if 'driver' in thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]:
                driver = thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['driver']
                return driver
        return None

    @staticmethod
    def get_current_thread_number():
        """
            Summary:
                获取当前线程编号
        """
        key = DevicesBaseTest.get_current_key()
        return thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['thread_number']

    @staticmethod
    def get_current_html_reporter():
        """
        获取当前线程的报告
        :return:
        """
        key = DevicesBaseTest.get_current_key()
        return thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['html_report']

    @staticmethod
    def get_current_thread_id():

        thread_id = thread_device_pool.ThreadDeviceInfoPool.get_current_thread_id()
        return thread_id

    @staticmethod
    def get_current_thread_number():
        """
            Summary:
                获取当前线程编号
        """
        key = DevicesBaseTest.get_current_key()
        return thread_device_pool.ThreadDeviceInfoPool.thread_device_pool[key]['thread_number']