local http = require"socket.http"
local https = require"ssl.https"

function http.schemes.https.create(t)
	if t.verify and t.verify~="none" and not (t.cafile or t.capath) then
		t.cadata = require"tichttp.cabundle"
	end
	return https.tcp(t)
end

return http
