Installation
============

Requirements
------------
- Mac OS X or Linux  
Promptastic is mainly developed for Mac OS X but it works smoothly under Linux too.
- Python 3+  
- A terminal with support for ANSI colors  
Promptastic uses [ANSI color codes](http://en.wikipedia.org/wiki/ANSI_escape_code)
to display colors in Bash terminals. These are notoriously non-portable, so may not work 
out of the box. *Terminal* and [*iTerm2*](http://iterm2.com) perfectly work in Mac OS X
by setting the terminal as `xterm-256color`.
- *Optional* - Patched fonts for better-looking glyphs  
Install patched [powerline-fonts](https://github.com/Lokaltog/powerline-fonts) and set the 
terminal to use them. My favorite is
[Sauce Code Powerline Light](https://github.com/Lokaltog/powerline-fonts/tree/master/SourceCodePro)
.

Steps
-----
1. Clone this repository:

        git clone https://github.com/nimiq/promptastic.git
2. Run:

        ./install.py
3. *Optional* - Edit the file `config.py`, in particular:
    - set `PATCHED_FONTS` to `False` if you are not using patched fonts;
    - set `THEME` to your favorite theme or create a new one copying one of the existent themes;
    - enable/disable segments.
4. Logout and login again in the shell to see the new prompt!