#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:该模块包含以下功能:启动adb服务,获取设备连接和设备信息

Authors: Turinblueice
Date:    16/4/14 15:11
"""

import re
import sys
import os

from devices_manager import command_prompt
from util import log


class DeviceConfiguration(object):

    """
        Summary:
            -
        Attribute:
            - device_list:设备列表
    """

    def __init__(self, device_list=list()):
        super(DeviceConfiguration, self).__init__()
        self.cmd = command_prompt.CommandPrompt()

        self.adb_dir = ''
        if 'ANDROID_HOME' in os.environ:
            self.adb_dir = os.path.join(os.getenv('ANDROID_HOME'), 'platform-tools') + '/'
        self.start_adb_cmd_str = self.adb_dir+'adb start-server'
        self.stop_adb_cmd_str = self.adb_dir+'adb kill-server'
        self.devices_list = device_list

    def start_adb(self):

        """
            Summary:
                开启adb 服务
            Return:
                True or False
        """
        try:
            output, ret_code = self.cmd.run_command_sync(self.start_adb_cmd_str)
            if ret_code == 0:
                lines = output.split('\n')
                if len(lines) == 1:
                    log.logger.info('adb服务已经开启!')
                elif lines[1].lower() == '* daemon started successfully *':
                    log.logger.info('adb服务开启成功!')
                elif lines[0].find('internal or external command'):
                    log.logger.error('adb环境变量未设置,请先设置adb环境变量!')
                    raise SystemExit()
                else:
                    log.logger.info('未知情况!')
                    raise SystemExit()
            else:
                raise SystemExit()
        except:
            log.logger.error("adb server开启失败!")
            return False
        else:
            return True

    def stop_adb(self):
        """
            Summary:
                停止adb 服务
            Return:
                True or False
        """
        try:
            self.cmd.run_command_sync(self.stop_adb_cmd_str)
        except:
            return False
        else:
            return True

    def get_devices(self):
        """
            Summary:
                获取已连接的所有设备
        """

        adb_server_status = self.start_adb()
        if adb_server_status:
            devices_cmd_str = self.adb_dir+'adb devices'
            output = self.cmd.run_command_sync(devices_cmd_str)[0]
            output = output.strip()
            lines = output.split('\n')

            if len(lines) <= 1:
                log.logger.info('无设备连接')
                self.stop_adb()
                sys.exit(0)

            for line in lines[1:]:
                line = re.sub('\s+', '', line)
                if line.find('device') > -1:  # 包含'device',说明该行包含连接的手机device id
                    device_id = line.replace('device', '')
                    device_brand_cmd_str = self.adb_dir+'adb -s {} shell getprop ro.product.brand'.format(device_id)  # 手机品牌命令行
                    device_model_cmd_str = self.adb_dir+'adb -s {} shell getprop ro.product.model'.format(device_id)  # 手机型号命令行
                    device_os_version_cmd_str = self.adb_dir+'adb -s {} shell getprop ro.build.version.release'.format(
                        device_id)  # 操作系统版本命令行
                    device_brand = self.cmd.run_command_sync(device_brand_cmd_str)[0].strip()
                    device_model = self.cmd.run_command_sync(device_model_cmd_str)[0].strip()
                    device_os_version = self.cmd.run_command_sync(device_os_version_cmd_str)[0].strip()

                    self.devices_list.append(dict(
                        device_id=device_id,
                        device_brand=device_brand,
                        device_model=device_model,
                        device_os_version=device_os_version
                    ))

                    log.logger.info('手机已经连接,该连接的手机信息如下:')
                    log.logger.info('*****************************')
                    log.logger.info('设备ID:' + device_id)
                    log.logger.info('设备品牌:' + device_brand)
                    log.logger.info('设备型号:' + device_model)
                    log.logger.info('系统版本:' + device_os_version)
                    log.logger.info('*****************************')

                elif line.find('unauthorized') > -1:
                    device_id = line.replace('unauthorized', '')
                    log.logger.info('设备未获得授权')
                    log.logger.info('设备ID:' + device_id)

                elif line.find('offline') > -1:
                    device_id = line.replace('offline', '')
                    log.logger.info('设备已离线')
                    log.logger.info('设备ID:' + device_id)
                else:
                    pass

        return self.devices_list

if __name__ == '__main__':
    DeviceConfiguration().get_devices()
