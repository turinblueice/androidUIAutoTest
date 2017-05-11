#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: appium服务管理(开启\关闭)模块

Authors: Turinblueice
Date:    16/4/15 15:13
"""
import platform
import re
import time

from devices_manager import available_ports
from devices_manager import command_prompt
from util import config_initial, log


class AppiumManager(object):

    """
        Summary:
            -
        Attribute:
    """
    def __init__(self):
        """
            Summary:
                -
            Attribute:
                cmd:
                port_repo:
                port_used:
        """
        super(AppiumManager, self).__init__()
        self.cmd = command_prompt.CommandPrompt()
        self.host = '127.0.0.1'
        self.port_repo = available_ports.AvailablePorts()
        self.port_used = list()
        self.platform = platform.system()
        self.postfix = 'win' if self.platform.lower() == 'windows' else 'linux'

    def start_appium_by_default(self, delay=3):

        default_port = 4723  # appium  服务默认端口
        cmd_str = config_initial.config_parser.get('cmd', 'start_default_appium_cmd_' + self.postfix)
        sub_process = self.cmd.run_command_async(cmd_str)
        time.sleep(delay)
        self.port_used.append(4723)

        return sub_process, default_port

    def start_appium(self, port=None, bootstrap_port=None, delay=3):
        """
            Args:
                - port 端口
                - delay 延迟的时间,单位秒
            Returns:
                tuple(sub_process, port)
                - sub_process: appium 服务开启的子进程
                - port : appium服务占用的端口
        """

        try:
            port = port or self.port_repo.get_port()
            bootstrap_port = bootstrap_port or self.port_repo.get_port()

            cmd_str = config_initial.config_parser.get('cmd', 'start_appium_cmd_' + self.postfix)
            cmd_str = cmd_str.replace('#port#', str(port))
            cmd_str = cmd_str.replace('#bootstrap_port#', str(bootstrap_port))
            log.logger.info("appium命令将开启:{}".format(cmd_str))
            sub_process = self.cmd.run_command_async(cmd_str)
            time.sleep(delay)
            self.port_used.append(port)
            return sub_process, port
        except:
            return None, None
    #
    # def get_status(self, port):
    #     """
    #         Summary:
    #             -  检查appium服务是否启动成功
    #     """
    #     if not self.port_used:
    #         log.logger.info('无端口启用,appium服务未开启!')
    #         return False
    #     if port not in self.port_used:
    #         log.logger.info('所给端口不在appium已开启的列表中')
    #         return False
    #
    #     host = self.host
    #     url = 'http://{host}:{port}/wd/hub/status'.format(host=host, port=port)
    #     try:
    #         resp = requests.get(url)
    #         json_obj = resp.json()
    #         if 'status' in json_obj and json_obj['status'] == 0:
    #             log.logger.info('appium服务已开启,url:{}'.format(url))
    #             return True
    #     except:
    #         log.logger.info('appium服务已开启失败,url:{}'.format(url))
    #         return False

    def find_appium_process(self):

        pid_list = []
        cmd_str = config_initial.config_parser.get('cmd', 'find_appium_cmd_' + self.postfix)

        output, status_code = self.cmd.run_command_sync(cmd_str)
        if status_code == 0:
            lines = output.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    pid = re.split('\s*', line)[1]
                    pid_list.append(pid)
        return pid_list

    def kill_appium_process_by_pid(self, pid, cmd_str=None):
        """
            Summary:
                关闭appium进程
            Args:
                pid： 进程号
        """

        cmd_str = cmd_str or config_initial.config_parser.get('cmd',
                                                     'kill_appium_cmd_' + self.postfix).replace('#pid#', str(pid))
        return_code = self.cmd.run_command_sync(cmd_str)[1]
        if return_code == 0:
            log.logger.info("已成功杀死进程ID为{}的appium服务".format(pid))
        else:
            log.logger.error("杀死进程ID为{}的appium服务失败".format(pid))

    def kill_appium_processes(self, pid_list=None):
        """
            Summary:
                批量关闭所有appium后台服务进程，如果pid_list为空，则直接根据appium进程指令名称来关闭进程
            Args:
                pid_list: 进程PID列表

        """

        if pid_list is not None:
            if not pid_list:
                log.logger.info("appium后台进程已全部清理完毕,无需再次清理")
                return

            for pid in pid_list:
                log.logger.info("关闭appium后台进程，进程号{}".format(pid))
                self.kill_appium_process_by_pid(pid)
        else:
            cmd_str = config_initial.config_parser.get('cmd', 'kill_appiums_cmd_' + self.postfix)
            log.logger.info("开始清理appium所有后台服务")
            output, return_code = self.cmd.run_command_sync(cmd_str)
            if return_code == 0:
                log.logger.info("已全部清理appium后台服务")
            else:
                log.logger.error("关闭所有appium后台服务失败，失败返回code：{}".format(return_code))
                log.logger.error("失败提示：{}".format(output))
