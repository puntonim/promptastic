from os import getenv

from segments import Segment
import colors


class Ssh(Segment):
    bg = colors.background(colors.LIGHT_ORANGE)
    fg = colors.foreground(colors.WHITE) + colors.bold()

    def __init__(self):
        super().__init__()
        self.text = 'SSH'

        if not getenv('SSH_CLIENT'):
            self.active = False