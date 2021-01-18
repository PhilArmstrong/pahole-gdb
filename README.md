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

``` plain
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

(gdb) pahole testStruct
/*  152     */ struct testStruct {
/*   0    2 */     short a
/*   2    1 */     char b
/* XXX    5 */ !!  char [5] __40_bit_padding__
/*   8  144 */     testStruct::more_struct more
               } testStruct
```

When specifying `walk` right after the type name, `pahole` will walk your object recursively and reveal the content of nested `struct`s and `union`s:

``` plain
(gdb) pahole testStruct walk
/*  152     */ struct testStruct {
/*   0    2 */     short a
/*   2    1 */     char b
/* XXX    5 */ !!  char [5] __40_bit_padding__
/*   8  144 */     struct testStruct::more_struct {
/*   0  128 */       union testStruct::more_struct::union_x {
/*   0  128 */         char [128] c
/*   0    2 */         struct testStruct::more_struct::union_x::s_y {
/*   0    1 */           char v
/*   1    0 */           char g1_1:7
/* XXX    1 */ !!        char [1] __1_bit_padding__
                     } y
/* XXX 1008 */ !!      char [126] __1008_bit_padding__
                   } x
/* 128    8 */       long e
/* 136    0 */       char s1_1:1
/* 136    0 */       char s1_2:1
/* 136    0 */       char s2:2
/* XXX   60 */ !!    char [8] __60_bit_padding__
                 } more
               } testStruct
```

Python compatibility
--------------------

The script should work on both gdb using Python 2 (gdb versions <7.8 IIRC) and Python 3.
