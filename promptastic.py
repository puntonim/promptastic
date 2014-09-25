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

    def append_right_group_and_new_line(self, group):
        # Check whether the first segment is a Divider.
        starts_w_divider = True if isinstance(group[0], Divider) else False
        # Terminal width.
        cols = self._get_console_columns_n()
        # Total length of the text (without the initial divider, in case there is).
        text_len = self._get_current_prompt_length() + sum(x.length() for x in group)
        text_len -= Divider().length() if starts_w_divider else 0
        # Delta = number of empty spaces to write.
        delta = cols - (text_len % cols)
        # In case non empty space is needed, we remove the initial divider, in case there is.
        if cols == delta:
            if starts_w_divider:
                group.pop(0)
        else:
            # Remove from delta the length of the initial divider, in case there is.
            delta -= Divider().length() if starts_w_divider else 0
            self.append_left(Padding(delta))
        # Add right group segments.
        for segment in group:
            self.append_left(segment)
        self.append_left(NewLine())

    def render(self):
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
    prompt.append_right_group_and_new_line([Divider(), Time()])
    prompt.append_left(Root())
    sys.stdout.write(prompt.render())