# TIC-80 Lua HTTP core

A Lua core for TIC-80's dynamic script runtime system, with LuaSocket included.

## How to build

Clone this repository next to TIC-80, and use cmake to build it. You should get a `luahttp.dll` (or `.dylib` or `.so`, depending on platform).

You can then toss the shared library into the same directory as the TIC-80 binary and create a lua cart with `-- script: luahttp`, and you should be able to `require` the LuaSocket libraries.
