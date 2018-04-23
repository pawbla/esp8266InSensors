import json

class Config:
	def __init__(self):
		with open('config.json', 'r') as file: 
			self.config = json.load(file)
		file.close()

		print("ssid: " + self.config['ssid'])
		print("password: " + self.config['password'])	

	def getSSID(self):
		return self.config['ssid']

	def getPassword(self):
		return self.config['password']

	def getDH11pin(self):
		return self.config['dht11Pin']

	def getBMPscl(self):
		return self.config['bmp180SCL']

	def getBMPsda(self):
		return self.config['bmp180SDA']