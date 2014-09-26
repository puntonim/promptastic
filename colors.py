# Colors
WHITE = 15
BLACK = 0

NEARLY_WHITE_GREY = 254
LIGHT_GREY = 250
MID_GREY = 240
MID_DARK_GREY = 238
DARK_GREY = 237
DARKER_GREY = 235
MORE_DARKER_GREY = 234
DARKEST_GREY = 232 # or 16.

BLUEISH = 31

MID_ORANGE = 166
PINKISH_RED = 161

LIGHT_GREEN = 148
MID_GREEN = 35
SMERALD = 29
DARK_GREEN = 22


def foreground(color):
    return '\[$(tput setaf {})\]'.format(color)


def background(color):
    return '\[$(tput setab {})\]'.format(color)


def reset():
    return '\[$(tput sgr0)\]'