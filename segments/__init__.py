import colors


class Segment:
    bg = ''  # Default: no color.
    fg = ''  # Default: no color.

    def __init__(self):
        self.active = True

    def render(self):
        output = list()
        output.append(self.bg)
        output.append(self.fg)
        output.append(self.text)
        output.append(colors.reset() if self.bg or self.fg else '')
        return ''.join(output)

    def length(self):
        return len(self.text)