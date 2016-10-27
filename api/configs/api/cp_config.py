conf = {
	"global": {
		"server.socket_host": "0.0.0.0",#"72.231.30.212",
		"server.socket_port": 548,

		# Remove this to auto-reload code on change and output logs
		# directly to the console (dev mode).
		# "environment": "production",
	},
	"/": {
		"tools.sessions.on"             : True,
		"tools.sessions.timeout"        : 60,
		"tools.response_headers.on"     : True,
		"tools.sessions.storage_type"   : "file",
		"tools.sessions.storage_path"   : "C:/Users/Admin/Desktop/Folders/apps/bidavision/sessions",
		"tools.response_headers.headers": [
			(
				"Content-Type", 
				"application/json"
			)
		],
	}
}