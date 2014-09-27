from os import popen, getcwd, getenv, sep, path, chdir
from sys import exit

from symbols import ESCLAMATION
import colors
from segments import Divider


def print_warning(text):
    divider = Divider()
    cross_rendered = '{}{} {}{}{}{}'.format(
        colors.foreground(colors.WHITE) + colors.background(colors.GOLD),
        ESCLAMATION,
        colors.reset(),
        colors.foreground(colors.GOLD),
        divider.text if divider.active else '',
        colors.reset()
    )

    text_rendered = '{}{}promptastic{}: {}{}'.format(
        colors.foreground(colors.LIGHTER_GOLD),
        colors.underline_start(),
        colors.underline_end(),
        text,
        colors.reset()
    )

    print('{} {}'.format(cross_rendered, text_rendered))


def get_valid_cwd():
    """
    Get the current working dir.
    The current working dir can be not valid: for instance when I delete a parent dir or when I
    git checkout a branch which does not have the current dir. In this case we return the current
    invalid dir (because this is what the OS thinks) but we display a warning.
    """
    try:
        cwd = getcwd()
    except FileNotFoundError:
        cwd = getenv('PWD')  # This is where the OS thinks we are.
        parts = cwd.split(sep)
        up = cwd
        while parts and not path.exists(up):
            parts.pop()
            up = sep.join(parts)
        try:
            chdir(up)
        except Exception:
            print_warning('Your current directory is invalid!')
            exit(1)
        print_warning('Your current directory is invalid!\n'
                      'Closest valid parent directory: {}'.format(up))
    return cwd


def get_terminal_columns_n():
    _, columns = popen('stty size', 'r').read().split()
    return int(columns)