from subprocess import Popen, PIPE
from os import getppid
from re import findall
from datetime import datetime
from getpass import getuser
from socket import gethostname

from segments import Segment
import colors
import glyphs


class Jobs(Segment):
    bg = colors.background(colors.DARK_PURPLE)
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()
        pppid = Popen(['ps', '-p', str(getppid()), '-oppid='], stdout=PIPE).communicate()[0].strip()
        output = Popen(['ps', '-a', '-o', 'ppid'], stdout=PIPE).communicate()[0]
        num_jobs = len(findall(bytes(pppid), output)) - 1

        self.text = '{} {}'.format(glyphs.HOURGLASS, num_jobs)

        if not num_jobs:
            self.active = False

    # The following code is an alternative way to get the number of jobs by reading `/proc` folder.
    # It works only on linux (no Mac OS) and it has better performance making it especially
    # suitable for old machines.
    # Source: https://github.com/milkbikis/powerline-shell/issues/117
    #
    # myppid = os.getppid()
    # count_jobs = {}
    # process_pid = -1
    #
    # for f in os.listdir('/proc'):
    #     pathname = os.path.join('/proc', f)
    #     fstat = os.stat(pathname)
    #
    #     if fstat.st_uid != os.getuid():
    #         continue
    #
    #     if S_ISDIR(fstat.st_mode):
    #         statfile = os.path.join(pathname, 'stat')
    #         if os.path.isfile(statfile):
    #             with open(statfile) as f:
    #                 statline = f.readline()
    #                 fields   = statline.split()
    #                 if len(fields) >= 3:
    #                     process_pid  = fields[0]
    #                     process_ppid = fields[3]
    #
    #                     if process_pid == str(myppid):
    #                        process_pid = process_ppid
    #
    #                     if count_jobs.has_key(process_ppid):
    #                        count_jobs[process_ppid] += 1
    #                     else:
    #                        count_jobs[process_ppid]  = 1
    #
    # num_jobs = count_jobs[str(process_pid)] - 1


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


class UserAtHost(Segment):
    bg = colors.background(colors.SMERALD)
    fg = colors.foreground(colors.WHITE)

    def __init__(self):
        super().__init__()
        self.text = '{}@{}'.format(
            getuser(),
            gethostname().replace('.local', '')
        )