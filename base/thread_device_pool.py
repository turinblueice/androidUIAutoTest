#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 线程-设备(key-value)存储模块

Authors: Turinblueice
Date:    16/3/23 16:18
"""

import re
import threading

from util import config_initial


class ThreadDeviceInfoPool(object):
    """
        Summary:
            全局线程-设备存储容器类,存储各个线程-设备信息
    """

    thread_device_pool = dict()  # 线程-设备信息池,存储各个不同线程的字典容器
    model_config_parser = config_initial.config_parser

    @staticmethod
    def get_current_device(key=None):

        key = key or ThreadDeviceInfoPool.get_current_key()
        if key in ThreadDeviceInfoPool.thread_device_pool:
            if 'device' in ThreadDeviceInfoPool.thread_device_pool[key]:
                device = ThreadDeviceInfoPool.thread_device_pool[key]['device']

                device_name = device['device_brand'] + ' ' + device['device_model'] \
                    if device else ThreadDeviceInfoPool.model_config_parser.get(
                    'default_capabilities', 'device_name')

                device_name = re.sub('\s+', '_', device_name)

                platform_version = device['device_os_version'] \
                    if device else ThreadDeviceInfoPool.model_config_parser.get(
                    'default_capabilities', 'platform_version')

                udid = device['device_id'] \
                    if device else ThreadDeviceInfoPool.model_config_parser.get(
                    'default_capabilities', 'udid')
                return dict(device_name=device_name, device_id=udid, device_version=platform_version)
            return dict(device_id=config_initial.config_parser.get('default_capabilities', 'udid'))
        return None

    @staticmethod
    def get_current_key():
        """
            Summary:
                根据当前线程,获取key
        """
        thread_name = threading.currentThread().name
        thread_id = str(threading.currentThread().ident)  # 多线程运行需要绑定当前线程名称
        key = thread_name + '_' + thread_id

        return key

    @staticmethod
    def get_current_thread_id():

        thread_id = str(threading.currentThread().ident)
        return thread_id

    @staticmethod
    def get_current_thread_number():
        """
            Summary:
                获取当前线程编号
        """
        key = ThreadDeviceInfoPool.get_current_key()
        return ThreadDeviceInfoPool.thread_device_pool[key]['thread_number']

    @staticmethod
    def get_current_logger():

        key = ThreadDeviceInfoPool.get_current_key()
        logger = ThreadDeviceInfoPool.thread_device_pool[key]['log'] \
            if 'log' in ThreadDeviceInfoPool.thread_device_pool[key] else None
        return logger
