from fabric.api import env, run, task, cd

@task
def compass_compile():
    with cd(env.PROJECT_PATH):
        run('compass compile')
