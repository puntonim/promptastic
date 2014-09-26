#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from getpass import getuser
from socket import gethostname
from os.path import expanduser
from os import getcwd, popen
from datetime import datetime


class Symbol:
    DIVIDER_RIGHT = chr(57520)
    DIVIDER_RIGHT_SOFT = chr(57521)
    DIVIDER_LEFT = chr(57522)
    DIVIDER_LEFT_SOFT = chr(57523)
    BRANCH = chr(57504)
    TIME = chr(8986)
    VIRTUAL_ENV = chr(9445)
    TIME = chr(8986)


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
    #text = ':'
    #text = u'\uE0B0'.encode('utf-8')
    #text = u'\uE0B0'
    #text = ''  # '\xee\x82\xb0'
    text = Symbol.DIVIDER_RIGHT


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
        Symbol.TIME,
        now.hour,
        now.minute,
        now.second
    )


class Padding(Segment):
    bg = None
    fg = None

    def __init__(self, amount):
        self.text = ''.ljust(amount)


class Prompt:
    def __init__(self):
        self.segments = []

    def append_left(self, segment):
        self.segments.append(segment)

    def append_right_and_new_line(self, segment):
        cols = self._get_console_columns_n()
        text_len = self._get_current_prompt_length() + segment.length()
        delta = cols - (text_len % cols)
        self.append_left(Padding(delta))
        self.append_left(segment)

    def render(self):
        output = ''.join([x.render() for x in self.segments])
        return output + '\r\n\\$ '

    @staticmethod
    def _get_console_columns_n():
        _, columns = popen('stty size', 'r').read().split()
        # A second option is:
        #cols = os.popen('tput cols').read()
        return int(columns)

    def _get_current_prompt_length(self):
        return sum([x.length() for x in self.segments])


if __name__ == '__main__':
    #prompt = '${debian_chroot:+($debian_chroot)}\\u@\\h:\\w\\$ '
    #prompt = "${debian_chroot:+($debian_chroot)}\[$(tput setaf 250)\]\[$(tput bold)\]\\u\[$(tput sgr0)\]@\\h\[$(tput sgr0)\] \[$(tput setaf 7)\][\\t] \\w\n\[$(tput setaf 7)\]\[$(tput bold)\]\\$\[$(tput sgr0)\] "

    #if hasattr(sys.stdout, 'buffer'):
    #    sys.stdout.buffer.write(draw_prompt())
    #else:
    #    sys.stdout.write(draw_prompt())

    prompt = Prompt()
    prompt.append_left(UserAtHost())
    prompt.append_left(Divider())
    prompt.append_left(CurrentDir())

    prompt.append_right_and_new_line(Time())

    sys.stdout.write(prompt.render())