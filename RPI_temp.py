import RPi.GPIO as GPIO
import time
import urllib2
 
def bin2dec(string_num):
    return str(int(string_num, 2))


data = []
	 
GPIO.setmode(GPIO.BCM)
	 
GPIO.setup(4,GPIO.OUT)
GPIO.output(4,GPIO.HIGH)
time.sleep(0.025)
GPIO.output(4,GPIO.LOW)
time.sleep(0.02)
 
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	

while GPIO.input(4) == 0:
	pass
while GPIO.input(4) == 1:
	pass
for i in range(0,2000):
    data.append(GPIO.input(4))
	
#print data
bit_count = 0
tmp = 0
count = 0
HumidityBit = ""
TemperatureBit = ""
crc = ""
	 

try:
	while data[count] == 1:
		tmp = 1
		count = count + 1
 
	for i in range(0, 32):
		bit_count = 0
 
		while data[count] == 0:
			tmp = 1
			count = count + 1
 
		while data[count] == 1:
			bit_count = bit_count + 1
			count = count + 1
	 
		if bit_count > 9:
			if i>=0 and i<8:
				HumidityBit = HumidityBit + "1"
			if i>=8 and i<16:
				pass
			if i>=16 and i<24:
				TemperatureBit = TemperatureBit + "1"
			if i>=24 and i<32:
				pass
		else:
			if i>=0 and i<8:
				HumidityBit = HumidityBit + "0"
			if i>=8 and i<16:
				pass
			if i>=16 and i<24:
				TemperatureBit = TemperatureBit + "0"
			if i>=24 and i<32:
				pass
#	print "Data : "
#	print "Humidity : " + HumidityBit
#	print "Temperature : " + TemperatureBit
#	print da1
#	print da2
 	
except:
	print "ERR_RANGE 1"
#	exit(0)
 
try:
	for i in range(0, 8):
		bit_count = 0
 
		while data[count] == 0:
			tmp = 1
			count = count + 1
 
		while data[count] == 1:
			bit_count = bit_count + 1
			count = count + 1
 
		if bit_count > 12:
			crc = crc + "1"
		else:
				crc = crc + "0"
except:
	print "ERR_RANGE 2"
#	exit(0)
	 
Humidity = bin2dec(HumidityBit)
Temperature = bin2dec(TemperatureBit)
	 
if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:
	print "Humidity:"+ Humidity +"%"
	print "Temperature:"+ Temperature +"C"
	urllib2.urlopen("http://192.168.88.85?temp="+Temperature+"humid="+Humidity).close
else:
	print "Result"
	print Humidity
	print Temperature
#	print "ERR_CRC"
