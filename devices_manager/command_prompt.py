#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
command_prompt模块,命令行程序执行类

Authors: Turinblueice
Date:    16/4/13 12:04
"""

import platform
import subprocess


class CommandPrompt(object):

    def __init__(self):
        super(CommandPrompt, self).__init__()
        self.platform = platform.system()

    def run_command_sync(self, cmd_str):

        """
            Summary:
                同步执行命令行命令,等待自进程运行结束
            Args:
                cmd_str: 命令行字符串
            Returns:
                命令行执行的标准输出信息
        """
        return_code = 0
        if self.platform.lower() == 'windows':
            cmd_str = 'cmd /c ' + cmd_str
        try:
            output = subprocess.check_output(cmd_str, shell=True)
        except subprocess.CalledProcessError as exp:
            output = exp.output
            return_code = exp.returncode
        return output, return_code

    def run_command_async(self, cmd_str):
        """
            Summary:
                异步执行命令行,主进程不阻塞
            Args:
                cmd_str: 命令行字符串
            Returns:
                返回子进程
        """
        p = None
        if self.platform.lower() == 'windows':
            cmd_str = 'cmd /c ' + cmd_str
        try:
            p = subprocess.Popen(cmd_str, shell=True)
        except:
            pass
        finally:
            return p

