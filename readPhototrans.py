#!/usr/bin/python
 
import spidev
 
spi = spidev.SpiDev()
spi.open(0,0)
 
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
while True:
 
  print "0="+str(ReadChannel(0))+" 1="+str(ReadChannel(1))+" 2="+str(ReadChannel(2))+" 3="+str(ReadChannel(3))
 
