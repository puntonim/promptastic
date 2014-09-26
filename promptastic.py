#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os import popen

from segments import UserAtHost, Divider, Padding, CurrentDir, Time, NewLine, Root, Jobs


class Prompt:
    def __init__(self):
        self.first_line_left = []
        self.first_line_right = []
        self.last_line = []

    def render(self):
        """
        Render the prompt with the appropriate syntax.
        """
        # Remove inactive segments and duplicated Dividers.
        self._clean_segments()

        # Render first and last lines.
        first_line = self._render_first_line()
        last_line = self._render_last_line()

        # Return the entire prompt.
        return first_line + last_line

    def _clean_segments(self):
        """
        Remove inactive segments.
        """
        def remove_inactive(segments):
            active_segments = []
            for i, segment in enumerate(segments):
                if segment.active:
                    active_segments.append(segment)
            return active_segments

        def remove_duplicated_dividers(segments):
            to_remove = []
            for i in range(len(segments)-1):
                if isinstance(segments[i], Divider) and isinstance(segments[i+1], Divider):
                    to_remove.append(i)
            for i in to_remove:
                segments.pop(i)
            return segments

        self.first_line_left = remove_duplicated_dividers(remove_inactive(self.first_line_left))
        self.first_line_right = remove_duplicated_dividers(remove_inactive(self.first_line_right))
        #self.last_line = remove_inactive(self.last_line)  # last_line is always safe.

    def _render_first_line(self):
        segments = self.first_line_left

        # Check whether the right part starts with a Divider.
        right_starts_w_divider = True if isinstance(self.first_line_right[0], Divider) else False

        # Terminal width.
        cols = self._get_console_columns_n()

        # Total length of the text (without the initial divider of the right part, in case).
        text_len = (self._get_total_segments_length(self.first_line_left) +
                    self._get_total_segments_length(self.first_line_right))
        text_len -= Divider().length() if right_starts_w_divider else 0

        # Delta = number of empty spaces to write.
        delta = cols - (text_len % cols)

        # In case no empty space is needed, we remove the initial divider, in case there is.
        if cols == delta:
            if right_starts_w_divider:
                self.first_line_right.pop(0)
        else:
            # Remove from delta the length of the initial divider, in case there is.
            delta -= Divider().length() if right_starts_w_divider else 0
            segments.append(Padding(delta))

        # Finally add right part segments.
        for segment in self.first_line_right:
            segments.append(segment)
        segments.append(NewLine())

        # Color the dividers.
        segments = self._color_dividers(segments)

        # Render the resulting segments.
        output = ''
        for segment in segments:
            output += segment.render()
        return output

    def _render_last_line(self):
        output = ''
        for segment in self.last_line:
            output += segment.render()
        return output

    @staticmethod
    def _get_console_columns_n():
        _, columns = popen('stty size', 'r').read().split()
        return int(columns)

    @staticmethod
    def _get_total_segments_length(segments):
        return sum([x.length() for x in segments])

    @staticmethod
    def _color_dividers(segments):
        for i, segment in enumerate(segments):
            # We need to color a divider based on the colors of the previous and next segments.
            if isinstance(segment, Divider):
                prev = segments[i-1] if i > 0 else None
                next = segments[i+1] if i+1 < len(segments) else None
                segment.set_colors(prev, next)
        return segments


if __name__ == '__main__':
    prompt = Prompt()

    # First line left (order: left to right).
    prompt.first_line_left.append(UserAtHost())
    prompt.first_line_left.append(Divider())
    prompt.first_line_left.append(CurrentDir())
    prompt.first_line_left.append(Divider())

    # First line right (order: left to right).
    prompt.first_line_right.append(Divider())
    prompt.first_line_right.append(Jobs())
    prompt.first_line_right.append(Divider())
    prompt.first_line_right.append(Time())

    # Last line.
    prompt.last_line.append(Root())

    sys.stdout.write(prompt.render())