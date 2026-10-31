#!/usr/bin/python3
"""Patch ssl.lua to remove get_system_ca check.

LuaSec, by default, tries to find a system certificate bundle on load. It does
this by attempting to open a handful of "expected" certificate bundle locations
using the io library.

TIC-80 doesn't provide the io library by default. While we theoretically could
provide the io library for users of this core, I think it makes more sense to
just disable this functionality. (It doesn't even work on Windows computers
anyways, since Windows does things its own weird Microsoft-y way.) I even ship
a certificate bundle with the core, which lets me side-step the issue...

...except I forgot to update the special ssl_patched.lua to handle the
load-from-string functionality I added in my LuaSec fork/PR.

So this script does the patching automagically, and I can remember to run this
script whenever I run into odd situations."""
import util
import sys
util.ensure_project_root()

with open("src/luasec/src/ssl.lua","r") as f:
	ssl_lua = f.read().splitlines()

# remove the auto-detection block
TARGET = "-- System CA auto-detection"
END_TARGET = "local function newcontext(cfg)"
try:
	start_idx = ssl_lua.index(TARGET)
	end_idx = ssl_lua.index(END_TARGET)
	# also remove the divider line behind the "target" line
	del ssl_lua[start_idx-1:end_idx]
except ValueError:
	print("Error: can't find CA autodetection block",file=sys.stderr)
	sys.exit(1)
# and the exported system_ca methods too
WRAP = "  wrap            = wrap,"
while ssl_lua[-1]!=WRAP:
	ssl_lua.pop()
ssl_lua.extend("""}

return _M""".splitlines())

with open("src/ssl_patched.lua","w") as f:
	f.write("\n".join(ssl_lua)+"\n")
