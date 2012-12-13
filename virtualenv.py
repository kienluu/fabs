from contextlib import contextmanager
from fabric.colors import red
from fabric.contrib import files
from fabric.network import needs_host
from fabric.api import *
from fabs.exceptions import VirtualEnvExistError


APT_GET_DEFAULT_VIRTUALWRAPPER_SETUP_PATH = \
    '/etc/bash_completion.d/virtualenvwrapper'


@contextmanager
def virtualenv():
    """
    allows:
    with virtualenv():
        run('which pip')
    """
    with prefix('source %s/bin/activate' % env.VIRTUAL_ENV_PATH):
        yield


@contextmanager
def aptget_virtualenvwrapper():
    """
    Source the default apt-get install path to virtualenv wrapper setup script
    """
    with prefix('source %s' % APT_GET_DEFAULT_VIRTUALWRAPPER_SETUP_PATH):
        yield


def has_aptget_virtualwrapper():
    return files.exists(APT_GET_DEFAULT_VIRTUALWRAPPER_SETUP_PATH)



@needs_host
def make_virtualenv(virtualenv_name=None):
    """
    Will make a virtualenv with the name virtualenv_name or
    env.DJANGO_PROJECT_NAME.

    It will make this with the virtualenv wrapper mkvirtualenv function.

    The easiest way to setup virtualenvwrapper is to just install it with
    apt-get install virtualenvwrapper.

    Otherwise you will just need to source the relevant files & and setup the
    correct env variables yourself in your rc file.
    """
    def _make_virtualenv():
        run('mkvirtualenv --no-site-packages %s' % virtualenv_name)
        with virtualenv():
            #FIXME: Why do I always have to update easy_install -U distribute now?
            run('easy_install -U distribute')

    def _error_on_virtualenv_exist():
        exists = run('test -e $VIRTUALENVWRAPPER_HOOK_DIR/%s'\
            % env.DJANGO_PROJECT_NAME).succeeded
        if not exists:
            return
        raise VirtualEnvExistError('Virtualenv %s already exist' %
                                   env.DJANGO_PROJECT_NAME)

    if not virtualenv_name:
        virtualenv_name = env.DJANGO_PROJECT_NAME
    if has_aptget_virtualwrapper():
        with aptget_virtualenvwrapper():
            _error_on_virtualenv_exist()
            _make_virtualenv()
    else:
        _error_on_virtualenv_exist()
        _make_virtualenv()


