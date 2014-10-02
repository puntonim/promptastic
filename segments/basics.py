import sys

from segments import Segment
import colors
import glyphs


class NewLine(Segment):
    text = '\r\n'


class Root(Segment):
    text = '\\$ '


class Divider(Segment):
    text = glyphs.DIVIDER_RIGHT

    def set_colors(self, prev, next):
        self.bg = next.bg if next and next.bg else Padding.bg
        self.fg = prev.bg if prev and prev.bg else Padding.bg
        self.fg = self.fg.replace('setab', 'setaf')


class ExitCode(Segment):
    bg = colors.background(colors.RED)
    fg = colors.foreground(colors.WHITE)

    def init(self):
        self.text = ' {} '.format(glyphs.CROSS)

        if sys.argv[1] == '0':
            self.active = False


class Padding(Segment):
    bg = colors.background(colors.EXTRA_DARK_GREY)

    def init(self, amount):
        self.text = ''.ljust(amount)