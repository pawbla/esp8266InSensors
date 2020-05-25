import json
import esp

class SysInfo():

	def __init__(self):
		self.apiPath = "sysinfo"
		self.sysVersion = "1.0"

	def getApiPath(self):
		return self.apiPath

	def getMessage(self):
		""" This method is paring a measured values into json format """
		print("Prepare message for measurements")

		header = "HTTP/1.1 200 OK\nContent-Type: application/json\r\n\n"
		html1 = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body>"""
		html2 = """</body>
</html>
"""
		msg = json.dumps({"version" : self.sysVersion, "flashSize:": str(esp.flash_size())})
		return header + msg