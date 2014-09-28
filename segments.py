from datetime import datetime
from getpass import getuser
from socket import gethostname
from os import getppid, access, W_OK, getenv, path
from subprocess import Popen, PIPE
from re import findall
from sys import argv

import glyphs
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


class UserAtHost(Segment):
    bg = colors.background(colors.SMERALD)
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()
        self.text = '{}@{}'.format(
            getuser(),
            gethostname().replace('.local', '')
        )


class Divider(Segment):
    text = glyphs.DIVIDER_RIGHT

    def set_colors(self, prev, next):
        self.bg = next.bg if next and next.bg else Padding.bg
        self.fg = prev.bg if prev and prev.bg else Padding.bg
        self.fg = self.fg.replace('setab', 'setaf')


class CurrentDir(Segment):
    bg = colors.background(colors.DARK_GREY)
    fg = colors.foreground(colors.LIGHT_GREY)

    def __init__(self, cwd):
        super().__init__()
        home = path.expanduser('~')
        self.text = cwd.replace(home, '~')


class Time(Segment):
    bg = colors.background(colors.DARKER_GREY)
    fg = colors.foreground(colors.MID_DARK_GREY)

    def __init__(self):
        super().__init__()
        now = datetime.now().time()
        self.text = '{} {}:{}:{}'.format(
            glyphs.TIME,
            now.hour,
            now.minute,
            now.second
        )


class Padding(Segment):
    bg = colors.background(colors.MORE_DARKER_GREY)

    def __init__(self, amount):
        super().__init__()
        self.text = ''.ljust(amount)


class NewLine(Segment):
    text = '\r\n'


class Root(Segment):
    text = '\\$ '


class Jobs(Segment):
    bg = colors.background(colors.MID_ORANGE)
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()
        pppid = Popen(['ps', '-p', str(getppid()), '-oppid='], stdout=PIPE).communicate()[0].strip()
        output = Popen(['ps', '-a', '-o', 'ppid'], stdout=PIPE).communicate()[0]
        num_jobs = len(findall(bytes(pppid), output)) - 1

        self.text = '{} {}'.format(glyphs.HOURGLASS, num_jobs)

        if not num_jobs:
            self.active = False


class ReadOnly(Segment):
    bg = colors.background(colors.LIGHT_GREY)
    fg = colors.foreground(colors.RED)

    def __init__(self, cwd):
        super().__init__()
        self.text = ' {} '.format(glyphs.LOCK)

        if access(cwd, W_OK):
            self.active = False


class ExitCode(Segment):
    bg = colors.background(colors.RED)
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()
        self.text = ' {} '.format(glyphs.CROSS)

        if argv[1] == '0':
            self.active = False


class Ssh(Segment):
    bg = colors.background(colors.LIGHT_ORANGE)
    fg = colors.foreground(colors.WHITE) + colors.bold()

    def __init__(self):
        super().__init__()
        self.text = 'SSH'

        if not getenv('SSH_CLIENT'):
            self.active = False


class Venv(Segment):
    bg = colors.background(colors.SMERALD)  # 161
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()

        env = getenv('VIRTUAL_ENV')
        if env is None:
            self.active = False
            return

        env_name = path.basename(env)
        self.text = '{} {}'.format(glyphs.VIRTUAL_ENV, env_name)


class Git(Segment):
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()

        branch_name = self.get_branch_name()

        if not branch_name:
            self.active = False
            return

        self.git_status_output = self.get_git_status_output()

        wd_glyph, bg_col = self.get_working_dir_status_decorations()
        self.bg = colors.background(bg_col)

        current_commit_text = self.get_current_commit_decoration_text()

        self.text = '{} {}{} {}'.format(
            wd_glyph,
            branch_name,
            glyphs.BRANCH,
            current_commit_text,
        )

    @staticmethod
    def get_branch_name():
        try:
            # See:
            # http://git-blame.blogspot.com/2013/06/checking-current-branch-programatically.html
            p = Popen(['git', 'symbolic-ref', '-q', 'HEAD'], stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()

            if 'not a git repo' in str(err).lower():
                raise FileNotFoundError
        except FileNotFoundError:
            return None

        return out.decode().replace('refs/heads/', '').strip() if out else '(Detached)'

    @staticmethod
    def get_git_status_output():
        return Popen(['git', 'status', '--ignore-submodules'],
                     env={"LANG": "C", "HOME": getenv("HOME")},
                     stdout=PIPE).communicate()[0].decode().lower()

    def get_working_dir_status_decorations(self):
        # Working directory statuses:
        UNTRACKED_FILES = 0
        CHANGES_NOT_STAGED = 1
        ALL_CHANGES_STAGED = 2
        CLEAN = 3
        UNKNOWN = 4

        # Statuses vs colors:
        STATUSES_BGCOLORS = {
            UNTRACKED_FILES: colors.LIGHT_RED,
            CHANGES_NOT_STAGED: colors.LIGHT_RED,
            ALL_CHANGES_STAGED: colors.LIGHT_ORANGE,
            CLEAN: colors.DARK_GREEN,
            UNKNOWN: colors.RED,
        }

        # Statuses vs glyphs:
        STATUSES_GLYPHS = {
            UNTRACKED_FILES: glyphs.RAINY,
            CHANGES_NOT_STAGED: glyphs.CLOUDY,
            ALL_CHANGES_STAGED: glyphs.SUNNY,
            CLEAN: '',
            UNKNOWN: '?',
        }

        if 'untracked files' in self.git_status_output:
            return STATUSES_GLYPHS[UNTRACKED_FILES], STATUSES_BGCOLORS[UNTRACKED_FILES]

        if 'changes not staged for commit' in self.git_status_output:
            return STATUSES_GLYPHS[CHANGES_NOT_STAGED], STATUSES_BGCOLORS[CHANGES_NOT_STAGED]

        if 'changes to be committed' in self.git_status_output:
            return STATUSES_GLYPHS[ALL_CHANGES_STAGED], STATUSES_BGCOLORS[ALL_CHANGES_STAGED]

        if 'nothing to commit' in self.git_status_output:
            return STATUSES_GLYPHS[CLEAN], STATUSES_BGCOLORS[CLEAN]

        return STATUSES_GLYPHS[UNKNOWN], STATUSES_BGCOLORS[UNKNOWN]

    def get_current_commit_decoration_text(self):
        DIRECTIONS_GLYPHS = {
            'ahead': glyphs.RIGHT_ARROW,
            'behind': glyphs.LEFT_ARROW,
        }

        match = findall(
            r'your branch is (ahead|behind).*?(\d+) commit', self.git_status_output)

        if not match:
            return ''

        direction = match[0][0]
        amount = match[0][1]
        amount = getattr(glyphs, 'N{}'.format(amount)) if int(amount) <= 10 else amount

        return '{}{} '.format(amount, DIRECTIONS_GLYPHS[direction]) if direction == 'ahead' else \
               '{}{} '.format(DIRECTIONS_GLYPHS[direction], amount)