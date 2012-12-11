from fabric.api import env, run, task, cd

@task
def git_pull():
    with cd(env.PROJECT_PATH):
        run('git pull')
