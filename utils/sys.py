def print_raw(text):
    import sys

    if hasattr(sys.stdout, 'buffer'):
        sys.stdout.buffer.write(text.encode('utf-8'))
    else:
        sys.stdout.write(text.render())


def print_warning(text):
    from utils import colors
    from utils.glyphs import ESCLAMATION
    from segments.basics import Divider

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
    print_raw(output)


def get_valid_cwd():
    """
    Get the current working dir.
    The current working dir can be not valid: for instance when I delete a parent dir or when I
    git checkout a branch which does not have the current dir. In this case we return the current
    invalid dir (because this is what the OS thinks) but we display a warning.
    """
    import os

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
    import os

    _, columns = os.popen('stty size', 'r').read().split()
    return int(columns)


def get_current_theme_name():
    import config
    import os

    try:
        name = config.THEME
        if not name:
            raise ValueError
        path = os.sep.join([os.path.abspath(os.path.dirname(__file__)), '../themes', '{}.py'.format(name)])
        if not os.path.isfile(path):
            raise FileNotFoundError
        return name
    except AttributeError:
        print_raw('Promptastic ERROR: the config.py file does not contain a THEME attribute.')
        exit(1)
    except ValueError:
        print_raw('Promptastic ERROR: the THEME setting in the file config.py seems to be empty.')
        exit(1)
    except FileNotFoundError:
        print_raw('Promptastic ERROR: {}.py is not a file in the themes directory.'.format(name))
        exit(1)
