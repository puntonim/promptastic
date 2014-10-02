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
    'CIRCLED_U': 'ⓤ',
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
    'SUNNY1': '☼',
    'SUNNY2': '☀',
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
    'PEN1': '',
    'PEN2': '✎',
    'LEFT1': '⤌',
    'RIGHT1': '⤍',
    'LEFT2': '⤎',
    'RIGHT2': '⤏',
    'LEFT3':  '⬸',
    'RIGHT3': '⤑',
    'ONE1': '➀',
    'TWO1': '➁',
    'THREE1': '➂',
    'FOUR1': '➃',
    'FIVE1': '➄',
    'SIX1': '➅',
    'SEVEN1': '➆',
    'EIGHT1': '➇',
    'NINE1': '➈',
    'TEN1': '➉',
    'ONE2': '➊',
    'TWO2': '➋',
    'THREE2': '➌',
    'FOUR2': '➍',
    'FIVE2': '➎',
    'SIX2': '➏',
    'SEVEN2': '➐',
    'EIGHT2': '➑',
    'NINE2': '➒',
    'TEN2': '➓',
    'ONE0': '①',
    'TWO0': '②',
    'THREE0': '③',
    'FOUR0': '④',
    'FIVE0': '⑤',
    'SIX0': '⑥',
    'SEVEN0': '⑦',
    'EIGHT0': '⑧',
    'NINE0': '⑨',
    'TEN0': '⑩',
    'ELEVEN0': '⑪',
    'TWELVE0': '⑫',
    'THIRTEEN0': '⑬',
    'FOURTEEN0': '⑭',
    'FIFTEEN0': '⑮',
    'SIXTEEN0': '⑯',
    'SEVENTEEN0': '⑰',
    'EIGHTEEN0': '⑱',
    'NINETEEN0': '⑲',
    'TWENTY0': '⑳',
}


def print_all_chars():
    # Chars should go from chr(0) to chr(110000), but there is nothing after around 68000
    for x in range(68000):  #26950
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