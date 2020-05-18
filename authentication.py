import ure
import ubinascii

class Authentication():
	def __init__(self, password):
		self.password = password

	def authenticate(self, msg):
		u = ure.search(b'Authorization:\\s([A-Za-z0-9\\.]*)\r', msg)
		if u is None:
			return False
		if u.group(1).decode("utf-8") != self.getPass():
			return False
		return True

	def getPass(self):
		return ubinascii.a2b_base64(self.password.encode("ascii")).decode("utf-8")

	def message(self):
		return "HTTP/1.1 401 Unauthorized\nWWW-Authenticate: Basic\n"