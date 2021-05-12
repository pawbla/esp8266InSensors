import uasyncio
import config
import lanConnection as LAN
import dhtMeasure as DHT
import restAPI as api
import sysInfo as sys_i

class ESP8266:
	def __init__(self):
		#get configuration datas
		print("Initialization")
		conf = config.Config()
		self.lan = LAN.LAN_Connection(conf.getSSID(), conf.getPassword())
		self.lan.connectToLAN()
		self.dht_m = DHT.DHT_Measure(conf)
		self.sys = sys_i.SysInfo()
		self.api = api.Rest_API(conf, self.dht_m, self.sys)
		self.iter = 0

	def initialize(self):
		print("Initialize threads")
		loop = uasyncio.get_event_loop()
		loop.create_task(self.dht_m.measureTempAndHum())
		loop.call_soon(uasyncio.start_server(self.api.process, "0.0.0.0", 80))
		loop.run_forever()
		pass