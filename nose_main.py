#  -*-coding:utf8-*-
# !/usr/bin/env python

import os
import threading
import traceback

import nose

from base import  devices_base_test
from devices_manager import appium_manager
from devices_manager import device_configuration
from util import log
from util import modules
from util import option

if __name__ == '__main__':

    test_support_list = list()
    support_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'web/supports.txt')
    )
    if os.path.isfile(support_path):
        for line in open(support_path):
            support = line.strip()
            test_support_list.append(support)
        os.remove(support_path)  # 删除case集结果文件，使得能够正常访问case选择页

    else:
        args_parser = option.args_parser
        test_modules_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'test_cases')
        )
        modules_parser = modules.ModulesParser(test_modules_dir)
        test_support_list = modules_parser.get_test_supports_by_args(args_parser, test_modules_dir)

    if test_support_list:
        #  当有可执行的case列表返回时，执行测试
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
                    log.logger.info("appium后台服务进程已开启,进程号为{}".format(process.pid + 1))

            threads = list()

            for index in range(0, device_count):
                argv = [__file__, '--debug=nose,nose.importer', '--debug-log=nose_debug', '-v', '--with-xunit',
                        '--xunit-file={}'.format('nosetests_' + str(index) + '.xml')]
                for temp_support in test_support_list:
                    argv.append(temp_support)

                curr_thread = threading.Thread(
                    target=nose.run, args=(),
                    kwargs={'argv': argv},
                    name='nose_run_'+str(index))
                threads.append(curr_thread)
                curr_thread.start()

            for thread in threads:
                thread.join()
        except Exception as e:
            log.logger.error('程序异常:'+str(e))
            traceback.print_exc()
        finally:
            am.kill_appium_processes()
