"""
Check out this website for the entire Unicode characters list:
http://unicode-table.com
"""
import config


# Python 2 and 3 compatibility: chr(n) in Python3, unichr(n).encode('utf-8') in Python2.
try:
    # Note: exceptions raised by the lambda function are not caught by the next `except` clause,
    # so we first run a unichr() to raise an exception in Python 3.
    unichr(0)
    # chr = lambda x: unichr(x).encode('utf-8')
    chr = lambda x: unichr(x)
except NameError:
    # Then we are in Python3 (which has no unichr()).
    pass


# *_PATCHED glyphs exist only in patched fonts (available at:
# https://github.com/Lokaltog/powerline-fonts).
DIVIDER_RIGHT_PATCHED = chr(57520)
DIVIDER_RIGHT_SOFT_PATCHED = chr(57521)
DIVIDER_LEFT_PATCHED = chr(57522)
DIVIDER_LEFT_SOFT_PATCHED = chr(57523)
BRANCH1_PATCHED = chr(57504)

# All other glyphs exist in any font.
BRANCH2 = chr(11075)
TIME = chr(8986)
VIRTUAL_ENV = chr(9445)
TIME = chr(8986)
HOURGLASS = chr(8987)
CROSS = chr(10006)
ESCLAMATION = chr(10069)
LOCK = chr(57506)
N1 = chr(10122)
N2 = chr(10123)
N3 = chr(10124)
N4 = chr(10125)
N5 = chr(10126)
N6 = chr(10127)
N7 = chr(10128)
N8 = chr(10129)
N9 = chr(10130)
N10 = chr(10131)
LEFT_ARROW = chr(10510)
RIGHT_ARROW = chr(10511)
PEN = chr(63490)
SUNNY = chr(9728)
CLOUDY = chr(9729)
RAINY = chr(9730)

# Branch and divider glyphs are different depending on whether the current theme is using
# patched fonts or not.
BRANCH = BRANCH1_PATCHED if config.PATCHED_FONTS else BRANCH2
DIVIDER = DIVIDER_RIGHT_PATCHED if config.PATCHED_FONTS else ''
WRITE_ONLY = LOCK if config.PATCHED_FONTS else PEN