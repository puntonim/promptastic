#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
In order to install promptastic a few lines have to be appended to those files sourced every time
a Bash shell is invoked.
The affected files (as explained at http://mywiki.wooledge.org/DotFiles) are:
~/.bash_profile - read every time a Bash shell is invoked,
~/.bashrc - read when a subshell is invoked with a command like `bash`.
"""
import re
import os


FUNCTION_CMD = 'function _update_ps1() {{ export PS1="$({}/promptastic.py $?)"; }}'
PROMPT_CMD = 'export PROMPT_COMMAND="_update_ps1"'


class ConfigFile:
    def __init__(self):
        self.is_already_setup = self._is_already_setup()

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
        match = re.search(r'^[ \t]*{}[ \t;]*$'.format(PROMPT_CMD), content, re.M)
        if not match:
            # So the file does not contain `PROMPT_CMD`.
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


class BashRc(ConfigFile):
    path = '~/.bashrc'


if __name__ == '__main__':
    print('\nPromptastic setup\n=================')
    print('\nChecking if promptastic is already installed in the system...')

    bash_profile = BashProfile()
    bash_rc = BashRc()

    to_be_installed = [x for x in (bash_profile, bash_rc) if not x.is_already_setup]

    if to_be_installed:
        text = ' and '.join([x.path for x in to_be_installed])
        print('\nWe are about to install promptastic in {}'.format(text))
        a = input('Are you sure you want to continue [y/N]? ')

        if a == 'y':
            for x in to_be_installed:
                x.install()

    print('\nSetup complete!\n')
    exit(0)