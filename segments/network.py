import os

from segments import Segment
from utils import colors


class Ssh(Segment):
    bg = colors.background(colors.LIGHT_ORANGE)
    fg = colors.foreground(colors.WHITE) + colors.bold()

    def init(self):
        self.text = 'SSH'

        if not os.getenv('SSH_CLIENT'):
            self.active = False