from fabric.colors import red, green
from fabric.network import needs_host
from fabric.api import *

@needs_host
def aptget_install_packages(use_sudo=True):
	run_or_sudo = sudo if use_sudo else run
	if env.APT_GET_PACKAGES:
		run_or_sudo('apt-get -y update')
		run_or_sudo('apt-get -y install %s' % env.APT_GET_PACKAGES)
	else:
		print red('anv.APT_GET_PACKAGES not set.')