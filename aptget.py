from fabric.colors import red, green
from fabric.network import needs_host
from fabric.api import *

@needs_host
def aptget_install_packages(use_sudo=True, non_interactive=False):
    # TODO: instead of using a non interactive mode I should use the debconf-set-selections
    # method, getting the settings from debconf-get-selections available from the debconf-utils
    # package.
    run_or_sudo = sudo if use_sudo else run
    if not non_interactive:
        non_interactive = ''
    else:
        non_interactive = 'DEBIAN_FRONTEND=noninteractive '
    if env.APT_GET_PACKAGES:
        run_or_sudo('apt-get -y update')
        run_or_sudo('%sapt-get -y install %s' %
                    (non_interactive, env.APT_GET_PACKAGES))
    else:
        print red('anv.APT_GET_PACKAGES not set.')
