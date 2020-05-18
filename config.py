import json

class Config:
	def __init__(self):
		with open('config.json', 'r') as file: 
			self.config = json.load(file)
		file.close()

		print("DHT11 data pin: " + self.config['dht11Pin'])
		print("ssid: " + self.config['ssid'])

	def getSSID(self):
		return self.config['ssid']

	def getPassword(self):
		return self.config['password']

	def getDH11pin(self):
		return self.config['dht11Pin']

	def getAccPassword(self):
		return self.config['accPassword']