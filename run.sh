#!/bin/bash

# 修改之前确保赋予文件可执行权限

#先运行web/view.py 启动web server，供case选择
python web/view.py&

while [ ! -f 'web/support.txt' ]
do
    sleep 3
    echo "等待3秒，等待用户选择运行的case..."
done

echo "已选择case结果"


pid=$(ps -ef | grep 'python web/view.py' | grep -v 'grep' | awk '{print $2}' | sort -n)

# 关闭web server进程
arr=(${pid})

for each_pid in ${arr[@]}
do
    echo "开始关闭web服务，进程号为${each_pid}"
    kill -s 9 ${each_pid}
done

python clients_main_nose.py
