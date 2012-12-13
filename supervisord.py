from fabric.api import *

@task
def supervisor_restart(use_sudo=True):
    run_or_sudo = sudo if use_sudo else run
    run_or_sudo('supervisorctl update')
    run_or_sudo('supervisorctl restart %s' %env.SUPERVISOR_RESTART_PROCESSES)