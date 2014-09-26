#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os import popen

from segments import UserAtHost, Divider, Padding, CurrentDir, Time


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
        return int(columns)

    def _get_current_prompt_length(self):
        return sum([x.length() for x in self.segments])


if __name__ == '__main__':
    prompt = Prompt()
    prompt.append_left(UserAtHost())
    prompt.append_left(Divider())
    prompt.append_left(CurrentDir())

    prompt.append_right_and_new_line(Time())

    sys.stdout.write(prompt.render())