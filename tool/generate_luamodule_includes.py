#!/usr/bin/python3
"""Generate the includes for LuaSocket pure-Lua modules."""
import util
util.ensure_project_root()

XXD = util.which("xxd")

LUASOCKET_MODULES = {
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

LUASEC_MODULES = {
	"ssl": "../ssl_patched.lua",
	"ssl.https": "src/https.lua"
}

INTERNAL_MODULES = {
	"tichttp": "tichttp.lua"
}

VARIABLE_NAMES = {}
MODULE_DUMPS = []

# LuaSocket modules
with util.chdir("src/luasocket"):
	for module, filename in LUASOCKET_MODULES.items():
		# socket.http = socket_http
		# socket = socket_lua
		variable_name = module.replace(".","_")
		if "." not in module:
			variable_name+="_lua"
		VARIABLE_NAMES[module] = variable_name
		output = util.call([XXD, "-i", "-n", variable_name, filename]).rstrip()
		MODULE_DUMPS.append(output)

# LuaSec modules
with util.chdir("src/luasec"):
	for module, filename in LUASEC_MODULES.items():
		variable_name = module.replace(".","_")
		if "." not in module:
			variable_name+="_lua"
		VARIABLE_NAMES[module] = variable_name
		output = util.call([XXD, "-i", "-n", variable_name, filename]).rstrip()
		MODULE_DUMPS.append(output)

# Internal modules
with util.chdir("src"):
	for module, filename in INTERNAL_MODULES.items():
		variable_name = module.replace(".","_")
		if "." not in module:
			variable_name+="_lua"
		VARIABLE_NAMES[module] = variable_name
		output = util.call([XXD, "-i", "-n", variable_name, filename]).rstrip()
		MODULE_DUMPS.append(output)

with open("src/lua_modules.h","w") as f:
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
