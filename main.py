#  -*-coding:utf8-*-
# !/usr/bin/env python

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
import threading
import traceback
import unittest

from base import devices_base_test
from devices_manager import appium_manager
from devices_manager import device_configuration
from util import log
from util import modules
from util import option

if __name__ == '__main__':

    args_parser = option.args_parser
    test_modules_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'test_cases')
    )

    modules_parser = modules.ModulesParser(test_modules_dir)

    test_suite = modules_parser.get_test_suite(args_parser, test_modules_dir)

    if test_suite:
        # 当有可执行的测试集合时，执行测试步骤
        process_list = list()
        am = appium_manager.AppiumManager()
        try:
            device_queue = devices_base_test.AppiumDevicesPortsInfo.device_queue
            ports_queue = devices_base_test.AppiumDevicesPortsInfo.ports_queue

            map(device_queue.put, device_configuration.DeviceConfiguration().get_devices())

            device_count = device_queue.qsize()

            for _ in range(0, device_count):
                process, port = am.start_appium()
                if process and port:
                    log.logger.info("appium服务已开启,进程ID为{},端口号为{}".format(process.pid, port))
                    ports_queue.put(port)
                    log.logger.info("端口号{}已进入队列".format(port))
                    process_list.append(process)
                    # linux/mac系统下, 尚不清楚为什么appium服务的实际进程ID号比Popen创建的pid大1
                    log.logger.info("appium后台服务进程已开启,进程号为{}".format(process.pid + 1))

            threads = list()
            for _ in range(0, device_count):

                test_runner = unittest.TextTestRunner(verbosity=2)
                curr_thread = threading.Thread(target=test_runner.run, args=(test_suite,))
                threads.append(curr_thread)
                curr_thread.start()

            for thread in threads:
                thread.join()
        except Exception as e:
            log.logger.error('程序异常:'+str(e))
            traceback.print_exc()
        finally:
            am.kill_appium_processes()
