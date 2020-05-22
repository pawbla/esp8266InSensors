import network

class LAN_Connection():

	def __init__(self, ssid, password):
		self.password = password
		self.password = password


	def connectToLAN(self):
		""" This method allows to connect an ESP8266 to the router """
		print("Connect to LAN")
		#stationary mode for connecting ESP8266 module to the router
		sta_if = network.WLAN(network.STA_IF)
		print("Check connection....")
		if not sta_if.isconnected():
			#connect to the router when no connected after startup
			print("Connecting to network...")
			sta_if.active(True)
			sta_if.connect(self.ssid, self.password)
			while not sta_if.isconnected():
				pass
		print('ESP8266 is connected to the router. IP: ', sta_if.ifconfig())
		pass