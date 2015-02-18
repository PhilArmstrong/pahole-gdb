#
# C++ related beautifiers (optional)
#

set print pretty on
set print object on
set print static-members on
set print vtbl on
set print demangle on
set demangle-style gnu-v3
set print sevenbit-strings off
set python print-stack full

python
sys.path.insert(0, '/home/phil/bin')
import offsets
import pahole
end
