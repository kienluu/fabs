# PORTABLE FABRIC COMMANDS


## INTRODUCTION
---

This is a portable set of fabric commands for writing scripts to automate server
deployment of django projects targeting ubuntu based machines with
virtualenvs, supervisord, nginx and sass compass for css preprocessing.

Features:
- typical apt-get compass, django git make pip and virtualenv commands.
- pip requirement files with a frozen requirements list and a non frozen always
updated list
- helpers for server setup scripts, such as source compilation helpers.

Planned features:
- templated config files for nginx & supervisord & django


## ENV CONSTANTS TO SET
---

The following is a list of env variables used in this fab library and what
they are.

VIRTUAL_ENV_PATH : Path to virtualenvs folder.
e.g. env.VIRTUAL_ENV_PATH = /home/user/.virtualenvs

PROJECT_PATH : Path to project.
e.g. /home/user/projects/project_name

DJANGO_PROJECT_NAME : Path to django project name.

e.g. /home/user/projects/project_name/django_project_name

MANAGE_PATH : Path to manage.py, default is the default django 1.4 path.

PIP_REQUIREMENT_PATH : path to a list of pip frozen requirements
DYNAMIC_PIP_REQUIREMENT_PATH : path to a list of pip not frozen requirements.
 This would be github based eggs where you may always want the latest version.

APT_GET_PACKAGES : apt-get packages to install.  It would be good to list them
all here for future installs so they can be used in part of a install script.
e.g. env.APT_GET_PACKAGES = 'python2.7-dev mysql-server zip '


## USAGE
---

git clone or use (git submodule) this repository with a desired module name.
e.g. fabulous

```
git clone git@github.com:kienluu/fabs.git fabulous
```

Then here is an example fabric.py file:

```python
from fabric.api import *
from fabric.contrib import django as fabric_django
from fabulous import *


DJANGO_PROJECT_NAME = 'procor'
fabric_django.project(DJANGO_PROJECT_NAME)
from django.conf import settings as django_settings


env.django_settings = django_settings
env.PROJECT_PATH = '/home/mohu/projects/project_name'
env.DJANGO_PROJECT_NAME = DJANGO_PROJECT_NAME
env.SUPERVISOR_RESTART_PROCESSES = 'nginx gunicorn'
env.VIRTUAL_ENV_PATH = '/home/mohu/.virtualenvs/project_name'
env.PIP_REQUIREMENT_PATH = env.PROJECT_PATH + \
                           '/configuration/pip-frozen-requirements.txt'
env.PIP_DYNAMIC_REQUIREMENT_PATH = env.PROJECT_PATH + \
                           '/configuration/pip-dynamic-requirements.txt'
env.APT_GET_PACKAGES = \
	'build-essential curl git-core libfreetype6 ' \
	'libfreetype6-dev libjpeg62 libjpeg62-dev libmysql++-dev ' \
	'libmysqlclient15-dev libpcre3-dev libssl-dev libtool libxml2 ' \
	'libxml2-dev libxslt-dev linux-kernel-headers lsof mysql-server ' \
	'python-dev python-imaging python-pip python-setuptools ' \
	'python-software-properties python-virtualenv virtualenvwrapper ' \
	'python2.7-dev ' \
	'supervisor unzip uuid-dev wget xvfb zip ' \
	'zlib1g-dev memcached '


env.roledefs = {
'staging': ['user@project_name.example.com'],
'test_box': ['mohu@192.168.160.132'],
}


# Deploy script to update server.
@task
def deploy():
    git_pull()
    git_submodule_update()
    update_pip_requirements()
    collectstatic()
    migrate()
    compass_compile()


# Install nginx script
@task
def install_nginx():
    download_source(
    "http://www.grid.net.ru/nginx/download/nginx_upload_module-2.0.12.tar.gz")
    make("http://nginx.org/download/nginx-1.2.6.tar.gz",
         configure_options='--with-http_ssl_module --add-module=' \
                           '../nginx_upload_module-2.0.12')
    sudo('ln -s /usr/local/nginx/sbin/nginx /usr/local/bin/nginx')


# The server will need openssh-server installed at least.
@task
def setup_server():
    # Turn off mysql password prompts (before careful of other prompts) and
    # then prompt user manually with
    # sudo dpkg-reconfigure mysql-server-5.5
    aptget_install_packages(True)
    sudo('dpkg-reconfigure mysql-server-5.5')
    install_nginx()
    try:
        clone_repository('git@github.com:mohu/procor_corp.git')
    except RepositoryPathExistError, e:
        print red('Repository path already exist.')
    try:
        make_virtualenv()
    except VirtualEnvExistError, e:
        print red('Virtualenv already exist.')

```
