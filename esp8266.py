import network
import socket
import dht
import machine
import json
import ure
import bmp180
import time
import config

class ESP8266:
	def __init__(self):

		#get configuration datas
		conf = config.Config()

		self.connectToLAN(conf.getSSID(), conf.getPassword())
		self.createSocketServer()
		self.dht11 = dht.DHT11(machine.Pin(int(conf.getDH11pin())))
		self.bmp = bmp180.BMP180(conf.getBMPscl() , conf.getBMPsda())

	def listenOnSocketServer(self):
		""" This method is listening on created socket server """
		# in this method shall be executed every sensors' measurements
		while True:
			con, addr = self.s.accept()
			print('Connection from: ', addr)
			# here shall be executed all measurements and getting measured values
			dht = self.measureTempAndHum()
			bmpM = self.measurePressure()
			#get request and send message
			try:
				rec = con.recv(500)
				print("Received message: " + str(rec))
			except OSError as e:
				print("An error has occured: ", e)
			msg = self.prepareMessage(bmpM[0],dht[1],bmpM[1])
			con.send(msg)
			con.close()
		pass		

	def connectToLAN(self, ssid, password):
		""" This method allows to connect an ESP8266 to the router """
		print("Connect to LAN")
		#stationary mode for connecting ESP8266 module to the router
		sta_if = network.WLAN(network.STA_IF)
		print("Check connection....")
		if not sta_if.isconnected():
			#connect to the router when no connected after startup
			print("Connecting to network...")
			sta_if.active(True)
			sta_if.connect(ssid, password)
			while not sta_if.isconnected():
				pass
		print('ESP8266 is connected to the router. IP: ', sta_if.ifconfig())
		pass

	def createSocketServer(self):
		""" This metod allows to create a server which will be listen a connection on created socket """
		port = 80
		addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
		try:
			self.s = socket.socket()
			self.s.bind(addr)
			self.s.listen(1)
		except OSError as e:
			print("Error: " + str(e))
			if ure.match('.*EADDRINUSE.*',str(e)):
				print("Adrr")
				machine.reset()

	def measureTempAndHum(self):
		dht=[0,0]
		self.dht11.measure()
		dht[0] = self.dht11.temperature()
		dht[1] = self.dht11.humidity()
		print("temperature: " + str(dht[0]) + " humidity: " + str(dht[1]))
		return dht

	def measurePressure(self):
		bmp=[0,0]
		self.bmp.measure()
		bmp[0]=self.bmp.temperature()
		bmp[1]=self.bmp.pressure()
		print("temperature: " + str(bmp[0]) + " pressure: " + str(bmp[1]))
		return bmp


	def prepareMessage(self, t, h, p):
		""" This method is paring a measured values into json format """

		html1 = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body>"""
		html2 = """</body>
</html>
"""

		msg = json.dumps({"Temperature" : str(t), "Humidity: " : str(h), "Pressure:" : str(p)})
		print("Message prepared: " + msg)
		return html1 + msg + html2