# Data Files for Inject Buttons in NodeRED

## Usage

The files are usually taken from real data and may contain placeholders in python format
string syntax: '%(myplaceholder)s'.

Those are looked up in `variables.py, class Variables`, within the same directory then the data files.

When defined as function, it will be called, e.g. `%(time)s` and `def time(): return time.time()` defined.

When not cached (parameter for file read operator), changed to either file, data and
variables are loaded at every inject - w/o the need to restart the worker.

## Mechanics
The inject buttons declare the filename, and the file read operator will read the file,
then replace the variables.


## Add more

You can define arbitrary values as placeholders, using '%(myval)s' format, then add the
value to the variables file.



