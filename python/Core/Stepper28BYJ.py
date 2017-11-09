#!/usr/bin/env python
 
# import required libs
import time
import RPi.GPIO as GPIO

class Stepper28BYJ(object):
  def __init__(self, Pin1, Pin2, Pin3, Pin4, cleanup = True, setGPIOMode = True):

    self.Pin1 = Pin1
    self.Pin2 = Pin2
    self.Pin3 = Pin3
    self.Pin4 = Pin4
    self.cleanup = cleanup
    self.setGPIOMode = setGPIOMode

    #Throw error if class is called without the 4 pins .... change this to like try catch with int(input) or whatever
    if (Pin1 == None or Pin2 == None or Pin3 == None or Pin4 == None):
      raise ValueError("You MUST define all 4 pins as INTEGERS, ex: 2,23,4,21")

    #if cleanup:
      #GPIO.cleanup() #cleaning up in case GPIOS have been preactivated
    
    # Use BCM GPIO references
    # instead of physical pin numbers
    if(setGPIOMode):
      GPIO.setmode(GPIO.BOARD)
    
    # be sure you are setting pins accordingly
    #in 1, 2, 3, 4
    self.StepPins = [Pin1,Pin2,Pin3,Pin4]
   
    # Set all pins as output and ensure they are low
    for pin in self.StepPins:
      GPIO.setup(pin,GPIO.OUT)
      GPIO.output(pin, False)
    #wait some time to start
    time.sleep(0.5)
      # Define some settings from datasheet
    self.StepCounter = 0
    self.WaitTime = 0.0015
     
     
    # Define stepper sequence
    self.StepCount = 8
    self.Seq = []
    self.Seq = range(0, self.StepCount)
    self.Seq[0] = [1,0,0,0]
    self.Seq[1] = [1,1,0,0]
    self.Seq[2] = [0,1,0,0]
    self.Seq[3] = [0,1,1,0]
    self.Seq[4] = [0,0,1,0]
    self.Seq[5] = [0,0,1,1]
    self.Seq[6] = [0,0,0,1]
    self.Seq[7] = [1,0,0,1]

  def moveDegrees(self, degrees, clockwise = True):
    GPIO.setmode(GPIO.BOARD)
    try:
      
      self.steps = int(round(abs(degrees)*1024/90))
      print('Moving Stepper %i steps',self.steps)
      print(', which is the same as %i degrees',degrees)
      # moves stepper motor by 45 degrees forever
      for _ in range(0,self.steps):  # 12 =1 degree
          for pin in range(0, 4):
            xpin = self.StepPins[pin]
            if self.Seq[self.StepCounter][pin]!=0:
              #print " Step %i Enable %i" %(StepCounter,xpin)
              GPIO.output(xpin, True)
            else:
              GPIO.output(xpin, False)

          # Determine the direction of the stepper motor    
          if (clockwise):                    ### Might need to change this direction logic
            self.StepCounter += 1
          else:
            self.StepCounter -= 1                ### Might need to do more than just this 
        # If we reach the end of the sequence
        # start again
          if (self.StepCounter==self.StepCount):
            self.StepCounter = 0
          if (self.StepCounter<0):
            self.StepCounter = self.StepCount - 1      
        # Wait before moving on
          time.sleep(self.WaitTime)
      print('program succeeded')
      time.sleep(0.01)   #wait 10 ms 

    except Exception as e:
      if self.cleanup:
        GPIO.cleanup()
        print('program failed: \t')
        print str(e)
        time.sleep(0.500)

    #turn off stepper motor
    finally: #cleaning up and setting pins to low again (motors can get hot if you wont) 
        for pin in self.StepPins:
          GPIO.setup(pin,GPIO.OUT)
          GPIO.output(pin, False)
          print('program complete')
  