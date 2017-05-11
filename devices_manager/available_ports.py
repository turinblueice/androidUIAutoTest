#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 获取空闲状态的端口
 
Authors: Turinblueice
Date:    16/4/14 11:05
"""
import socket


class AvailablePorts(object):

    def __init__(self):
        super(AvailablePorts, self).__init__()

    @staticmethod
    def get_port():
        """
            Summary:
                - 获取空闲的port, 通过UDP的方式获取socket套接字之后,获取该socket的端口,关闭socket.

        """
        socket_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket.SOCK_STREAM为TCP协议
        socket_temp.bind(("127.0.0.1", 0))
        # 若使用TCP协议获取套接字,则需要进行监听连接数的设置
        # socket_temp.listen(1)
        port = socket_temp.getsockname()[1]
        socket_temp.close()
        return port

    @staticmethod
    def get_local_ip():
        """
            Summary:
                获取本机IP
        """
        return socket.gethostbyname(socket.gethostname())

