from subprocess import Popen, PIPE
from os import getppid
from re import findall
from datetime import datetime
from getpass import getuser
from socket import gethostname

from segments import Segment
import colors
import glyphs


class Jobs(Segment):
    bg = colors.background(colors.DARK_PURPLE)
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()
        pppid = Popen(['ps', '-p', str(getppid()), '-oppid='], stdout=PIPE).communicate()[0].strip()
        output = Popen(['ps', '-a', '-o', 'ppid'], stdout=PIPE).communicate()[0]
        num_jobs = len(findall(bytes(pppid), output)) - 1

        self.text = '{} {}'.format(glyphs.HOURGLASS, num_jobs)

        if not num_jobs:
            self.active = False


class Time(Segment):
    bg = colors.background(colors.DARKER_GREY)
    fg = colors.foreground(colors.MID_DARK_GREY)

    def __init__(self):
        super().__init__()
        now = datetime.now().time()
        self.text = '{} {}:{}:{}'.format(
            glyphs.TIME,
            now.hour,
            now.minute,
            now.second
        )


class UserAtHost(Segment):
    bg = colors.background(colors.SMERALD)
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()
        self.text = '{}@{}'.format(
            getuser(),
            gethostname().replace('.local', '')
        )