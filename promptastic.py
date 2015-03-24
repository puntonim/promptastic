#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from segments import basics, sysinfo, filesystem, git, network
from utils.sys import get_valid_cwd, get_terminal_columns_n

FileNotFoundError = getattr(__builtins__, 'FileNotFoundError', IOError)


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
            segments.append(basics.Padding(padding_len))

        # Finally add right part segments.
        segments.extend(self.first_line_right)
        segments.append(basics.NewLine())

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
            return [x for x in segments if x.active]

        def remove_duplicated_dividers(segments):
            # Collect in a list all indexes of elements in `segments` which must be removed ('cause
            # they are duplicated dividers).
            to_remove = []
            for i in range(len(segments)-1):
                if isinstance(segments[i], basics.Divider) and isinstance(segments[i+1],
                                                                          basics.Divider):
                    to_remove.append(i)

            # Remove from segments the collected indexes.
            for counter, i in enumerate(to_remove):
                segments.pop(i - counter)
            return segments

        def strip():
            # Remove initial Divider, if any.
            if isinstance(self.first_line_left[0], basics.Divider):
                self.first_line_left.pop(0)

            # Remove final Divider, if any.
            if isinstance(self.first_line_right[-1], basics.Divider):
                self.first_line_right.pop(-1)

        self.first_line_left = remove_duplicated_dividers(remove_inactive(self.first_line_left))
        self.first_line_right = remove_duplicated_dividers(remove_inactive(self.first_line_right))
        # Commented out because the last_line is always safe.
        #self.last_line = remove_duplicated_dividers(remove_inactive(self.last_line))
        strip()

    def _compute_padding_length_first_line(self):
        """
        Compute the padding length, which is the number of empty spaces to place between
        the left part and the right part.
        """
        # Check whether the right part starts with a Divider.
        right_starts_w_divider = (True if self.first_line_right and
                                  isinstance(self.first_line_right[0], basics.Divider) else False)

        # Terminal width.
        cols = get_terminal_columns_n()

        # Total length of the text (without the initial divider of the right part, in case).
        text_len = (self._get_total_segments_length(self.first_line_left) +
                    self._get_total_segments_length(self.first_line_right))
        text_len -= basics.Divider().length() if right_starts_w_divider else 0

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
            padding_len -= basics.Divider().length() if right_starts_w_divider else 0

        return padding_len

    @staticmethod
    def _get_total_segments_length(segments):
        return sum([x.length() for x in segments])

    @staticmethod
    def _color_dividers(segments):
        for i, segment in enumerate(segments):
            # We need to color a divider based on the colors of the previous and next segments.
            if isinstance(segment, basics.Divider):
                prev = segments[i-1] if i > 0 else None
                next_ = segments[i+1] if i+1 < len(segments) else None
                segment.set_colors(prev, next_)
        return segments


if __name__ == '__main__':
    prompt = Prompt()

    # First line left (order: left to right).
    prompt.first_line_left.append(sysinfo.UserAtHost())
    prompt.first_line_left.append(basics.Divider())
    prompt.first_line_left.append(network.Ssh())
    prompt.first_line_left.append(basics.Divider())
    prompt.first_line_left.append(filesystem.CurrentDir(prompt.cwd))
    prompt.first_line_left.append(basics.Divider())
    prompt.first_line_left.append(filesystem.ReadOnly(prompt.cwd))
    prompt.first_line_left.append(basics.Divider())
    prompt.first_line_left.append(basics.ExitCode())
    prompt.first_line_left.append(basics.Divider())

    # First line right (order: left to right).
    prompt.first_line_right.append(basics.Divider())
    prompt.first_line_right.append(git.Git())
    prompt.first_line_right.append(basics.Divider())
    prompt.first_line_right.append(filesystem.Venv())
    prompt.first_line_right.append(basics.Divider())
    prompt.first_line_right.append(sysinfo.Jobs())
    prompt.first_line_right.append(basics.Divider())
    prompt.first_line_right.append(sysinfo.Time())

    # Last line.
    prompt.last_line.append(basics.Root())

    if hasattr(sys.stdout, 'buffer'):
        sys.stdout.buffer.write(prompt.render().encode('utf-8'))
    else:
        sys.stdout.write(prompt.render())