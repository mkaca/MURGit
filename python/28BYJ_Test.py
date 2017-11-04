#!/usr/bin/env python
"""
# import required libs
import time
import RPi.GPIO as GPIO

GPIO.cleanup() #cleaning up in case GPIOS have been preactivated
 
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)
 
# be sure you are setting pins accordingly
#in 1, 2, 3, 4
StepPins = [37,33,31,29]
 
# Set all pins as output and makes them be 0 
for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

#wait some time to start
time.sleep(0.5)
 
# Define some settings from datasheet
StepCounter = 0
WaitTime = 0.0015
 
# Define simple sequence
StepCount1 = 4
Seq1 = []
Seq1 = range(0, StepCount1)
Seq1[0] = [1,0,0,0]
Seq1[1] = [0,1,0,0]
Seq1[2] = [0,0,1,0]
Seq1[3] = [0,0,0,1]
 
# Define advanced sequence
# as shown in manufacturers datasheet
StepCount2 = 8
Seq2 = []
Seq2 = range(0, StepCount2)
Seq2[0] = [1,0,0,0]
Seq2[1] = [1,1,0,0]
Seq2[2] = [0,1,0,0]
Seq2[3] = [0,1,1,0]
Seq2[4] = [0,0,1,0]
Seq2[5] = [0,0,1,1]
Seq2[6] = [0,0,0,1]
Seq2[7] = [1,0,0,1]

#Full torque
StepCount3 = 4
Seq3 = []
Seq3 = [3,2,1,0]
Seq3[0] = [0,0,1,1]
Seq3[1] = [1,0,0,1]
Seq3[2] = [1,1,0,0]
Seq3[3] = [0,1,1,0]
 
# set
Seq = Seq2
StepCount = StepCount2
 
# Start main loop
try:
  while 1==1:
    # moves stepper motor by 45 degrees forever
    for _ in range(0,512):  # 12 =1 degree
        for pin in range(0, 4):
          xpin = StepPins[pin]
          if Seq[StepCounter][pin]!=0:
            #print " Step %i Enable %i" %(StepCounter,xpin)
            GPIO.output(xpin, True)
          else:
            GPIO.output(xpin, False)
        StepCounter += 1
        

      # If we reach the end of the sequence
      # start again
        if (StepCounter==StepCount):
          StepCounter = 0
        if (StepCounter<0):
          StepCounter = StepCount
     
      # Wait before moving on
        time.sleep(WaitTime)
    time.sleep(2)
except:
  GPIO.cleanup();
finally: #cleaning up and setting pins to low again (motors can get hot if you wont) 
  GPIO.cleanup();
  for pin in StepPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)
"""
from Core import Stepper28BYJ
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)

stepper = Stepper28BYJ.Stepper28BYJ(37,33,31,29,cleanup=True)

stepper.moveDegrees(90)