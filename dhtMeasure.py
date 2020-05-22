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
		self.dht11 = dht.DHT11(machine.Pin(int(conf.getDH11pin())))
		self.iter = 0

	def testMeasureAndStoreData(self):
		print ("Masure values ==")
		while True:
			print("=== Iteration" + str(self.iter))
			self.addElementToArray(self.tempArr, self.iter)
			self.addElementToArray(self.humArr, self.iter + 2)
			self.iter = self.iter + 1
			await uasyncio.sleep(2)

	def measureTempAndHum(self):
		print("Measure temperature and humidity")
		self.dht11.measure()
		self.addElementToArray(self.tempArr, self.dht11.temperature())
		self.addElementToArray(self.humArr, self.dht11.humidity())
		print("temperature: " + str(dht[0]) + " humidity: " + str(dht[1]))
		await uasyncio.sleep(10)

	def getApiPath(self):
		return self.apiPath

	def getMessage(self):
		""" This method is paring a measured values into json format """
		print("Prepare message")

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

		msg = json.dumps({"Temperature" : str(t), "Humidity" : str(h)})
		print("Message prepared: " + msg)
		return header + msg

	def addElementToArray(self, arr, value):
		arr.append(value)
		arr = arr[-self.arrLength:]

	def calcMovingAvg(self, val):
		""" Calculate moving avarage for entered values """
		sum = 0
		for v in val:	
			sum = sum + v
		return int(sum / len(val))
