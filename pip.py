from fabric.colors import red, green, blue
from fabric.operations import *
import re
import os
from fabric.api import env, run, task, cd, puts
from fabric.contrib import files
from fabs.virtualenv import virtualenv


env.PIP_REQUIREMENT_PATH = None
env.PIP_DYNAMIC_REQUIREMENT_PATH = None


@task
def update_frozen_pip_requirements():
    """
    This is actually going to use
    """
    if not env.PIP_REQUIREMENT_PATH:
        print 'env.PIP_REQUIREMENT_PATH not set.'
        return
    if not files.exists(env.PIP_REQUIREMENT_PATH):
        print 'File at env.PIP_REQUIREMENT_PATH(%s) does not exist.' \
                % env.PIP_REQUIREMENT_PATH
        return
    with virtualenv():
        out = run('pip freeze')
        pip_file_out = run('cat %s' % env.PIP_REQUIREMENT_PATH).stdout
        if out == pip_file_out:
            print 'pip requirements are upto date.'
            return

        run('pip install -r %s' % env.PIP_REQUIREMENT_PATH)


@task
def update_dynamic_pip_requirements():
    if not env.PIP_DYNAMIC_REQUIREMENT_PATH:
        print 'File at env.DYNAMIC_PIP_REQUIREMENT_PATH(%s) does not exist.'\
              % env.PIP_DYNAMIC_REQUIREMENT_PATH
        return
    if not files.exists(env.PIP_DYNAMIC_REQUIREMENT_PATH):
        print 'File at env.DYNAMIC_PIP_REQUIREMENT_PATH(%s) does not exist.' \
                % env.PIP_DYNAMIC_REQUIREMENT_PATH
        return
    with virtualenv():
        run('pip install -r %s' % env.PIP_DYNAMIC_REQUIREMENT_PATH)


@task
def update_pip_requirements():
    update_frozen_pip_requirements()
    update_dynamic_pip_requirements()



# TODO: This function will only remove dynamic eggs that are using the
# -e option.  Support is for external github modules.
@task
def create_freeze_requirements():
    """
    Will run a pip freeze, then if set will remove the dynamic requirements
    in the env.PIP_DYNAMIC_REQUIREMENT_PATH file and output the files to
    env.PIP_REQUIREMENT_PATH.
    """
    if env.PIP_DYNAMIC_REQUIREMENT_PATH:
        dynamic_reqs = run('cat %s' % env.PIP_DYNAMIC_REQUIREMENT_PATH)
        dynamic_egg_list = _get_eggs(dynamic_reqs)
        with virtualenv():
            freeze_output = run('pip freeze').stdout
        # Results from run include a '\r\n' in them.  Regex does not treat \r\n as
        # a newline.  So we must remove this.
        freeze_output = re.sub(r'\r\n','\n',freeze_output)
        for egg_name in dynamic_egg_list:
            # Python 2.6 re.sub command does not take flags so compile the pattern.
            # Also, I'm not sure why the DOTALL flag is needed here.
            pattern = re.compile(r'^.+?#egg=%s$' % egg_name, flags=re.MULTILINE)
            freeze_output = pattern.sub('', freeze_output)
        # Remove empty lines
        freeze_output = '\n'.join([line for line in freeze_output.split('\n')
                 if line.strip()])
        print green('\n New frozen requirements file:\n')
        print red(freeze_output)
    else:
        with virtualenv():
            freeze_output = run('pip freeze').stdout

    # Backup old file
    if files.exists(env.PIP_REQUIREMENT_PATH):
        run('mv %s %s' % (env.PIP_REQUIREMENT_PATH,
            os.path.splitext(env.PIP_REQUIREMENT_PATH)[0] + '.bak'))
    run("echo '%s' > %s" % (freeze_output, env.PIP_REQUIREMENT_PATH))


def _get_eggs(dynamic_reqs):
    """
    Takes a dynamic pip requirements file content and return a list
    of egg names.
    """
    eggs = []
    for line in dynamic_reqs.split('\n'):
        if len(line) < 2:
            continue
        match = re.match(r'^.+#egg=(?P<egg>.+)$', line)
        if not match:
            continue
        eggs.append(match.groupdict()['egg'])
    print eggs, dynamic_reqs
    return eggs