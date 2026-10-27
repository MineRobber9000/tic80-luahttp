cmake_minimum_required(VERSION 3.12)
project(tic80-core-luahttp VERSION 0.1.0 LANGUAGES C CXX)

# I copied these from TIC-80 itself just in case it matters
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
set(CMAKE_C_FLAGS_RELEASE "-O2 -flto -ffat-lto-objects ${CMAKE_C_FLAGS_RELEASE}")
set(CMAKE_CXX_FLAGS_RELEASE "-O2 -flto -ffat-lto-objects ${CMAKE_CXX_FLAGS_RELEASE}")
endif()

if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang"  OR CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
set(CMAKE_C_FLAGS_RELEASE "-O2 -flto ${CMAKE_C_FLAGS_RELEASE}")
set(CMAKE_CXX_FLAGS_RELEASE "-O2 -flto ${CMAKE_CXX_FLAGS_RELEASE}")
endif()

if(APPLE)
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.15" CACHE STRING "Minimum OS X deployment version")
endif()

set(LUA_DIR "${CMAKE_SOURCE_DIR}/src/lua-5.3.6/src")
add_library(lua STATIC
	${LUA_DIR}/lapi.c
	${LUA_DIR}/lauxlib.c
	${LUA_DIR}/lbaselib.c
	${LUA_DIR}/lbitlib.c
	${LUA_DIR}/lcode.c
	${LUA_DIR}/lcorolib.c
	${LUA_DIR}/lctype.c
	${LUA_DIR}/ldblib.c
	${LUA_DIR}/ldebug.c
	${LUA_DIR}/ldo.c
	${LUA_DIR}/ldump.c
	${LUA_DIR}/lfunc.c
	${LUA_DIR}/lgc.c
	${LUA_DIR}/linit.c
	${LUA_DIR}/liolib.c
	${LUA_DIR}/llex.c
	${LUA_DIR}/lmathlib.c
	${LUA_DIR}/lmem.c
	${LUA_DIR}/loadlib.c
	${LUA_DIR}/lobject.c
	${LUA_DIR}/lopcodes.c
	${LUA_DIR}/loslib.c
	${LUA_DIR}/lparser.c
	${LUA_DIR}/lstate.c
	${LUA_DIR}/lstring.c
	${LUA_DIR}/lstrlib.c
	${LUA_DIR}/ltable.c
	${LUA_DIR}/ltablib.c
	${LUA_DIR}/ltm.c
	${LUA_DIR}/lundump.c
	${LUA_DIR}/lutf8lib.c
	${LUA_DIR}/lvm.c
	${LUA_DIR}/lzio.c)
target_include_directories(lua PUBLIC
	${LUA_DIR})
target_compile_options(lua PRIVATE "-fPIC")

set(LUASOCKET_DIR "${CMAKE_SOURCE_DIR}/src/luasocket/src")
add_library(luasocket STATIC
	# socket.core
	${LUASOCKET_DIR}/luasocket.c
	${LUASOCKET_DIR}/timeout.c
	${LUASOCKET_DIR}/buffer.c
	${LUASOCKET_DIR}/io.c
	${LUASOCKET_DIR}/auxiliar.c
	${LUASOCKET_DIR}/options.c
	${LUASOCKET_DIR}/inet.c
	${LUASOCKET_DIR}/except.c
	${LUASOCKET_DIR}/select.c
	${LUASOCKET_DIR}/tcp.c
	${LUASOCKET_DIR}/udp.c
	${LUASOCKET_DIR}/compat.c
	# mime.core
	${LUASOCKET_DIR}/mime.c)
target_compile_definitions(luasocket PRIVATE LUASOCKET_DEBUG)
if(LINUX OR APPLE)
	target_sources(luasocket PRIVATE
		# add usocket.c
		${LUASOCKET_DIR}/usocket.c
		# socket.unix
		${LUASOCKET_DIR}/buffer.c
		${LUASOCKET_DIR}/compat.c
		${LUASOCKET_DIR}/auxiliar.c
		${LUASOCKET_DIR}/options.c
		${LUASOCKET_DIR}/timeout.c
		${LUASOCKET_DIR}/io.c
		${LUASOCKET_DIR}/usocket.c
		${LUASOCKET_DIR}/unix.c
		${LUASOCKET_DIR}/unixdgram.c
		${LUASOCKET_DIR}/unixstream.c
		# socket.serial
		${LUASOCKET_DIR}/buffer.c
		${LUASOCKET_DIR}/compat.c
		${LUASOCKET_DIR}/auxiliar.c
		${LUASOCKET_DIR}/options.c
		${LUASOCKET_DIR}/timeout.c
		${LUASOCKET_DIR}/io.c
		${LUASOCKET_DIR}/usocket.c
		${LUASOCKET_DIR}/serial.c
	)
	if(APPLE)
		target_compile_definitions(luasocket PRIVATE UNIX_HAS_SUN_LEN)
	endif()
	target_compile_definitions(luasocket PUBLIC LUASOCKET_IS_UNIX)
endif()
if(WIN32)
	# add wsocket.c to socket.core
	target_sources(luasocket PRIVATE ${LUASOCKET_DIR}/wsocket.c)
	target_link_libraries(luasocket PRIVATE ws2_32)
	target_compile_definitions(luasocket PRIVATE NDEBUG)
endif()
target_include_directories(luasocket PUBLIC
	${LUASOCKET_DIR})
target_link_libraries(luasocket PUBLIC lua)
target_compile_options(luasocket PRIVATE "-fPIC")

set(LUASEC_DIR "${CMAKE_SOURCE_DIR}/src/luasec/src")
add_library(luasec STATIC
	${LUASEC_DIR}/options.c
	${LUASEC_DIR}/config.c
	${LUASEC_DIR}/ec.c
	${LUASEC_DIR}/x509.c
	${LUASEC_DIR}/context.c
	${LUASEC_DIR}/ssl.c
	${LUASEC_DIR}/luasocket/buffer.c
	${LUASEC_DIR}/luasocket/io.c
	${LUASEC_DIR}/luasocket/timeout.c)
find_package(OpenSSL REQUIRED)
target_link_libraries(luasec PRIVATE OpenSSL::SSL OpenSSL::Crypto lua luasocket)
target_compile_definitions(luasec PRIVATE WITH_LUASOCKET LUASOCKET_DEBUG OPENSSL_API_COMPAT=0x10101000L)
if(LINUX OR APPLE)
	target_sources(luasocket PRIVATE
		# add usocket.c
		${LUASEC_DIR}/luasocket/usocket.c
	)
endif()
if(WIN32)
	# add wsocket.c to socket.core
	target_sources(luasec PRIVATE ${LUASEC_DIR}/luasocket/wsocket.c)
	target_link_libraries(luasec PRIVATE ws2_32)
	target_compile_definitions(luasec PRIVATE "WIN32" "NDEBUG" "_WINDOWS" "_USRDLL" "LSEC_EXPORTS" "BUFFER_DEBUG" "LSEC_API=__declspec(dllexport)"
                  "LUASEC_INET_NTOP" "WINVER=0x0501" "_WIN32_WINNT=0x0501" "NTDDI_VERSION=0x05010300")
endif()
target_include_directories(luasec PRIVATE
	${LUASEC_DIR}
	${LUASEC_DIR}/luasocket)

set(TIC80_DIR "${CMAKE_SOURCE_DIR}/../TIC-80")

add_library(luahttp SHARED
	${TIC80_DIR}/src/api/parse_note.c
	${TIC80_DIR}/src/api/luaapi.c
	${CMAKE_SOURCE_DIR}/src/main.c)
target_include_directories(luahttp PRIVATE
	${CMAKE_SOURCE_DIR}/src
	${TIC80_DIR}/include
	${TIC80_DIR}/src
	${TIC80_DIR}/src/api
)
target_link_libraries(luahttp PRIVATE lua luasocket luasec)
set_target_properties(luahttp PROPERTIES
	PREFIX "")
# If you want textri/OVR stuff:
# target_compile_definitions(luahttp PRIVATE BUILD_DEPRECATED)
