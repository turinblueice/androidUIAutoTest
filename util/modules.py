#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 模块级测试用例导入和解析模块,获取测试套件、nose测试路径等功能的模块

Authors: Turinblueice
Date:    16/3/23 16:18
"""
import os
import re
import sys
import unittest

from util import log


class ModulesParser(object):
    """
        Summary:
            测试模块导入解析类
        Attribute:
            module_dir:测试模块目录
    """

    def __init__(self, module_dir):
        self.__module_dir = module_dir

    def get_test_module_names(self):
        """
            Summary:
                获取测试用例的模块名称列表
        """
        module_files = os.listdir(self.__module_dir)
        regex = re.compile("^test_.*\.py$", re.IGNORECASE)
        test_modules_files = filter(regex.search, module_files)
        to_module_name = lambda filename: os.path.splitext(filename)[0]
        test_modules = map(to_module_name, test_modules_files)
        return test_modules

    @staticmethod
    def get_test_modules(module_names):
        """
            Symmary:
                获取导入的测试模块
        """
        return map(__import__, module_names)

    def get_test_suite(self, arg_parser, test_module_dir=None):
        """
            Summary:
                获取测试集
            Args:
                arg_parser:参数解析对象
                test_module_dir:测试模块所在目录
        """
        test_module_list = arg_parser.module_case
        test_ignore_module_list = arg_parser.exclude_module

        test_module_dir = test_module_dir or self.__module_dir
        test_module_list = self.filter_test_modules(test_module_list, test_ignore_module_list, test_module_dir)

        if len(test_module_list) == 0:
            log.logger.error("有效的测试模块数量为0,程序退出")
            raise SystemExit()

        if len(test_module_list) == 1:
            test_ignore_function_list = arg_parser.exclude_function or list()
            test_module = test_module_list[0]
            #  筛选出测试类
            test_class = self.filter_test_class(test_module)

            if arg_parser.function_case:  # 命令行指定的测试模块数量等于1且已指定测试方法时,才考虑指定的方法级测试用例
                test_function_list = arg_parser.function_case

                #  筛选存在于测试类中的测试方法
                test_function_list = self.filter_test_functions(test_class, test_function_list,
                                                                test_ignore_function_list)
            else:  # 未指定具体的测试方法,则从所有方法中筛选
                test_function_list = self.filter_test_functions(test_class, None, test_ignore_function_list)
            curr_suites = map(test_class, test_function_list) if test_function_list else None
        else:
            curr_suites = map(unittest.defaultTestLoader.loadTestsFromModule, test_module_list)

        ret_suite = unittest.TestSuite(curr_suites) if curr_suites else None
        return ret_suite

    def filter_test_modules(self, src_modules=None, ignore_modules=None, test_module_dir=None):
        """
            Summary:
                筛选有效的模块级测试用例
            Args:
                src_modules:待筛选的源模块列表
                ignore_modules:排除的模块列表
                test_module_dir:已有的测试模块目录
            Returns:
                dest_modules:筛选后的模块列表,成员类型为模块类型,非入参时的字符串类型
        """
        available_module_names = self.get_test_module_names()
        module_dir = test_module_dir or self.__module_dir
        sys.path.append(module_dir)  # 将要导入的模块目录添加到PYTHONPATH中

        #  假如src_modules为None,则模块为指定目录下的所有模块
        dest_modules = available_module_names if src_modules is None else \
            filter(lambda module: module in available_module_names, src_modules)

        # 排除ignore_modules列表中的模块
        dest_modules = dest_modules if ignore_modules is None else \
            filter(lambda module: module not in ignore_modules, dest_modules)

        dest_modules = self.get_test_modules(dest_modules)

        return dest_modules

    @staticmethod
    def filter_test_class(module):
        """
            Summary:
                从指定模块中筛选出测试类
            Args:
                module:指定的模块
        """
        test_class_list = filter(lambda attr: len(attr) > 8 and attr[-8:] == 'TestCase', dir(module))
        test_class = module.__getattribute__(test_class_list[0])
        return test_class

    @staticmethod
    def filter_test_functions(test_class, src_functions=None, ignore_test_functions=None):
        """
            Summary:
                筛选指定测试类中的测试方法
            Args:
                test_class:指定的测试类
                src_functions:源测试方法列表
                ignore_test_functions:排除的不执行的测试方法
        """
        ignore_test_functions = ignore_test_functions or list()

        if src_functions is None:
            src_functions = filter(lambda function_name: function_name.startswith('test_'), dir(test_class))

        dest_functions = filter(lambda function_name:
                                function_name in dir(test_class) and function_name not in ignore_test_functions,
                                src_functions)
        return dest_functions

    @staticmethod
    def get_function_doc(test_class, function_name):
        """
            Summary:
                获取方法的说明文档
        """
        if function_name in dir(test_class):
            return unicode(test_class.__dict__[function_name].__doc__, 'utf8')
        return None

    def get_test_support(self, modules_dir=None, test_module=None, test_method=None):
        """
            Summary:
                过滤得到测试集
                /{test_cases_dir}/{test_case.py}:Test_class.test_method
                /{test_cases_dir}/{test_case.py}:test_method
        """
        modules_dir = modules_dir or self.__module_dir
        if not os.path.isdir(modules_dir):
            log.logger.error("测试模块目录不存在")
            return None

        # 测试模块如果为None,则直接返回指定目录为测试集
        modules_abs_dir = os.path.abspath(modules_dir)
        if test_module is None:
            return modules_abs_dir

        test_module_list = self.get_test_module_names()

        test_modules = map(
            lambda module_file: os.path.split(module_file)[1].split(os.path.extsep)[0], test_module_list)
        if test_module not in test_modules:
            log.logger.error("测试模块不在指定的目录中")
            return None

        sys.path.append(modules_abs_dir)
        module = __import__(test_module)

        test_class_list = filter(lambda attr: len(attr) > 8 and attr[-8:] == 'TestCase', dir(module))
        test_class = test_class_list[0]
        support = os.path.join(modules_dir, test_module) + '.py:' + test_class

        if test_method is None:
            return support

        test_class = getattr(module, test_class)
        if test_method not in dir(test_class):
            log.logger.error("测试方法不在指定的测试类中")
            return None

        support = support + '.' + test_method

        return support

    def get_test_supports_by_args(self, arg_parser, modules_dir=None):

        """
            Summary:
                根据命令行参数获取测试集
        """
        modules_dir = modules_dir or self.__module_dir
        modules_dir = os.path.abspath(modules_dir)

        test_module_list = arg_parser.module_case

        test_ignore_module_list = arg_parser.exclude_module or list()
        test_ignore_function_list = arg_parser.exclude_function or list()

        test_supports = list()

        if test_module_list is None:
            if not test_ignore_module_list:
                #  若arg_paresr.module_case为None,即命令行参数中-m参数缺失,且没有忽略的模块列表,则默认返回指定目录下的所有测试模块
                support = self.get_test_support(modules_dir, None)
                if support:
                    test_supports.append(support)
            else:
                test_module_list = self.get_test_module_names()
                test_module_list = map(
                    lambda module_file: os.path.split(module_file)[1].split(os.path.extsep)[0],
                    test_module_list)
                test_module_list = filter(lambda module_name: module_name not in test_ignore_module_list,
                                          test_module_list)
                for test_module in test_module_list:
                    support = self.get_test_support(modules_dir, test_module)
                    if support:
                        test_supports.append(support)

        elif len(test_module_list) == 1:

            test_function_list = arg_parser.function_case
            if test_function_list is None:

                if not test_ignore_function_list:
                    #  如果命令行参数指定-m, 参数为1但没有指定-f参数,且没有忽略的方法, 则运行该模块下所有方法级的case
                    support = self.get_test_support(modules_dir, test_module_list[0], None)
                    if support:
                        test_supports.append(support)
                else:
                    if modules_dir not in sys.path:
                        sys.path.append(modules_dir)

                    test_module = __import__(test_module_list[0])
                    test_class = self.filter_test_class(test_module)

                    test_function_list = filter(
                        lambda function_name:
                        function_name not in test_ignore_function_list and function_name.startswith('test_'),
                        dir(test_class))
                    for function_case in test_function_list:
                        support = self.get_test_support(modules_dir, test_module_list[0], function_case)
                        if support:
                            test_supports.append(support)
            else:
                test_function_list = filter(lambda function_name: function_name not in test_ignore_function_list,
                                            test_function_list)
                for function_case in test_function_list:
                    support = self.get_test_support(modules_dir, test_module_list[0], function_case)
                    if support:
                        test_supports.append(support)

        else:
            test_module_list = filter(lambda module_name: module_name not in test_ignore_module_list, test_module_list)

            for test_module in test_module_list:
                #  如果命令行参数中指定了多个模块,则运行多个模块
                support = self.get_test_support(modules_dir, test_module)
                if support:
                    test_supports.append(support)

        return test_supports


if __name__ == '__main__':

    mp = ModulesParser('test_cases')
    from base import option
    argparser = option.args_parser
    supports = mp.get_test_supports_by_args(argparser)
    for test_support in supports:
        print test_support

    # suites = mp.get_test_suite(argparser)
    # for suite in suites:
    #     print suite
