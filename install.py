#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In order to install promptastic a few lines have to be appended to those files sourced every time
a Bash shell is invoked.
The affected files (as explained at http://mywiki.wooledge.org/DotFiles) are:
~/.profile (Linux) or ~/.bash_profile (Mac OS X) - read every time a Bash shell is invoked,
~/.bashrc - read when a subshell is invoked with a command like `bash`.


The first few lines make sure the rest of the code is compatible with both Python 2 and 3.
"""
from __future__ import print_function
# Python 2 and 3 compatibility: FileNotFoundError in Python 3, IOError in Python 2.
FileNotFoundError = getattr(__builtins__, 'FileNotFoundError', IOError)
input = getattr(__builtins__, 'raw_input', input)

import re
import os
import platform


FUNCTION_CMD = 'function _update_ps1() {{ export PS1="$({}/promptastic.py $?)"; }}'
PROMPT_CMD = 'export PROMPT_COMMAND="_update_ps1; $PROMPT_COMMAND"'


class ConfigFile(object):
    def __init__(self):
        self.is_already_setup = self._is_already_setup()
        self.enabled = True

    @staticmethod
    def _get_cwd(expanded=True):
        if expanded:
            return os.getcwd()
        return os.getcwd().replace(os.path.expanduser('~'), '~')

    def _is_already_setup(self):
        try:
            with open(os.path.expanduser(self.path)) as file:
                content = file.read()
        except FileNotFoundError:
            return False

        # Check for `PROMPT_CMD`:
        regex = r'^[ \t]*{}[ \t;]*$'.format(
            re.escape(PROMPT_CMD))
        match = re.search(regex, content, re.M)
        if not match:
            # So the file does NOT contain `PROMPT_CMD`.
            return False

        # So the file does contain `PROMPT_CMD`.
        # Check for `FUNCTION_CMD`:
        regex = r'^[ \t]*{}|{}[ \t;]*$'.format(
            re.escape(FUNCTION_CMD.format(self._get_cwd(True))),
            re.escape(FUNCTION_CMD.format(self._get_cwd(False))),
        )
        match = re.search(regex, content, re.M)
        if not match:
            # So the file does not contain `FUNCTION_CMD`.
            return False

        # So the file does not contain `FUNCTION_CMD`.
        print('Promptastic already installed in {}'.format(self.path))
        return True

    def install(self):
        print('\nInstalling to {}...'.format(self.path), end=' ')
        with open(os.path.expanduser(self.path), 'a') as file:
            file.write('\n\n' + FUNCTION_CMD.format(self._get_cwd()) + '\n')
            file.write(PROMPT_CMD + '\n')
        print('done')


class BashProfile(ConfigFile):
    path = '~/.bash_profile'

    def __init__(self):
        super(BashProfile, self).__init__()
        # This file need to edited exclusively for Mac OS X machines.
        if not 'darwin' in platform.system().lower():
            self.enabled = False


class BashRc(ConfigFile):
    path = '~/.bashrc'


if __name__ == '__main__':
    print('\nPromptastic setup\n=================')
    print('\nChecking if promptastic is already installed in the system...')

    bash_profile = BashProfile()
    bash_rc = BashRc()

    to_be_installed = [x for x in (bash_profile, bash_rc) if not x.is_already_setup and x.enabled]

    if to_be_installed:
        text = ' and '.join([x.path for x in to_be_installed])
        print('\nWe are about to install promptastic in {}'.format(text))
        a = input('Are you sure you want to continue [y/N]? ')

        if a == 'y':
            for x in to_be_installed:
                x.install()

    print('\nSetup complete!\n')
    exit(0)
