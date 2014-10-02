import os

from segments import Segment, theme
from utils import colors


class Ssh(Segment):
    bg = colors.background(theme.SSH_BG)
    fg = colors.foreground(theme.SSH_FG) + colors.bold()

    def init(self):
        self.text = 'SSH'

        if not os.getenv('SSH_CLIENT'):
            self.active = False