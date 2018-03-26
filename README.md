## Opalus 大数据分系系统

### 环境要求
- Python 3.6+
- MongoDB 3.0.6+
- Redis 4.0+


### 环境布署
- 进入当前项目目录  
- 创建虚拟环境(只在第一次布署时创建)：```/opt/python3/bin/virtualenv env```  
- 切换到虚拟环境：```source env/bin/activate```  
- 安装依赖: ```/opt/python3/bin/pip3 install -r requirements.txt```   


### 开发环境启动
- 切换当前虚拟环境: ```source env/bin/activate``` 
- 启动程序: ``` python manage.py run ```  
- 浏览地址：``` http://localhost:8002 ```  
- 启动控制台：``` python manage.py shell ```  

### 启动程序uwsgi:
- 切换当前虚拟环境: ```source env/bin/activate```  
- 启动uwsgi服务器: ```uwsgi --ini ./uwsgi.ini --vhost```  
- 快捷启动脚本: ```sh deploy.sh start|stop|restart```  

### 启动任务队列
```
celery worker -A celery_runner --loglevel=info
```

### 退出当前虚拟环境
```
deactivate
``` 

