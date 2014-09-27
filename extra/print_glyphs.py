# Works only with Python3

import sys

glyphs = {
    'DIVIDER_RIGHT': '',
    'DIVIDER_RIGHT_SOFT': '',
    'DIVIDER_LEFT': '',
    'DIVIDER_LEFT_SOFT': '',
    'BRANCH': '',
    'ELLIPSIS': '⋯',
    'LINE_NUMBER': '',
    'TIME1': '⌚',
    'TIME2': '⏰',
    'TIME3': '꒾',
    'TIME4': '⏳',
    'TIME5': '⌛',
    'DOWN': '⬇',
    'UP': '⬆',
    'LOCK': '',
    'FALLBACK': '♫',
    'PLAY': '▶',
    #'PAUSE': '▮▮',
    'STOP1': '■',
    'STOP2': '▇',
    'FULL_HEART': '♥',
    'EMPTY_HEART': '♡',
    'UPTIME': '⇑',
    'EMAIL': '✉',
    'VIRTUAL_ENV1': 'ⓔ',
    'VIRTUAL_ENV2': 'ⓥ',
    'CIRCLE': '〇',
    'BLUSTERY': '⚑',
    'RAINY1': '☔',
    'RAINY2': '☂',
    'CLOUDY1': '☁',
    'CLOUDY2': '⛅',
    'SNOWY1': '⛄',
    'SNOWY2': '❅',
    'STORMY': '☈',
    'FOGGY': '≡',
    'SUNNY': '☼',
    'NIGHT': '☾',
    'WINDY': '☴',
    'NOT_AVAILABLE': '�',
    'UNKNOWN': '⚠',
    'DOT': '·',
    'HAND1': '✊',
    'HAND2': '✋',
    'V1': '✓',
    'V2': '✔',
    'X1': '✕',
    'X2': '✖',
    'X3': '✗',
    'X4': '✘',
    'X5': '❌',
    'QUESTION1': '❓',
    'QUESTION2': '❔',
    'ESCLAMATION1': '❕',
    'ESCLAMATION2': '❗',
    'BALL1': '⚽',
    'BALL2': '⚾',
    'LIGHT': '⚡',
    'STARS': '✨',
    'STAR': '⭐',
}



def print_all_chars():
    # Chars should go from chr(0) to chr(110000), but there is nothing after around 68000
    for x in range(68000):
        try:
            print(chr(x), end=' ')
        except UnicodeEncodeError:
            pass


def print_collected_chars():
    for x in sorted(glyphs.values()):
        print('{} = {}'.format(x, ord(x)))

    print('\nNote: you can use the shown number in Python3 (not 2), like this:\n'
          '>>> print(chr(57520))\n'
          '{}'.format(chr(57520)))

    print('\nNote: Use the command line argument `all` to print all symbols.')

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'all':
            print_all_chars()
            exit(0)
    except IndexError:
        pass

    print_collected_chars()