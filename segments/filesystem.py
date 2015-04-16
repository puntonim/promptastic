import os

from segments import Segment, theme
from utils import colors, glyphs


class CurrentDir(Segment):
    bg = colors.background(theme.CURRENTDIR_BG)
    fg = colors.foreground(theme.CURRENTDIR_FG)

    def init(self, cwd):
        home = os.path.expanduser('~')
        self.text = cwd.replace(home, '~')


class ReadOnly(Segment):
    bg = colors.background(theme.READONLY_BG)
    fg = colors.foreground(theme.READONLY_FG)

    def init(self, cwd):
        self.text = ' ' + glyphs.WRITE_ONLY + ' '

        if os.access(cwd, os.W_OK):
            self.active = False


class Venv(Segment):
    bg = colors.background(theme.VENV_BG)
    fg = colors.foreground(theme.VENV_FG)

    def init(self):
        env = os.getenv('VIRTUAL_ENV')
        if env is None:
            self.active = False
            return

        env_name = os.path.basename(env)
        self.text = glyphs.VIRTUAL_ENV + ' ' + env_name