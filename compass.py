from fabric.api import env, run, task, cd

@task
def compass_compile(DEV_ENV=False):
    with cd(env.PROJECT_PATH):
        if DEV_ENV:
            run('compass compile --force')
        else:
            run('compass compile --force -e production')
