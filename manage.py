#!env/bin/python
import os
from app import create_app
from flask_script import Manager, Server

app = create_app(os.getenv('FLASK_ENV') or 'development')
manager = Manager(app)
manager.add_command("runserver", Server(host="127.0.0.1", port=8002, use_debugger=True))

if __name__ == '__main__':
    manager.run()
