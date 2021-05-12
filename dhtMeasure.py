import dht
import machine
import uasyncio
import json

class DHT_Measure():
	def __init__(self, conf):
		self.apiPath = "measurements"
		self.arrLength = 5
		self.tempArr = [0] * self.arrLength
		self.humArr = [0] * self.arrLength
		try:
			self.dht11 = dht.DHT11(machine.Pin(int(conf.getDH11pin())))
		except Exception as e:
			self.error = "Unable to initialize DHT sensor: "  + (str(e))
		self.iter = 0
		self.errors = ""
		self.m_p = 0

	def measureTempAndHum(self):
		print("Measure temperature and humidity")
		while True:
			if self.dht11:
				print("DHT 11 object exist start measurements")
				try:
					self.dht11.measure()
					self.addElementToArray(self.tempArr, self.dht11.temperature())
					self.addElementToArray(self.humArr, self.dht11.humidity())
					self.m_p = self.m_p + 1
					self.errors = ""
				except Exception as e:
					self.error = "Unable to measure DHT datas: " + (str(e))
			await uasyncio.sleep(10)

	def getApiPath(self):
		return self.apiPath

	def getMessage(self):
		""" This method is paring a measured values into json format """
		print("Prepare message for measurements")

		t = self.calcMovingAvg(self.tempArr)
		h = self.calcMovingAvg(self.humArr)

		header = "HTTP/1.1 200 OK\nContent-Type: application/json\r\n\n"
		html1 = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body>"""
		html2 = """</body>
</html>
"""
		if self.errors == "":
			msg = json.dumps({"Temperature" : str(t), "Humidity" : str(h)})
		else:
			msg = json.dumps({"error" : self.errors})
		return header + msg

	def addElementToArray(self, arr, value):
		arr.append(value)
		arr.remove(arr[0])

	def calcMovingAvg(self, val):
		""" Calculate moving avarage for entered values """
		sum = 0
		for v in val:	
			sum = sum + v
		return int(sum / len(val))
