#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:

Authors: Turinblueice
Date: 2016/7/26
"""

import os
import logging
import logging.handlers
import platform
from base import thread_device_pool


def init_log(log_path, log_name=None, level=logging.INFO, when="D", backup=7,
             format_str="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d: %(message)s",
             date_fmt="%y-%m-%d %H:%M:%S"):
    """
    Summary:

        init_log - initialize log module

    @:param
    Args：
        log_path      - Log file path prefix.
                      Log data will go to two files: log_path.log and log_path.log.wf
                      Any non-exist parent directories will be created automatically

        log_name      - name of log
        level         - msg above the level will be displayed
                      DEBUG < INFO < WARNING < ERROR < CRITICAL
                      the default value is logging.INFO
        when          - how to split the log file by time interval
                      'S' : Seconds
                      'M' : Minutes
                      'H' : Hours
                      'D' : Days
                      'W' : Week day
                      default value: 'D'
        format_str        - format of the log
                      default format:
                      %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                      INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
        backup        - how many backup file to keep
                      default value: 7

    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    """

    my_logger = logging.getLogger(log_name)
    my_logger.setLevel(level)

    formatter = logging.Formatter(format_str, date_fmt)

    dir_name = os.path.dirname(log_path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    curr_platform = platform.system().lower()

    handler = logging.handlers.TimedRotatingFileHandler(
        log_path + ".log", when=when, backupCount=backup) if not curr_platform == 'windows' else logging.FileHandler(
        log_path + ".log")

    handler.setLevel(level)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)

    handler = logging.handlers.TimedRotatingFileHandler(
        log_path + ".log.wf", when=when, backupCount=backup) if not curr_platform == 'windows' else logging.FileHandler(
        log_path + ".log.wf")
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)

    return my_logger

# logger = init_log((lambda log_path:
#                    os.path.abspath(os.path.join(os.path.dirname(__file__), log_path)))('../outputs/logs/kdt'))


class RunningLog(object):
    """
        Summary:
            优化log模块
    """
    def __init__(self, log_path, log_name=None, level=logging.INFO, when="D", backup=7,
                 format_str="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d: %(message)s",
                 date_fmt="%y-%m-%d %H:%M:%S"):

        """
        init_log - initialize log module
        Args:
          log_path      - Log file path prefix.
                          Log data will go to two files: log_path.log and log_path.log.wf
                          Any non-exist parent directories will be created automatically

          log_name      - name of log
          level         - msg above the level will be displayed
                          DEBUG < INFO < WARNING < ERROR < CRITICAL
                          the default value is logging.INFO
          when          - how to split the log file by time interval
                          'S' : Seconds
                          'M' : Minutes
                          'H' : Hours
                          'D' : Days
                          'W' : Week day
                          default value: 'D'
          format_str        - format of the log
                          default format:
                          %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                          INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
          backup        - how many backup file to keep
                          default value: 7

        Raises:
            OSError: fail to create log directories
            IOError: fail to open log file
        """
        self.__my_logger = logging.getLogger(log_name)
        self.__my_logger.setLevel(level)

        formatter = logging.Formatter(format_str, date_fmt)

        dir_name = os.path.dirname(log_path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        curr_platform = platform.system().lower()

        handler = logging.handlers.TimedRotatingFileHandler(
            log_path + ".log", when=when, backupCount=backup) if not curr_platform == 'windows' else logging.FileHandler(
            log_path + ".log")
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.__my_logger.addHandler(handler)

        handler = logging.handlers.TimedRotatingFileHandler(
            log_path + ".log.wf", when=when, backupCount=backup) if not curr_platform == 'windows' else logging.FileHandler(
            log_path + ".log.wf")
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        self.__my_logger.addHandler(handler)

        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.__my_logger.addHandler(handler)

    def info(self, message):

        device = thread_device_pool.ThreadDeviceInfoPool.get_current_device()

        # 如果设备信息尚未初始化,则用当前线程ID来代替tag
        device_name_tag = device['device_name'] if device \
            else thread_device_pool.ThreadDeviceInfoPool.get_current_thread_id()
        self.__my_logger.info('[{}]:{}'.format(device_name_tag, message))

    def warning(self, message):
        device = thread_device_pool.ThreadDeviceInfoPool.get_current_device()

        # 如果设备信息尚未初始化,则用当前线程ID来代替tag
        device_name_tag = device['device_name'] if device \
            else thread_device_pool.ThreadDeviceInfoPool.get_current_thread_id()
        self.__my_logger.warning('[{}]:{}'.format(device_name_tag, message))

    def error(self, message):
        device = thread_device_pool.ThreadDeviceInfoPool.get_current_device()

        # 如果设备信息尚未初始化,则用当前线程ID来代替tag
        device_name_tag = device['device_name'] if device \
            else thread_device_pool.ThreadDeviceInfoPool.get_current_thread_id()
        self.__my_logger.error('[{}]:{}'.format(device_name_tag, message))


my_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../outputs/logs/in.log'))

# logger = RunningLog(log_path=my_log_path)
logger = init_log(my_log_path)



