#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os import popen

from segments import UserAtHost, Divider, Padding, CurrentDir, Time, NewLine, Root


class Prompt:
    def __init__(self):
        self.segments = []

    def append_left(self, segment):
        self.segments.append(segment)

    def append_right_group_and_new_line(self, segment):
        cols = self._get_console_columns_n()
        text_len = self._get_current_prompt_length() + segment.length()
        delta = cols - (text_len % cols)
        self.append_left(Padding(delta))
        self.append_left(segment)
        self.append_left(NewLine())

    def render(self):
        #return ''.join([x.render() for x in self.segments])
        output = ''
        for i, segment in enumerate(self.segments):
            # We need to color a divider based on the colors of the previous and next segments.
            if isinstance(segment, Divider):
                prev = self.segments[i-1] if i > 0 else None
                next = self.segments[i+1] if i+1 < len(self.segments) else None
                segment.set_colors(prev, next)

            output += segment.render()
        return output

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
    prompt.append_left(Divider())
    prompt.append_right_group_and_new_line(Time())
    prompt.append_left(Root())
    sys.stdout.write(prompt.render())