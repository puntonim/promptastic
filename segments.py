from datetime import datetime
from getpass import getuser
from socket import gethostname
from os.path import expanduser
from os import getcwd

import symbols
import colors


class Segment:
    bg = ''  # Default: no color.
    fg = ''  # Default: no color.

    def render(self):
        output = list()
        output.append(self.bg)
        output.append(self.fg)
        output.append(self.text)
        output.append(colors.reset() if self.bg or self.fg else '')
        return ''.join(output)

    def length(self):
        return len(self.text)


class UserAtHost(Segment):
    bg = colors.background(colors.MID_GREY)
    fg = colors.foreground(colors.LIGHT_GREY)

    text = '{}@{}'.format(
        getuser(),
        gethostname().replace('.local', '')
    )


class Divider(Segment):
    bg = colors.background(colors.DARK_GREY)
    fg = colors.foreground(colors.MID_GREY)

    text = symbols.DIVIDER_RIGHT


class CurrentDir(Segment):
    bg = colors.background(colors.DARK_GREY)
    fg = colors.foreground(colors.LIGHT_GREY)

    home = expanduser('~')
    text = getcwd().replace(home, '~')


class Time(Segment):
    bg = colors.background(colors.DARKER_GREY)
    fg = colors.foreground(colors.DARK_GREY)

    now = datetime.now().time()
    text = '{} {}:{}:{}'.format(
        symbols.TIME,
        now.hour,
        now.minute,
        now.second
    )


class Padding(Segment):
    def __init__(self, amount):
        self.text = ''.ljust(amount)


class NewLine(Segment):
    text = '\r\n'


class Root(Segment):
    text = '\\$ '