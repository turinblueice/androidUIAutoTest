#  -*-coding:utf8-*-

import sys
import flask
import os


parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_path not in sys.path:
    sys.path.append(parent_path)

from util import modules

app = flask.Flask(__name__)

module_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '../test_cases'
    )
)

support_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'supports.txt')
)


@app.route('/')
def index():
    """
        Summary:
            选择页面展示页，主页
    """
    if os.path.isfile(support_path):
        #  case集结果文件存在，则说明上一次结果还未收集，等待收集执行后才允许访问case集选择页
        return '正在上一次持续集成中，请稍后'

    md_parser = modules.ModulesParser(module_dir)
    ret_modules = md_parser.filter_test_modules()

    case_dic = dict()
    for each_module in ret_modules:
        clazz = md_parser.filter_test_class(each_module)
        functions = md_parser.filter_test_functions(clazz)
        functions = [func+'.('+md_parser.get_function_doc(clazz, func)+')' for func in functions]
        case_dic[each_module.__name__+'.'+clazz.__name__] = functions

    return flask.render_template('case_select.html', cases=case_dic)


@app.route('/submit/', methods=['GET', 'POST'])
def submit_handle():
    """
        Summary:
            处理内容
    """

    if flask.request.method == 'POST':
        md_parser = modules.ModulesParser(module_dir)
        full_case_names = flask.request.form.getlist('case')
        with open(support_path, 'w') as f:
            for _index, full_case_name in enumerate(full_case_names):
                tmp_names = full_case_name.split('.')
                module_name = tmp_names[0]
                function_name = tmp_names[2]
                support = md_parser.get_test_support(test_module=module_name, test_method=function_name)
                f.write(support)
                if _index < len(full_case_names)-1:
                    f.write('\n')

    return '已经提交完毕，等待执行结束'


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
