import os

from segments import Segment
import colors
import glyphs


class CurrentDir(Segment):
    bg = colors.background(colors.DARK_GREY)
    fg = colors.foreground(colors.LIGHT_GREY)

    def init(self, cwd):
        home = os.path.expanduser('~')
        self.text = cwd.replace(home, '~')


class ReadOnly(Segment):
    bg = colors.background(colors.LIGHT_GREY)
    fg = colors.foreground(colors.RED)

    def init(self, cwd):
        self.text = ' {} '.format(glyphs.LOCK)

        if os.access(cwd, os.W_OK):
            self.active = False


class Venv(Segment):
    bg = colors.background(colors.SMERALD)
    fg = colors.foreground(colors.EXTRA_LIGHT_GREY)

    def init(self):
        env = os.getenv('VIRTUAL_ENV')
        if env is None:
            self.active = False
            return

        env_name = os.path.basename(env)
        self.text = '{} {}'.format(glyphs.VIRTUAL_ENV, env_name)