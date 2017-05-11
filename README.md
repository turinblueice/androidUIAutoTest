# 使用说明

## 1. 直接运行
> 1) 可使用 python main.py -h 获取帮助；

> 2) 执行所有case:  python main.py;

> 3) 执行指定模块case: python main.py -m test_discover_operation

> 4) 执行多个模块case: python main.py -m test_discover_operation test_paster_operation

> 5) 执行某个模块的指定方法case: python main.py -m test_discover_operation -f test_search_operation  test_discover_skip_operation

> 6) 执行排除某些模块的case:  python main.py -e test_discover_operation  test_paster_operation

> 7) 执行排除某模块中某些方法的case:　python main.py -m test_discover_operation -E test_search_operation  test_discover_skip_operation　


## 2. 获取case执行成功率

如果想要执行case的同时获取case执行成功率，则用client_main_nose.py来代替clients_main.py

>  1) python nose_main.py -m test_discover_operation

该命令运行完后会在同级目录上生成名为nosetests_0.xml的case执行结果文件，该文件为通用的xunit规则xml文件


## 3. 远程触发

在linux环境运行命令
>  1) ./run.sh

开启flask服务，访问http://{your_service_ip}:5000 , 勾选想要执行的case，点击提交即可。




