Configuration
=============
TODO: explain what config.py is, mention the 3 elements (theme, patched fonts, segments)

Themes
------
### Default
TODO: say that all screenshots in the Segments section are take with the default theme

### Light
TODO: screenshot

Patched fonts
-------------
TODO: explain what config.py is, post a screenshot with no patched fonts


Segments
========
Promptastic creates the *flavored* prompt appending several segments.
Any segment can be enabled/disabled via the `config.py` file.

The following section lists all the segments together with their details.

User at host
------------
The name of the logged user and the host name. In case the logged user is `root` the symbol `#`
is used.

![User at host segment](https://cloud.githubusercontent.com/assets/6423485/4515224/aa838794-4bb1-11e4-97c0-f2c559aef82e.png)

Time
----
The current time.

![Time segment](https://cloud.githubusercontent.com/assets/6423485/4515227/aa85510a-4bb1-11e4-9bb9-2037c55a3644.png)

Exit code
---------
A cross, only if the last command exited with a failure code.

![Exit code segment](https://cloud.githubusercontent.com/assets/6423485/4515222/aa76a920-4bb1-11e4-9a79-ec9da95a435e.png)

Current directory and read-only
-------------------------------
The path of the current directory. A padlock is added in case the logged user has no write 
permission on the directory. A warning message is shown in case the current directory is not a
valid path.

![Current directory and read-only segments](https://cloud.githubusercontent.com/assets/6423485/4515221/aa5afab8-4bb1-11e4-8fc2-b6d41e12e8fd.png)

Virtual environment
-------------------
The name of the active Python [virtualenv](https://github.com/pypa/virtualenv) environment, if any.

![Virtual environment segment](https://cloud.githubusercontent.com/assets/6423485/4515228/aa91c3fe-4bb1-11e4-917e-3ffd6fe6b96a.png)

Ssh
---
A special label in case the user is logged using a SSH connection.

![Ssh segment](https://cloud.githubusercontent.com/assets/6423485/4515223/aa836368-4bb1-11e4-9b5f-f9f0372d2ea4.png)

Active jobs
-----------
The number of active jobs, if any.

![Active jobs segment](https://cloud.githubusercontent.com/assets/6423485/4515225/aa83ca06-4bb1-11e4-9e5b-38dc60bdc625.png)

Git
---
If the current directory is a Git repository, the name of the current branch is displayed and:

- the color of the segment reveals the general status of the working directory:
  - *green* (e.g. 2nd prompt line in the screenshot) when the working directory is clean;
  - *pink* (e.g. 3rd prompt line in the screenshot) when the working directory is dirty (untracked
  files or changes not staged for commit);
  - *orange* (e.g. 4th prompt line in the screenshot) when all changes are staged for commit;
- glyphs are added to manifest detailed statuses:
  - an *umbrella* (e.g. 3rd prompt line in the screenshot) when there are untracked files;
  - a *cloud* (e.g. 5th prompt line in the screenshot) when there are changes not staged for
  commit, but no untracked files;
  - a *sun* (e.g. 4th prompt line in the screenshot) when all changes are staged for commit;
  - a *number n* plus a *arrow* right/left oriented (e.g. 6th and 8th prompt lines in the
  screenshot) when the current branch is *n* commits ahead/behind origin.

![Git segment](https://cloud.githubusercontent.com/assets/6423485/4515226/aa84c14a-4bb1-11e4-8ce3-a593e626aa55.png)