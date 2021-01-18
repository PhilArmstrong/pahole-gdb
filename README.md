pahole for gdb
==============

I believe this code ships with gdb in Fedora, but Debian doesn’t seem
to include it for some reason.

Put the two python scripts somewhere handy, then copy gdbinit to
~/.gdbinit (or add the python scripts to your existing gdbinit) after
editing the python include path in your ~/.gdbinit to add the
directory where you installed the python scripts.

Then invoke gdb on your compiled binary and check the offsets of your
C++ or C classes and structs like so:

```
$ gdb test-pahole
GNU gdb (Debian 10.1-1.7) 10.1.90.20210103-git
...
Reading symbols from test-pahole...
(gdb) pahole C
/*   16     */ struct C {
/*   0    4 */    int i
/*   4    1 */    char j
/* XXX    3 */ !! char [3] __24_bit_padding__
/*   8    8 */    void * l
              } 
(gdb)
```

Python compatibility
--------------------

The script should work on both gdb using Python 2 (gdb versions <7.8 IIRC) and Python 3.
