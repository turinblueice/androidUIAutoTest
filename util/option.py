#  -*-coding:utf8-*-

import argparse
from util import switch


def get_args(debug=False):

    if not debug:
        parser = argparse.ArgumentParser(description=u'android商家版自动化case运行命令行工具',
                                         usage='%(prog)s [-m] module [module ...] [-f] function [function ...] '
                                               '[-e] module [module ...] [-E] function [function ...] [-o] [-h] ')

        #  增加命令行参数,增加指定模块级别的case参数
        parser.add_argument('-m', '--module-case', nargs='+', type=str, metavar='module',
                            help=u'指定要运行的case,模块级别')

        #  增加命令行参数,增加指定方法级别的case参数
        parser.add_argument('-f', '--function-case', nargs='+', type=str, metavar='function',
                            help=u'指定要运行的case,方法级别')

        parser.add_argument('-e', '--exclude-module', nargs='+', type=str, metavar='exclude_module',
                            help=u'排除的case,模块级别')

        parser.add_argument('-E', '--exclude-function', nargs='+', type=str, metavar='exclude_function',
                            help=u'排除的case,方法级别')

        # 增加命令行参数,指定环境的参数, -o --on-line献上环境,指定该参数则为线上环境
        parser.add_argument('-o', '--on-line', dest='online',  action='store_true', default=False,
                            help=u'指定是否是QA环境')

        # # 增加html报告支持
        # parser.add_argument('--with-html-report', dest='htmlreport', action='store_true',
        #                     default=False, help=u'输出html报告，报告目录在outputs/report目录下')

        return parser.parse_args()
    return None

args_parser = get_args(switch.switch.debug)

if __name__ == '__main__':
    print args_parser.exclude_function


