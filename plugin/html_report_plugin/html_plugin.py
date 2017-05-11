#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: html模式输出测试报告的插件

Authors: Turinblueice
Date:    16/3/23 16:18
"""


import traceback
import sys
import os
import datetime
import shutil
import xml.etree.ElementTree as ET


class HtmlOutput(object):
    """
        Summary:
            没有样式装饰的html代码
    """

    def __init__(self, report_file=None):
        """

        Args:
            report_file: 报告文件保存的路径, 用户自定义目录
        """
        super(HtmlOutput, self).__init__()

        #  默认报告所在目录
        default_report_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../outputs/report'))

        if not os.path.isdir(default_report_dir):
            os.makedirs(default_report_dir)

        src_static_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'static')
        )
        dest_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../outputs/report/static')
        )

        if not os.path.isdir(dest_dir):
            shutil.copytree(src_static_dir, dest_dir)
        # # 默认报告路径
        # self.__default_report_path = default_report_dir+'/index.html'
        # # 报告一式两份, 用户给定一份,路径report_file, 可选; 本地保存一份, 默认路径为 default_report_path
        self.__report_file = report_file

        self.__case_count = 0
        self.__error_count = 0
        self.__failure_count = 0

        self.__html = ['<html><head>',
                       '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />',
                       '<link rel="stylesheet" type="text/css" href="../static/style/report.css" />',
                       '<title>测试报告</title>',
                       '</head>',
                       '<body><div id="table"></div></body>',
                       '</html>']

        # # 报告文件生成完毕后,开始加载报告文件的dom tree
        # self.__tree = ET.parse(self.__report_file)
        # self.__root = self.__tree.getroot()

        #  直接将html string装在入dom内存, 不用先生成文件再从文件中载入
        self.__root = ET.fromstring(''.join(self.__html))
        self.__tree = ET.ElementTree(self.__root)
        self.__body = self.__root.find('body')
        self.__table = self.__root.find('.//div[@id="table"]')

    def add_success(self, test_name):
        self.__case_count += 1
        row_elem = ET.SubElement(self.__table, 'div', attrib={'class': 'row'})
        cell_elem_1 = ET.SubElement(row_elem, 'div', attrib={'class': 'table-cell'})
        cell_elem_1.text = test_name.decode('utf8') if not isinstance(test_name, unicode) else test_name
        cell_elem_2 = ET.SubElement(row_elem, 'div', attrib={'class': 'table-cell pass'})
        cell_elem_2.text = 'Pass'

    def add_failure(self, test_name):
        self.__case_count += 1
        self.__failure_count += 1
        row_elem = ET.SubElement(self.__table, 'div', attrib={'class': 'row'})
        cell_elem_1 = ET.SubElement(row_elem, 'div', attrib={'class': 'table-cell'})
        cell_elem_1.text = test_name.decode('utf8') if not isinstance(test_name, unicode) else test_name
        cell_elem_2 = ET.SubElement(row_elem, 'div', attrib={'class': 'table-cell failure'})
        cell_elem_2.text = 'Fail'

    def add_error(self, test_name, error):
        self.__case_count += 1
        self.__error_count += 1
        row_elem = ET.SubElement(self.__table, 'div', attrib={'class': 'row'})
        cell_elem_1 = ET.SubElement(row_elem, 'div', attrib={'class': 'table-cell'})
        cell_elem_1.text = test_name.decode('utf8') if not isinstance(test_name, unicode) else test_name
        cell_elem_2 = ET.SubElement(row_elem, 'div', attrib={'class': 'table-cell error'})
        cell_elem_2.text = error.decode('utf8') if not isinstance(error, unicode) else error

    def finalize(self):

        elem = self.__root.find('.//*[@id="bottom"]')
        fail_elem = self.__root.find('.//*[@id="bottom-fail"]')
        if elem is None:

            row_elem = ET.SubElement(self.__body, 'div', attrib={'class': 'table-bottom', 'id': 'bottom'})
            row_elem.text = "Ran {} test{}".format(self.__case_count, self.__case_count != 1 and "s" or "")

            row_elem = ET.SubElement(self.__body, 'div', attrib={'class': 'table-bottom', 'id': 'bottom-fail'})
            row_elem.text = 'FAILED ( failures={} errors={} )'.format(self.__failure_count, self.__error_count)

        else:
            elem.text = "Ran {} test{}".format(self.__case_count, self.__case_count != 1 and "s" or "")
            fail_elem.text = 'FAILED ( failures={} errors={} )'.format(self.__failure_count, self.__error_count)

        if self.__report_file:
            self.__tree.write(self.__report_file, encoding='utf8')
        # self.__tree.write(self.__default_report_path, encoding='utf8')

    def dump_html(self):

        ET.dump(self.__tree)


def get_html_report_path(device=None):
    """
        Summary:
            获取html报告路径
    Returns:

    """
    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d%H%M%S")
    device_str = device or ''
    report_postfix = now_str + '_' + device_str

    today_str = now.strftime("%Y%m%d")
    dir_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../outputs/report/'+today_str)
    )

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    html_report_path = os.path.join(dir_path, 'report_'+report_postfix+'.html')
    return html_report_path

#HTMLget_current_html_reporter = HtmlOutput(report_file=_get_html_report_path())

if __name__ == '__main__':

    #path = '../../outputs/report/20161013/report_20161013154417'

    htmlrunner = HtmlOutput()
    htmlrunner.add_success('他人IN记点击头像')
    htmlrunner.add_success('加载')
    htmlrunner.add_success('加载xx')
    htmlrunner.add_failure('QQ登录失败')
    htmlrunner.add_error('他人IN记多页加载', '没有执行')
    htmlrunner.finalize()
    htmlrunner.finalize()
    htmlrunner.dump_html()
