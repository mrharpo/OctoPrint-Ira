from serial import Serial
from cobs import cobs
from struct import pack
port = '/dev/ttyUSB0'
BAUD = 1200
from time import sleep

#s = Serial(port, BAUD, )

def send(*args):
	p = cobs.encode(pack('>{}B'.format(len(args)), *args)) + b'\x00'
	#s.write(p)
	print(p)
	sleep(.1)
	if s.in_waiting:
		print(s.read(s.in_waiting))
