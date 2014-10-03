Configuration
=============
TODO: explain what if config.py and the themes
Explain the patched fonts, attach a screenshot with no patched fonts


Segments
========
Promptastic creates the *flavored* prompt appending several segments.
Any segment can be enabled/disabled via the `config.py` file.

The following section lists all the segments together with their details.

User at host
------------
The name of the logged user and the host name. In case the logged user is `root` the symbol `#`
is used.

TODO: screnshot

Time
----
The current time.

TODO: screnshot

Exit code
---------
A cross, only if the last command exited with a failure code.

TODO: screnshot

Current directory and read-only
-------------------------------
The path of the current directory. A padlock is added in case the logged user has no write 
permission on the directory. A warning message is shown in case the current directory is not a
valid path.

TODO: screnshot

Virtual environment
-------------------
The name of the active Python [virtualenv](https://github.com/pypa/virtualenv) environment, if any.

TODO: screnshot

Ssh
---
A special label in case the user is logged using a SSH connection.

TODO: screnshot

Active jobs
-----------
The number of active jobs, if any.

TODO: screnshot

Git
---
TODO