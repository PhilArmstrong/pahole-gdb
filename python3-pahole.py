# pahole command for gdb

# Copyright (C) 2008 Free Software Foundation, Inc.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gdb
import gdb.types

class Pahole (gdb.Command):
    """Show the holes in a structure.
This command takes a single argument, a type name.
It prints the type and displays comments showing where holes are."""

    def __init__ (self):
        super (Pahole, self).__init__ ("pahole", gdb.COMMAND_DATA,
                                       gdb.COMPLETE_SYMBOL)

    def pahole (self, atype, level, name):
        if name is None:
            name = ''
        tag = atype.tag
        if tag is None:
            tag = ''
        print ('/* %4d     */ %sstruct %s {' % (atype.strip_typedefs().sizeof, ' ' * (2 * level), tag))
        endpos = 0
        for field in atype.fields():
            # Skip static fields
            if not hasattr (field, ('bitpos')):
                continue
            # find the type
            ftype = field.type.strip_typedefs()

            # Detect hole
            if endpos < field.bitpos:
                hole = field.bitpos - endpos
                print ('/* XXX %d bit hole, try to pack */' % hole)

            # Are we a bitfield?
            if field.bitsize > 0:
                fieldsize = field.bitsize
            else:
                if ftype.code == gdb.TYPE_CODE_STRUCT and len(ftype.fields()) == 0:
                    fieldsize = 0 # empty struct
                else:
                    fieldsize = 8 * ftype.sizeof # will get packing wrong for structs

            print ('/* %3d %4d */' % (field.bitpos // 8, fieldsize // 8), end="")
            endpos = field.bitpos + fieldsize

#            if ftype.code == gdb.TYPE_CODE_STRUCT:
#                self.pahole (ftype, level + 1, field.name)
#            else:
            print (' ' * (4 + 2 * level), end="")
            print ('%s %s' % (str (ftype), field.name))

        print (' ' * (14 + 2 * level), end="")
        print ('} %s' % name)

    def invoke (self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        if len(argv) > 2:
            raise gdb.GdbError('pahole takes 1 arguments.')
        stype = gdb.lookup_type (argv[0])
        ptype = stype.strip_typedefs()
        if ptype.code != gdb.TYPE_CODE_STRUCT:
            raise '%s is not a struct type' % arg
        self.pahole (ptype, 0, '')

Pahole()
