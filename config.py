# This is the configuration file which helps you customize your 'promptastic' installation.
# For instructions on how to use the promptastic.py script, see the README.

# The theme defines the colors used to draw individual segments.
# Themes are collected in the `themes` directory. Their names match their file name.
THEME = 'default'

# Segments are the single elements which compose the Bash shell prompt.
# Enable or disable these segments to customize what you see on the shell prompt.
SEGMENTS = {
    # Current user's username plus @ plus machine's hostname.
    'userathost': True,

    # SSH tag when ssh-ing from another machine.
    'ssh': True,

    # Current directory path.
    'currentdir': True,

    # A padlock if the current user has read-only permissions on the current directory.
    'readonly': True,

    # A cross if the last command exited with a non-zero exit code.
    'exitcode': True,

    # Current git branch and status when the current directory is part of a git repo.
    'git': True,

    # Name of the current virtual environment (see http://www.virtualenv.org/), if any.
    'venv': True,

    # Number of running jobs, if any.
    'jobs': True,

    # Current time.
    'time': True,
}
