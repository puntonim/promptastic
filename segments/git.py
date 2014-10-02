import os
import re
import subprocess

from segments import Segment
from utils import colors, glyphs


class Git(Segment):
    def init(self):
        branch_name = self.get_branch_name()

        if not branch_name:
            self.active = False
            return

        self.git_status_output = self.get_git_status_output()

        wd_glyph, git_colors = self.get_working_dir_status_decorations()
        self.bg = colors.background(git_colors[0])
        self.fg = colors.foreground(git_colors[1])

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
            p = subprocess.Popen(['git', 'symbolic-ref', '-q', 'HEAD'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()

            if 'not a git repo' in str(err).lower():
                raise FileNotFoundError
        except FileNotFoundError:
            return None

        return out.decode().replace('refs/heads/', '').strip() if out else '(Detached)'

    @staticmethod
    def get_git_status_output():
        return subprocess.Popen(['git', 'status', '--ignore-submodules'],
                     env={"LANG": "C", "HOME": os.getenv("HOME")},
                     stdout=subprocess.PIPE).communicate()[0].decode().lower()

    def get_working_dir_status_decorations(self):
        # Working directory statuses:
        UNTRACKED_FILES = 0
        CHANGES_NOT_STAGED = 1
        ALL_CHANGES_STAGED = 2
        CLEAN = 3
        UNKNOWN = 4

        # Statuses vs colors:
        STATUSES_COLORS = {
            #STATUS: (bg_col, fg_col),
            UNTRACKED_FILES: (colors.PINKISH_RED, colors.NEARLY_WHITE_GREY),
            CHANGES_NOT_STAGED: (colors.PINKISH_RED, colors.NEARLY_WHITE_GREY),
            ALL_CHANGES_STAGED: (colors.LIGHT_ORANGE, colors.DARKER_GREY),
            CLEAN: (colors.PISTACHIO, colors.DARKER_GREY),
            UNKNOWN: (colors.RED, colors.WHITE),
        }

        # Statuses vs glyphs:
        STATUSES_GLYPHS = {
            #STATUS: glyph,
            UNTRACKED_FILES: glyphs.RAINY,
            CHANGES_NOT_STAGED: glyphs.CLOUDY,
            ALL_CHANGES_STAGED: glyphs.SUNNY,
            CLEAN: '',
            UNKNOWN: '?',
        }

        if 'untracked files' in self.git_status_output:
            return STATUSES_GLYPHS[UNTRACKED_FILES], STATUSES_COLORS[UNTRACKED_FILES]

        if 'changes not staged for commit' in self.git_status_output:
            return STATUSES_GLYPHS[CHANGES_NOT_STAGED], STATUSES_COLORS[CHANGES_NOT_STAGED]

        if 'changes to be committed' in self.git_status_output:
            return STATUSES_GLYPHS[ALL_CHANGES_STAGED], STATUSES_COLORS[ALL_CHANGES_STAGED]

        if 'nothing to commit' in self.git_status_output:
            return STATUSES_GLYPHS[CLEAN], STATUSES_COLORS[CLEAN]

        return STATUSES_GLYPHS[UNKNOWN], STATUSES_COLORS[UNKNOWN]

    def get_current_commit_decoration_text(self):
        DIRECTIONS_GLYPHS = {
            'ahead': glyphs.RIGHT_ARROW,
            'behind': glyphs.LEFT_ARROW,
        }

        match = re.findall(
            r'your branch is (ahead|behind).*?(\d+) commit', self.git_status_output)

        if not match:
            return ''

        direction = match[0][0]
        amount = match[0][1]
        amount = getattr(glyphs, 'N{}'.format(amount)) if int(amount) <= 10 else amount

        return '{}{} '.format(amount, DIRECTIONS_GLYPHS[direction]) if direction == 'ahead' else \
               '{}{} '.format(DIRECTIONS_GLYPHS[direction], amount)