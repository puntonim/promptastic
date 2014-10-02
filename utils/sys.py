import os
import sys

from utils.glyphs import ESCLAMATION
from segments.basics import Divider
from utils import colors


def print_warning(text):
    divider = Divider()
    cross_rendered = '{}{} {}{}{}{}'.format(
        colors.background(colors.GOLD),
        ESCLAMATION,
        colors.reset(),
        colors.foreground(colors.GOLD),
        divider.text if divider.active else '',
        colors.reset()
    )

    text_rendered = '{}{}promptastic{}: {}{}\n'.format(
        colors.foreground(colors.LIGHTER_GOLD),
        colors.underline_start(),
        colors.underline_end(),
        text,
        colors.reset()
    )

    output = '{} {}'.format(cross_rendered, text_rendered)
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout.buffer.write(output.encode('utf-8'))
    else:
        sys.stdout.write(output.render())


def get_valid_cwd():
    """
    Get the current working dir.
    The current working dir can be not valid: for instance when I delete a parent dir or when I
    git checkout a branch which does not have the current dir. In this case we return the current
    invalid dir (because this is what the OS thinks) but we display a warning.
    """
    try:
        cwd = os.getcwd()
    except FileNotFoundError:
        cwd = os.getenv('PWD')  # This is where the OS thinks we are.
        parts = cwd.split(os.sep)
        up = cwd
        while parts and not os.path.exists(up):
            parts.pop()
            up = os.sep.join(parts)
        try:
            os.chdir(up)
        except Exception:
            print_warning('Your current directory is invalid!')
            exit(1)
        print_warning('Your current directory is invalid!\n'
                      'Closest valid parent directory: {}'.format(up))
    return cwd


def get_terminal_columns_n():
    _, columns = os.popen('stty size', 'r').read().split()
    return int(columns)