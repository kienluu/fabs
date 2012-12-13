from fabric.api import *


@task
def new_mysql_db(username=None, password=None, db_name=None,
                 mysql_root_user='root'):
    """
    Setup a new mysql database for a typical django project.

    Default username, password and database name is env.DJANGO_PROJECT_NAME.

    Access is via @localhost only.
    """
    if not username:
        username = env.DJANGO_PROJECT_NAME
    if not password:
        password = env.DJANGO_PROJECT_NAME
    if not db_name:
        db_name = env.DJANGO_PROJECT_NAME

    mysql_root_pass = prompt('Please enter the mysql root user password:',
                             default='root')

    run('mysql --user=root --password=%(mysql_root_pass)s --execute=' \
'"CREATE DATABASE %(project_name)s DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci; \\n  ' \
'CREATE USER \'%(project_name)s\'@\'localhost\' IDENTIFIED BY \'%(project_name)s\'; \\n  ' \
'GRANT ALL ON %(project_name)s.* TO \'%(project_name)s\'@\'localhost\'; FLUSH PRIVILEGES;"' \
    % { 'project_name' : env.DJANGO_PROJECT_NAME,
        'mysql_root_pass' : mysql_root_pass })
    

