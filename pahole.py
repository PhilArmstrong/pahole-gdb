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

from __future__ import print_function
import gdb
import gdb.types
import math

class Pahole (gdb.Command):
    """Show the holes in a structure.
This command takes a single argument, a type name.
It prints the type and displays comments showing where holes are."""

    def __init__ (self):
        super (Pahole, self).__init__ ("pahole", gdb.COMMAND_DATA,
                                       gdb.COMPLETE_SYMBOL)

    def pahole (self, atype, level, name, walk=False, nested=False):
        if name is None:
            name = ''
        tag = atype.tag
        if tag is None:
            tag = ''
        kind = 'struct' if atype.code == gdb.TYPE_CODE_STRUCT else 'union'
        if nested == False:
            print ('/* %4d     */ ' % atype.sizeof, end="")
        print ('%s%s %s {' % ( ' ' * (2 * level), kind, tag))
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
                print ('/* XXX %4d */ !!' % (hole // 8), end="")
                print (' ' * (4 + 2 * level - 2), end="")
                print ('__%d_bit_padding__' % hole)

            # Are we a bitfield?
            if field.bitsize > 0:
                fieldsize = field.bitsize
            else:
                if (ftype.code == gdb.TYPE_CODE_STRUCT or ftype.code == gdb.TYPE_CODE_UNION) and len(ftype.fields()) == 0:
                    fieldsize = 0 # empty struct
                else:
                    fieldsize = 8 * ftype.sizeof # will get packing wrong for structs

            print ('/* %3d %4d */ ' % (field.bitpos // 8, fieldsize // 8), end="")
            endpos = field.bitpos + fieldsize

            # Walk nested structure or print variable size (this is not a hole)
            if walk == True and (ftype.code == gdb.TYPE_CODE_STRUCT or ftype.code == gdb.TYPE_CODE_UNION):
                print ('  ', end="")
                self.pahole (ftype, level + 1, field.name, walk=walk, nested=True)
            else:
                print (' ' * (4 + 2 * level), end="")
                print ('%s %s' % (str (ftype), field.name),end="")
                # Append bitfield size if non-standard
                if fieldsize != ftype.sizeof * 8:
                    print (':%d' % fieldsize)
                else:
                    print ('')

        # Check for padding at the end
        if endpos // 8 < atype.sizeof:
            hole = 8 * atype.sizeof - endpos
            print ('/* XXX %4d */ !!' % (hole // 8), end="")
            print (' ' * (4 + 2 * level - 2), end="")
            print ('__%d_bit_padding__' % hole)

        print (' ' * (14 + 2 * level), end="")
        print (' } %s' % name)

    def invoke (self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        if len(argv) > 2:
            raise gdb.GdbError('pahole takes a type name and an optional "walk" argument.')
        stype = gdb.lookup_type (argv[0])
        ptype = stype.strip_typedefs()
        if ptype.code != gdb.TYPE_CODE_STRUCT and ptype.code != gdb.TYPE_CODE_UNION:
            raise gdb.GdbError('%s is not a struct/union type: %s' % (arg, ptype.code))

        # Should the entire object be walked recursively?
        walk = len(argv) > 1 and argv[1] == "walk"

        self.pahole (ptype, 0, argv[0], walk=walk)

Pahole()
