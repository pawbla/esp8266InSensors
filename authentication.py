import ure

class Authentication():

	def authenticate(self, msg):
		print("Authenticate")
		u = ure.search(b'Authentication:\\s([A-Za-z0-9\\.]*)\r', msg)
		if u is None:
			return False
		if u.group(1).decode("utf-8") != "Password":
			return False
		return True