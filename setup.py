# In order to install this new prompt we have to add a few lines at those files source every time
# a Bash shell is invokes.
# Two are the files we need to edit, as explained here:
# http://mywiki.wooledge.org/DotFiles
# Every time a Bash shell is invoked, the file `~/.bash_profile` is read, if it exists.
# While the file `~/.bashrc` is read when a subshell is invoked with a command like `bash`.


# Read the files ~/.bash_profile and ~/.bashrc.
# Check if the text `function _update_ps1() { .* }` is included:
# if not: add it; else: if it is different from our text, comment it out and add it.
#function _update_ps1() {
#   export PS1="$(~/workspace/promptastic/promptastic.py $?)"
#}
#
# Check if the text `export PROMPT_COMMAND` is included:
# if not: add it; else: if it is different from our text, comment it out and add it.
#export PROMPT_COMMAND="_update_ps1"

