from fabric.api import env, run, task, cd
from fabric.contrib import files
from fabs.exceptions import RepositoryPathExistError


@task
def git_pull():
    """
    I also need a function to set git up.
    git pull wont work without a default upstream for the branch.
    """
    with cd(env.PROJECT_PATH):
        run('git pull')


@task
def git_submodule_update():
    """
    Updates git submodules.
    The first time the master repository is setup it must run
    git submodule init. Afterwards this will pull down the commit that is
    referenced in the master repository (This value is committed).
    """
    with cd(env.PROJECT_PATH):
        run('git submodule update')


@task
def clone_repository(repo_url, no_submodules=False):
    if files.exists(env.PROJECT_PATH):
        raise RepositoryPathExistError('Path at "%s" already exist' % env.PROJECT_PATH)
    run('mkdir --parents %s' % env.PROJECT_PATH)
    with cd(env.PROJECT_PATH):
        run('git clone "%s" .' % repo_url)
        if not no_submodules:
            run('git submodule init')
            run('git submodule update')