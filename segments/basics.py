import sys

from segments import Segment, theme
from utils import colors, glyphs


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
    bg = colors.background(theme.EXITCODE_BG)
    fg = colors.foreground(theme.EXITCODE_FG)

    def init(self):
        self.text = ' {} '.format(glyphs.CROSS)

        if sys.argv[1] == '0':
            self.active = False


class Padding(Segment):
    bg = colors.background(theme.PADDING_BG)

    def init(self, amount):
        self.text = ''.ljust(amount)