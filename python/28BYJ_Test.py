#!/usr/bin/env python

from Core import Stepper28BYJ
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.output(7,False)
stepper = Stepper28BYJ.Stepper28BYJ(37,33,31,29,cleanup=True)

stepper.moveToPosition(45)
time.sleep(1)
GPIO.output(7,True)
stepper.moveToPosition(-45)
time.sleep(1)
stepper.moveToPosition(0)
time.sleep(1)
#stepper.moveDegrees(90,clockwise = True)