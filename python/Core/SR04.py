import time
import RPi.GPIO as GPIO

class SR04(object):
    def __init__(self, echo, trig, cleanup = True, setGPIOMode = True):
        try:
            #check if correct input is used
            pass
        except:
            #Raise error that inputs must be integers for Pins
            pass

        if (self.setGPIOMode):
            GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.echo, GPIO.IN)
        GPIO.setup(self.trig, GPIO.OUT)

    ## Sense for HC-SR04 ...requires 10 us pulse to trigger module which will cause sensor to start (8 ultrasound bursts at 40 kHz)
    #And then obtains the echo response which we receive....so set trig high for 10us then set it low again
    def sense(self):
        try:
            GPIO.output(self.trig,0) # ensures that trigger is off
            time.sleep(1.0) #waits for sensors to settle                     #### Reduce this wait time later / optimize code so i don't have to wait 1 second for everytime that I want to sense something!!
            GPIO.output(self.trig,1) # sets trig on
            time.sleep(0.00001) #waits 10us
            GPIO.output(self.trig,0)
            while (GPIO.input(self.echo)) ==0:
                   self.pulse_start = time.time()
            while (GPIO.input(self.echo)) ==1:
                   self.pulse_end = time.time()
            self.pulse_duration = self.pulse_end - self.pulse_start
            self.distance = round(self.pulse_duration * 17150,  2) ## this gives us the distance rounded to 2 decimals in cm assuming speed = 343m/s
            print ("distance: " , self.distance, " cm")
        except Exception as e:
            print("Something went wrong, Error: ", str(e))
            if self.cleanup:
                GPIO.cleanup()
        finally:
          GPIO.output(self.trig, False)
          print('program complete')
 

