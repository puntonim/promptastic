from __future__ import print_function
# Python 2 and 3 compatibility: FileNotFoundError in Python 3, IOError in Python 2.
FileNotFoundError = getattr(__builtins__, 'FileNotFoundError', IOError)
input = getattr(__builtins__, 'raw_input', input)

import os
import re
import subprocess

from segments import Segment, theme
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
        self.text = wd_glyph + ' ' + branch_name + glyphs.BRANCH + ' ' + current_commit_text

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
        out, err = subprocess.Popen(['git', 'status', '--ignore-submodules'],
                                    env={"LANG": "C", "HOME": os.getenv("HOME")},
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if err:
            return ''  # An empty text as something went wrong so we cannot determine the
                       # current git status (it happens f.i. when cd-ing into .git folder).
        return out.decode().lower()

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
            UNTRACKED_FILES: (theme.GIT_UNTRACKED_FILES_BG, theme.GIT_UNTRACKED_FILES_FG),
            CHANGES_NOT_STAGED: (theme.GIT_CHANGES_NOT_STAGED_BG, theme.GIT_CHANGES_NOT_STAGED_FG),
            ALL_CHANGES_STAGED: (theme.GIT_ALL_CHANGES_STAGED_BG, theme.GIT_ALL_CHANGES_STAGED_FG),
            CLEAN: (theme.GIT_CLEAN_BG, theme.GIT_CLEAN_FG),
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

        return amount + DIRECTIONS_GLYPHS[direction] + ' ' if direction == 'ahead' else \
               DIRECTIONS_GLYPHS[direction] + amount + ' '
