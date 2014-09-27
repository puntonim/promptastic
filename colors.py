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
LIGHTER_RED = 196
LIGHT_RED = 160
RED = 124

LIGHT_GREEN = 148
MID_GREEN = 35
SMERALD = 29
DARK_GREEN = 22

GOLD = 94
LIGHT_GOLD = 3
LIGHTER_GOLD = 178


def foreground(color):
    return '\[$(tput setaf {})\]'.format(color)


def background(color):
    return '\[$(tput setab {})\]'.format(color)


def reset():
    return '\[$(tput sgr0)\]'


def underline_start():
    return '\[$(tput smul)\]'


def underline_end():
    return '\[$(tput rmul)\]'