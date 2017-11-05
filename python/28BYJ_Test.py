#!/usr/bin/env python

from Core import Stepper28BYJ

#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)

stepper = Stepper28BYJ.Stepper28BYJ(37,33,31,29,cleanup=True)

stepper.moveDegrees(90,clockwise = False)
stepper.moveDegrees(90,clockwise = True)