import ure
import authentication as Auth

class Rest_API():

	def __init__(self, conf, dht, sysInfo):
		self.dht = dht
		self.sysInfo = sysInfo
		self.api_ver = "1"
		self.authentication = Auth.Authentication(conf.getAccPassword()) 

	def process(self, reader, writer):
		print("Process received datas")
		response = self.prepareApiResponse((yield from reader.read()))
		yield from writer.awrite(response)
		yield from writer.aclose()

	def prepareApiResponse(self, read):
		print("Prepare response")
		path = ""
		if not self.authentication.authenticate(read):
			return self.authentication.message()
		parsed = ure.search(b'GET\\s/api/v' + self.api_ver + '/([A-Za-z0-9\\.]*)\\sHTTP', read)
		if parsed is None:
			return self.returnBadRequest()
		if parsed.group(1).decode("utf-8") != "/favicon.ico":
			path = parsed.group(1).decode("utf-8")
			return self.switchToApi(path)
		if parsed.group(1).decode("utf-8") == "/favicon.ico":
			path = parsed.group(1).decode("utf-8")
			return ""

	def switchToApi(self, path):
		print("Switch to API")
		if path == self.dht.getApiPath():
			resp = self.dht.getMessage();
		elif self.sysInfo.getApiPath():
			resp = self.sysInfo.getMessage();
		else:
			resp = self.returnNotFound()
		return resp

	def returnBadRequest(self):
		return "HTTP/1.1 400 Bad Request\n\n"

	def returnNotFound(self):
		return "HTTP/1.1 404 Not Found\n\n"