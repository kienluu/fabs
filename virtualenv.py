from contextlib import contextmanager
from fabric.context_managers import cd, prefix
from fabric.state import env


@contextmanager
def virtualenv():
    """
    allows:
    with virtualenv():
        run('which pip')
    """
    with prefix('source %s/bin/activate' % env.VIRTUAL_ENV_PATH):
        yield