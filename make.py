import os
import tempfile
from urlparse import urlparse
from fabric.api import *
from fabric.contrib import files
from fabs.exceptions import UnknownFormatError

def make(url, download_only=False, out_folder=None, configure_options='',
         configure_arguments='', make_options='', use_sudo=True):
    """
    Download source and make install
    """

    run_or_sudo = sudo if use_sudo else run

    # TODO: find out how to use pythons tempfile.gettempdir() results from the
    # remote machine here.
    TMP_DIR = '/tmp'
    TMP_DIR += '/fabric/make'
    if not files.exists(TMP_DIR):
        # No need to use settings(warn_only=True) here as the mkdir with
        # --parents does not fail
        run('mkdir --parents %s' % TMP_DIR)

    location = urlparse(url)
    source_name = os.path.basename(location.path)
    # Create default out_folder name
    archive_ext = os.path.splitext(source_name)[1].lower()
    if not out_folder:
        out_folder = os.path.splitext(source_name)[0]
        second_split = os.path.splitext(out_folder)
        if second_split[1] == '.tar':
            out_folder = second_split[0]
            archive_ext = '.tar'

    if archive_ext == '.tar':
        unarchiver = simple_untar
    elif archive_ext == '.zip':
        unarchiver = simple_unzip
    else:
        raise UnknownFormatError('Unknown extension: %s' % archive_ext)

    with cd(TMP_DIR):
        # Remove old source_name directory.  -f flag also causes rm to not fail
        run('rm -rf "$(echo %s)"' % out_folder)
        run('wget %s --output-document=%s' % (url, source_name) )
        unarchiver(source_name, out_folder)

        if not download_only:
            with cd(out_folder):
                if configure_arguments and configure_arguments[-1] != ' ':
                    configure_arguments += ' '
                run('%s./configure %s' % (
                    configure_arguments, configure_options))
                run('make %s' % make_options)
                run_or_sudo('make install')


def download_source(url, out_folder=None):
    make(url, out_folder=out_folder, download_only=True)



def simple_untar(path, out_folder=None):
    """
    Will try to auto untar a compressed tar archive to out_folder.

    Since I cannot get tar to untar to a specific folder we will rename the
    the folder instead.
    while
    """
    archive_name = os.path.basename(path)
    name, ext = os.path.splitext(archive_name)
    name2, ext2 = os.path.splitext(name)
    if ext2.lower() == '.tar':
        name = name2
    default_out_folder = name
    if not out_folder or out_folder==default_out_folder:
        run('tar -axf "$(echo %s)"' % path )
    else:
        run('tar -axf "$(echo %s)" && mv "$(echo %s)" "$(echo %s)"' %
            (path, default_out_folder, out_folder))


def simple_unzip(path, out_folder=None):
    """
    Will try to unzip a zip archive to a directory
    """
    if not out_folder:
        archive_name = os.path.basename(path)
        name = os.path.splitext(archive_name)[0]
        out_folder = name
    run('unzip "$(echo %s)" -d "$(echo %s)"' %
        (path, out_folder))