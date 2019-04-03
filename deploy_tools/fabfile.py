from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, cd
import random

REPO_URL = 'https://github.com/hj24/superlists.git'

def deploy():
	site_folder = f'/home/{env.user}/sites/{env.host}'
	source_folder = site_folder + '/source'
	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_update_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
	for subfolder in ('database', 'static', 'virtualenv', 'source'):
		run(f'mkdir -p {site_folder}/{subfolder}')

# 从github拉取源码到服务器
def _get_latest_source(source_folder):
	if exists(source_folder + '/.git'):
		with cd(source_folder):
			run(f'git fetch')
			run('git log -n 1')
	else:
		run(f'git clone {REPO_URL} {source_folder}')
	current_commit = local("git log -n 1 --format=%h", capture=True)
	# print(type(current_commit))
	run(f'cd {source_folder} && git reset --hard {current_commit}')
	# with cd(source_folder):
	# 	# git reset --hard命令，切换到指定的提交，此命令会撤销在服务器中对代码仓库做的任何改动
	# 	run(f'git reset --hard {current_commit}')

# 更新配置文件
def _update_settings(source_folder, site_name):
	# site_name 传入一个列表
	setting_path = source_folder + '/superlists/settings.py'
	sed(setting_path, "DEBUG = True", "DEBUG = False")
	sed(setting_path,
		'ALLOWED_HOSTS = .+$',
		f'ALLOWED_HOSTS = ["{site_name}"]'
	)
	secret_key_file = source_folder + '/superlists/secret_key.py'
	if not exists(secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		append(secret_key_file, f'SECRET_KEY = "{key}"')
	append(setting_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	if not exists(virtualenv_folder + '/bin/pip'):
		run(f'python3.6 -m venv {virtualenv_folder}')
	run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder):
	run(
		f'cd {source_folder}'
		' && ../virtualenv/bin/python manage.py collectstatic --noinput'
	)

def _update_database(source_folder):
	run(
		f'cd {source_folder}'
		' && sudo ../virtualenv/bin/python manage.py migrate --noinput'
	)





