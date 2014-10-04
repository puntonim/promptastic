Configuration
=============
*Promptastic* can be customized by editing the file `config.py`. This file contains 3 elements:
**theme**, **patched fonts flag**, **segments**. 

Themes
------
Themes determine the set of colors used in the prompt. There are a bunch of themes already
stored in the `themes` folder. New themes can be easily created copying one of those
already existent.

### Default theme: `default.py`
It's a dark-colors theme, best fitting a terminal with a dark background.
All screenshots in the next sections are based on this theme. It's my favorite!

### Light theme: `light.py`
It's a light-colors theme, best fitting a terminal with a light background, like the default
*Terminal* app in Mac OS X.

![Light theme](https://cloud.githubusercontent.com/assets/6423485/4515595/ab434f92-4bc6-11e4-92d4-25f7a23aa659.png)

Patched fonts
-------------
[Patched powerline-fonts](https://github.com/Lokaltog/powerline-fonts) can be used for
better-looking glyphs. My favorite is
[Sauce Code Powerline Light](https://github.com/Lokaltog/powerline-fonts/tree/master/SourceCodePro)
. See [INSTALL.md](https://github.com/nimiq/promptastic/blob/master/INSTALL.md) in order to
install patched fonts.      
All screenshots in the next sections were taken in terminals using *Sauce Code Powerline Light*
patched font. A terminal with no patched fonts looks like this:

![No patched fonts](https://cloud.githubusercontent.com/assets/6423485/4515599/b449a384-4bc6-11e4-8992-ed7ef91c6210.png)


Segments
========
*Promptastic* creates the *flavored* prompt appending several segments.
Any segment can be enabled/disabled in the `config.py` file.

The following sections list all the segments and their .

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