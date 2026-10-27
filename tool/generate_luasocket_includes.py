#!/usr/bin/python3
"""Generate the includes for LuaSocket pure-Lua modules."""
import os, subprocess

XXD = subprocess.check_output("which xxd", shell=True).decode("ascii").strip()

MODULES = {
	"socket.http": "src/http.lua",
	"socket.url": "src/url.lua",
	"socket.tp": "src/tp.lua",
	"socket.ftp": "src/ftp.lua",
	"socket.headers": "src/headers.lua",
	"socket.smtp": "src/smtp.lua",
	"ltn12": "src/ltn12.lua",
	"socket": "src/socket.lua",
	"mbox": "src/mbox.lua",
	"mime": "src/mime.lua"
}

VARIABLE_NAMES = {}
MODULE_DUMPS = []

os.chdir("src/luasocket")
for module, filename in MODULES.items():
	# socket.http = socket_http
	# socket = socket_lua
	variable_name = module.replace(".","_")
	if "." not in module:
		variable_name+="_lua"
	VARIABLE_NAMES[module] = variable_name
	output = subprocess.check_output([XXD, "-i", "-n", variable_name, filename]).decode("ascii").rstrip()
	MODULE_DUMPS.append(output)
os.chdir("..") # back to src
with open("lua_modules.h","w") as f:
	for module_dump in MODULE_DUMPS:
		f.write(module_dump)
		f.write("\n\n")
	f.write("#define PRELOAD_ALL_MODULES (")
	s = ""
	for module, variable_name in VARIABLE_NAMES.items():
		s += f" preload_lua(lua, \"{module}\", {variable_name}, {variable_name}_len) && \\\n"
	s = s[1:-6]
	f.write(s)
	f.write(")\n")
