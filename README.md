## Opalus 大数据分系系统

### 环境要求
- Python 3.6+
- MongoDB 3.0.6


### 环境布署
- 进入当前项目目录
- 创建虚拟环境：/opt/python3/bin/virtualenv env
- 切换到虚拟环境：source /opt/project/python/test/venv/bin/activate
- 关闭虚拟环境：deactivate

- 通过pip install -r requirements.txt在该环境下进行安装。


### 启动程序uwsgi:
- source env/bin/activate   #切换当前虚拟环境
- uwsgi uwsgi.ini   #启动uwsgi服务器
- ***快捷启动: sh deploy.sh start|stop|restart

