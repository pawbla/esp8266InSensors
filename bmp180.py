from machine import I2C, Pin
from ustruct import unpack as unp
import time
import math

class BMP180():
	def __init__(self, sclP, sdaP, alt):
		self.addr = 0x77
		self.mode = 0

		self.altitude = alt

		self.UT_nc = 0
		self.UP_nc = 0

		self.i2c = I2C(scl=Pin(int(sclP)),sda=Pin(int(sdaP)),freq=100000)


		self.readCalibration()

	def readCalibration(self):
		#read calibration datas
		self._AC1 = unp('>h', self.i2c.readfrom_mem(self.addr, 0xAA, 2))[0]
		self._AC2 = unp('>h', self.i2c.readfrom_mem(self.addr, 0xAC, 2))[0]
		self._AC3 = unp('>h', self.i2c.readfrom_mem(self.addr, 0xAE, 2))[0]
		self._AC4 = unp('>H', self.i2c.readfrom_mem(self.addr, 0xB0, 2))[0]
		self._AC5 = unp('>H', self.i2c.readfrom_mem(self.addr, 0xB2, 2))[0]
		self._AC6 = unp('>H', self.i2c.readfrom_mem(self.addr, 0xB4, 2))[0]
		self._B1 = unp('>h', self.i2c.readfrom_mem(self.addr, 0xB6, 2))[0]
		self._B2 = unp('>h', self.i2c.readfrom_mem(self.addr, 0xB8, 2))[0]
		self._MB = unp('>h', self.i2c.readfrom_mem(self.addr, 0xBA, 2))[0]
		self._MC = unp('>h', self.i2c.readfrom_mem(self.addr, 0xBC, 2))[0]
		self._MD = unp('>h', self.i2c.readfrom_mem(self.addr, 0xBE, 2))[0]
		pass

	def measure(self):
		#measure datas
		delays = (5, 8, 14, 25)
		#read raw temperature
		self.i2c.writeto_mem(self.addr, 0xF4, bytearray([0x2E]))
		#wait 5ms
		t_start = time.ticks_ms()
		time.sleep_ms(5)
		UT_raw = self.i2c.readfrom_mem(self.addr, 0xF6, 2)
		self.UT_nc = unp('>h', UT_raw)[0]
		#read raw pressure
		self.i2c.writeto_mem(self.addr, 0xF4, bytearray([0x34+(self.mode << 6)]))
		t_pressure_ready = delays[self.mode]
		t_start = time.ticks_ms()
		time.sleep_ms(5)
		MSB_raw = self.i2c.readfrom_mem(self.addr, 0xF6, 1)
		LSB_raw = self.i2c.readfrom_mem(self.addr, 0xF7, 1)
		XLSB_raw = self.i2c.readfrom_mem(self.addr, 0xF8, 1)
		MSB = unp('B', MSB_raw)[0]
		LSB = unp('B', LSB_raw)[0]
		XLSB = unp('B', XLSB_raw)[0]
		print("3")
		self.UP_nc = ((MSB << 16)+(LSB << 8)+XLSB) >> (8-self.mode)
		pass

	def temperature(self):
		X1 = (self.UT_nc-self._AC6)*self._AC5/2**15
		X2 = self._MC*2**11/(X1+self._MD)
		self.B5_raw = X1+X2
		t = (((X1+X2)+8)/2**4)/10
		return t

	def pressure(self):
		press = [0,0]
		B6 = self.B5_raw-4000
		X1 = (self._B2*(B6**2/2**12))/2**11
		X2 = self._AC2*B6/2**11
		X3 = X1+X2
		B3 = ((int((self._AC1*4+X3)) << self.mode)+2)/4
		X1 = self._AC3*B6/2**13
		X2 = (self._B1*(B6**2/2**12))/2**16
		X3 = ((X1+X2)+2)/2**2
		B4 = abs(self._AC4)*(X3+32768)/2**15
		B7 = (abs(self.UP_nc)-B3) * (50000 >> self.mode)
		if B7 < 0x80000000:
			pressure = (B7*2)/B4
		else:
			pressure = (B7/B4)*2
		X1 = (pressure/2**8)**2
		X1 = (X1*3038)/2**16
		X2 = (-7357*pressure)/2**16
		# atmospheric pressure
		press[0] = pressure+(X1+X2+3791)/2**4
		# atmospheric pressure at sea level
		press[1] = press[0] / (( 1 - (self.altitude / 44330)) ** 5.255)
		return press
