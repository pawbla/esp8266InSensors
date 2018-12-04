import json

class Config:
	def __init__(self):
		with open('config.json', 'r') as file: 
			self.config = json.load(file)
		file.close()

		print("BMP180 SDA pin: " + self.config['bmp180SDA'])
		print("BMP180 SCL pin: " + self.config['bmp180SCL'])
		print("DHT11 data pin: " + self.config['dht11Pin'])
		print("ssid: " + self.config['ssid'])

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

	def getAltitude(self):
		return self.config['altitude']

	def getAccPassword(self):
		return self.config['accPassword']