from fabric.api import run
from fabric.context_managers import settings
import os

# 如果推出终端请重新设置环境变量
# 如果在服务器中请在init 脚本中用env设置
SERVER_PASSWORD = os.environ.get('SERVER_PASSWORD')

def _get_manage_dot_py(host):
	return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'

def reset_database(host):
	manage_dot_py = _get_manage_dot_py(host)
	with settings(host_string=f'mamba@{host}:26536', password=SERVER_PASSWORD):
		run(f'{manage_dot_py} flush --noinput')

def create_session_on_server(host, email):
	manage_dot_py = _get_manage_dot_py(host)
	with settings(host_string=f'mamba@{host}:26536', password=SERVER_PASSWORD):
		session_key = run(f'{manage_dot_py} create_session {email}')
		return session_key.strip()