## Opalus 大数据分系系统

### 环境要求
- Python 3.6+
- MongoDB 3.0.6


### 环境布署
- 进入当前项目目录
- 创建虚拟环境(只在第一次布署时创建)：/opt/python3/bin/virtualenv env
- 切换到虚拟环境：source env/bin/activate

- 通过/opt/python3/bin/pip3 install -r requirements.txt在该环境下进行安装。

### 启动程序uwsgi:
- source env/bin/activate   #切换当前虚拟环境
- uwsgi --ini ./uwsgi.ini --vhost   #启动uwsgi服务器
- ***快捷启动脚本: sh deploy.sh start|stop|restart

- 关闭虚拟环境：deactivate

