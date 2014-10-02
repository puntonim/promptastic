import colors
import config


class Segment:
    bg = ''  # Default: no color.
    fg = ''  # Default: no color.

    def __init__(self, *args, **kwargs):
        class_name = type(self).__name__.lower()
        if class_name in ['newline', 'root', 'divider', 'padding']:
            # These segments are always active.
            self.active = True
        else:
            # Other segments are active if the config files states so.
            self.active = config.SEGMENTS.get(class_name, False)

        if self.active:
            self.init(*args, **kwargs)

    def init(self):
        pass

    def render(self):
        output = list()
        output.append(self.bg)
        output.append(self.fg)
        output.append(self.text)
        output.append(colors.reset() if self.bg or self.fg else '')
        return ''.join(output)

    def length(self):
        return len(self.text)