#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from segments import UserAtHost, Divider, Padding, CurrentDir, Time, NewLine, Root, Jobs, ReadOnly
from utils import get_valid_cwd, get_terminal_columns_n


class Prompt:
    def __init__(self):
        self.cwd = get_valid_cwd()

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

    def _render_first_line(self):
        # List of segments for the first line (left part, padding, right part).
        # Add left part segments.
        segments = self.first_line_left

        # Compute the length of the padding between the left part and the right part.
        padding_len = self._compute_padding_length_first_line()

        # Add padding segment.
        if padding_len:
            segments.append(Padding(padding_len))

        # Finally add right part segments.
        segments.extend(self.first_line_right)
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

    def _clean_segments(self):
        """
        Remove inactive segments.
        F.i. the job segment is inactive when there is no job.
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
        # Commented out because the last_line is always safe.
        #self.last_line = remove_duplicated_dividers(remove_inactive(self.last_line))

    def _compute_padding_length_first_line(self):
        """
        Compute the padding length, which is the number of empty spaces to place between
        the left part and the right part.
        """
        # Check whether the right part starts with a Divider.
        right_starts_w_divider = True if isinstance(self.first_line_right[0], Divider) else False

        # Terminal width.
        cols = get_terminal_columns_n()

        # Total length of the text (without the initial divider of the right part, in case).
        text_len = (self._get_total_segments_length(self.first_line_left) +
                    self._get_total_segments_length(self.first_line_right))
        text_len -= Divider().length() if right_starts_w_divider else 0

        # Padding dimension formula.
        padding_len = cols - (text_len % cols)

        # If the padding length is exactly one column, then we don't need padding at all.
        if padding_len == cols:
            padding_len = 0
            # And we also don't need the initial divider in the right part.
            if right_starts_w_divider:
                self.first_line_right.pop(0)
        # Else: remove from padding_len the length of the initial divider, in case.
        else:
            padding_len -= Divider().length() if right_starts_w_divider else 0

        return padding_len

    @staticmethod
    def _get_total_segments_length(segments):
        return sum([x.length() for x in segments])

    @staticmethod
    def _color_dividers(segments):
        for i, segment in enumerate(segments):
            # We need to color a divider based on the colors of the previous and next segments.
            if isinstance(segment, Divider):
                prev = segments[i-1] if i > 0 else None
                next_ = segments[i+1] if i+1 < len(segments) else None
                segment.set_colors(prev, next_)
        return segments


if __name__ == '__main__':
    prompt = Prompt()

    # First line left (order: left to right).
    prompt.first_line_left.append(UserAtHost())
    prompt.first_line_left.append(Divider())
    prompt.first_line_left.append(CurrentDir(prompt.cwd))
    prompt.first_line_left.append(Divider())
    prompt.first_line_left.append(ReadOnly(prompt.cwd))
    prompt.first_line_left.append(Divider())

    # First line right (order: left to right).
    prompt.first_line_right.append(Divider())
    prompt.first_line_right.append(Jobs())
    prompt.first_line_right.append(Divider())
    prompt.first_line_right.append(Time())

    # Last line.
    prompt.last_line.append(Root())

    sys.stdout.write(prompt.render())