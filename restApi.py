import ure
import authentication as Auth

class Rest_API():

	def __init__(self, conf, dht):
		self.dht = dht
		self.api_ver = "1"
		self.aa = "aaa"
		self.authentication = Auth.Authentication(conf.getAccPassword()) 
		# DOROBIĆ AUTHENTYKACJĘ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	def process(self, reader, writer):
		print("Process received datas")
		response = self.prepareApiResponse((yield from reader.read()))
		yield from writer.awrite(response)
		yield from writer.aclose()

	def prepareApiResponse(self, read):
		print("Prepare response")
		path = ""
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
		print("Api " + self.dht.getApiPath())
		if path == self.dht.getApiPath():
			resp = self.dht.getMessage();
		else:
			resp = self.returnNotFound()
		return resp

	def returnBadRequest(self):
		return "HTTP/1.1 400 Bad Request\n\n"

	def returnNotFound(self):
		return "HTTP/1.1 404 Not Found\n\n"