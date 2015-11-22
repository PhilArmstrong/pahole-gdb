from __future__ import print_function
import gdb

class Offsets(gdb.Command):
    def __init__(self):
        super (Offsets, self).__init__ ('offsets-of', gdb.COMMAND_DATA, gdb.COMPLETE_SYMBOL)

    def invoke(self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        if len(argv) != 1:
            raise gdb.GdbError('offsets-of takes exactly 1 argument.')

        stype = gdb.lookup_type(argv[0])

        print (argv[0], '{')
        for field in stype.fields():
            print ('    %s => %d' % (field.name, field.bitpos//8))
        print ('}')

Offsets()
