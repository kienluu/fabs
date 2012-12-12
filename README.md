# PORTABLE FABRIC COMMANDS


## INTRODUCTION
-

This is a portable set of fabric commands for automated server deployment of
django projects targeting (or will be) ubuntu based machines with
virtualenvs, supervisord, nginx and sass compass for css preprocessing.

Planned features:
- templated config files for nginx & supervisord


## ENV CONSTANTS TO SET
-

The following is a list of env variables used in this fab library and what
they are.

VIRTUAL_ENV_PATH : Path to virtualenvs folder.
e.g.

```python
env.VIRTUAL_ENV_PATH = /home/user/.virtualenvs
```

PROJECT_PATH : Path to project.
e.g. /home/user/projects/project_name

DJANGO_PROJECT_NAME : Path to django project name.

e.g. /home/user/projects/project_name/django_project_name

MANAGE_PATH : Path to manage.py, default is the default django 1.4 path.

PIP_REQUIREMENT_PATH : path to a list of pip frozen requirements
DYNAMIC_PIP_REQUIREMENT_PATH : path to a list of pip not frozen requirements.
 This would be github based eggs where you may always want the latest version.


## USAGE
-

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


env.roledefs = {
'staging': ['user@project_name.example.com'],
}


@task
def deploy():
    git_pull()
    git_submodule_update()
    update_pip_requirements()
    collectstatic()
    migrate()
    compass_compile()
```