from datetime import datetime
from getpass import getuser
from socket import gethostname
from os.path import expanduser
from os import getcwd, getppid
from subprocess import Popen, PIPE
from re import findall

import symbols
import colors


class Segment:
    bg = ''  # Default: no color.
    fg = ''  # Default: no color.

    def __init__(self):
        self.active = True

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
    bg = colors.background(colors.SMERALD)
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()
        self.text = '{}@{}'.format(
            getuser(),
            gethostname().replace('.local', '')
        )


class Divider(Segment):
    text = symbols.DIVIDER_RIGHT

    def set_colors(self, prev, next):
        if next:
            self.bg = next.bg

        if prev:
            self.fg = prev.bg.replace('setab', 'setaf')


class CurrentDir(Segment):
    bg = colors.background(colors.DARK_GREY)
    fg = colors.foreground(colors.LIGHT_GREY)

    def __init__(self):
        super().__init__()
        home = expanduser('~')
        self.text = getcwd().replace(home, '~')


class Time(Segment):
    bg = colors.background(colors.DARKER_GREY)
    fg = colors.foreground(colors.MID_DARK_GREY)

    def __init__(self):
        super().__init__()
        now = datetime.now().time()
        self.text = '{} {}:{}:{}'.format(
            symbols.TIME,
            now.hour,
            now.minute,
            now.second
        )


class Padding(Segment):
    bg = colors.background(colors.MORE_DARKER_GREY)

    def __init__(self, amount):
        super().__init__()
        self.text = ''.ljust(amount)


class NewLine(Segment):
    text = '\r\n'


class Root(Segment):
    text = '\\$ '


class Jobs(Segment):
    bg = colors.background(colors.MID_ORANGE)
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()
        pppid = Popen(['ps', '-p', str(getppid()), '-oppid='], stdout=PIPE).communicate()[0].strip()
        output = Popen(['ps', '-a', '-o', 'ppid'], stdout=PIPE).communicate()[0]
        num_jobs = len(findall(bytes(pppid), output)) - 1

        self.text = '{} {}'.format(symbols.HOURGLASS, num_jobs)

        if not num_jobs:
            self.active = False