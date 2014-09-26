from datetime import datetime
from getpass import getuser
from socket import gethostname
from os.path import expanduser
from os import getcwd

import symbols


class Segment:
    reset = '\[$(tput sgr0)\]'
    bg = '\[$(tput setab {})\]'
    fg = '\[$(tput setaf {})\]'

    def render(self):
        output = list()
        output.append(self.bg if self.bg else '')
        output.append(self.fg if self.fg else '')
        output.append(self.text)
        output.append(self.reset if self.bg or self.fg else '')
        return ''.join(output)

    def length(self):
        return len(self.text)


class UserAtHost(Segment):
    bg = Segment.bg.format(240)
    fg = Segment.fg.format(250)
    text = '{}@{}'.format(
        getuser(),
        gethostname().replace('.local', '')
    )


class Divider(Segment):
    bg = Segment.bg.format(237)
    fg = Segment.fg.format(240)
    text = symbols.DIVIDER_RIGHT


class CurrentDir(Segment):
    bg = Segment.bg.format(237)
    fg = Segment.fg.format(250)
    home = expanduser('~')
    text = getcwd().replace(home, '~')


class Time(Segment):
    bg = Segment.bg.format(235)
    fg = Segment.fg.format(237)
    now = datetime.now().time()
    text = '{} {}:{}:{}'.format(
        symbols.TIME,
        now.hour,
        now.minute,
        now.second
    )


class Padding(Segment):
    bg = None
    fg = None

    def __init__(self, amount):
        self.text = ''.ljust(amount)