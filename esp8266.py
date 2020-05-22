import uasyncio
import config
import lanConnection as LAN
import dhtMeasure as DHT
import restAPI as api

class ESP8266:
	def __init__(self):
		#get configuration datas
		conf = config.Config()
		self.lan = LAN.LAN_Connection(conf.getSSID(), conf.getPassword())
		self.lan.connectToLAN()
		self.dht_m = DHT.DHT_Measure(conf)
		self.api = api.Rest_API(conf, self.dht_m)
		self.iter = 0

	def initialize(self):
		print("Initialize threads")
		loop = uasyncio.get_event_loop()
		loop.create_task(self.dht_m.measureTempAndHum())
		loop.call_soon(uasyncio.start_server(self.api.process, "0.0.0.0", 80))
		loop.run_forever()
		pass