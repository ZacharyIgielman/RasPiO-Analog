#!/usr/bin/python
 
import spidev
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

a=GPIO.PWM(17,10)
b=GPIO.PWM(18,10)
p=GPIO.PWM(22,10)
q=GPIO.PWM(23,10)

a.start(0)
b.start(0)
p.start(0)
q.start(0)

def stop():
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(0)

# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
def spinRight(speed):
    p.ChangeDutyCycle(speed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(speed)
    b.ChangeDutyCycle(0)

# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
def spinLeft(speed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(speed)

# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def forward(speed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(speed)
    b.ChangeDutyCycle(0)

# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def reverse(speed):
    p.ChangeDutyCycle(speed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(speed)

# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnForward(leftSpeed, rightSpeed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(leftSpeed)
    a.ChangeDutyCycle(rightSpeed)
    b.ChangeDutyCycle(0)

# turnReverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnReverse(leftSpeed, rightSpeed):
    p.ChangeDutyCycle(leftSpeed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(rightSpeed)
 
spi = spidev.SpiDev()
spi.open(0,0)
 
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
while True:
 
  frontRight=ReadChannel(0)
  frontLeft=ReadChannel(1)
  backRight=ReadChannel(2)
  backLeft=ReadChannel(3)
 
  frontR=frontRight<200
  frontL=frontLeft<200
  backR=backRight<200
  backL=backLeft<200

  if (frontR+frontL>0 and backR+backL>0) or frontR+frontL+backL+backR==0:
    stop()
  else:
    q.ChangeDutyCycle(frontL*frontLeft*0.2)
    b.ChangeDutyCycle(frontR*frontRight*0.2)

  if frontRight+frontLeft<backRight+backLeft:
    frontRight=0.2*frontRight
    frontLeft=0.2*frontLeft
    if frontLeft>100:
      frontLeft=100
    if frontRight>100:
      frontRight=100
    turnForward(frontRight,frontLeft)
  else:
    turnReverse(50,50)
