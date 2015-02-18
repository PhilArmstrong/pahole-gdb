pahole for gdb
==============

Put the two python scripts somewhere handy, then copy gdbinit to
~/.gdbinit (or add the python scripts to your existing gdbinit) after
editing the python include path in your ~/.gdbinit to add the
directory where you installed the python scripts.

Then invoke gdb on your compiled binary and check the offsets of your
C++ or C classes and structs like so:

```
$ gdb test-cxx
GNU gdb (Debian 7.7.1+dfsg-5) 7.7.1
...
Reading symbols from test-cxx...done.
(gdb) pahole C
/*   16     */ struct C {
/*   0    4 */      int i
/*   4    1 */      char j
/* XXX 24 bit hole, try to pack */
/*   8    8 */      void * l
}
(gdb) quit
```
