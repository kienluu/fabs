

# ENV CONSTANTS TO SET
---
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

PIP_REQUIREMENT_PATH : path to the pip-requirement.txt file
PIP_DYNAMIC_EGGS : list of name of pip-requirement eggs that will always pull the latest commit

e.g. env.PIP_EGGS = ['']

