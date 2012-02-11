# Jobtpl: A set of templating tools for generating and submitting Torque jobs

This project contains a set of Python and shell scripts for generating and managing
[Torque](http://en.wikipedia.org/wiki/TORQUE_Resource_Manager) job files.  Their
main focus is on [Gaussian 09](http://www.gaussian.com/) calculations, but the 
general approach is broadly applicable. 

The Python scripts to not use any modules outside of the core distribution as they
are intended to run on a broad variety of environments.  The scripts have been
used with Python 2.4 - 2.7.

## Python Scripts

The two Python scripts, `dihed.py` and `irc.py`, create job files for performing dihedral
rotation and following internal reaction coordinates, respectively.  This involves making
copies of a single Gaussian 09 frequency calculation checkpoint  file and creating the 
appropriate Gaussian 09 com files and Torque job files.

The com and job files are created based on template files.  `dihed.py` uses `comtpl` and 
`jobtpl` for its default com and job templates.  `irc.py` uses `irccomtpl` and `jobtpl` for
its defaults.  The template syntax is the built-in [Python template string style]
(http://docs.python.org/library/string.html#template-strings).

Both scripts use Python's [OptionParser](http://docs.python.org/library/optparse.html) 
library for parsing command-line options.  The `-h` option will print a usage
description message. 

## Shell Scripts

The shell scripts are intended as examples of basic shell loops.  `run.sh` loops through
the output of an `ls` command and `range.sh` loops through a given range of
integers.  I do not know how recent `bash`s addition of the C-style `for` loop is, so
`range.sh` may not work in older environments.