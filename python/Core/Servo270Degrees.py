import time
import RPi.GPIO as GPIO


## CLASS FOR MOVING THE VEHICLE
class Move (object):
    def __init__(self, pin, cleanup = False, setWarnings = False, debugging = False, keepCurrentOn = False, startValue = 6.5):
        self.pin = pin
        self.cleanup = cleanup
        self.setWarnings = setWarnings
        self.debugging = debugging
        self.keepCurrentOn = keepCurrentOn
        self.startValue = startValue         # Experiment with this value 

        #set GPIO mode
        GPIO.setmode(GPIO.BOARD)

        if not setWarnings:
            GPIO.setwarnings(False)
        if cleanup:
            GPIO.cleanup()

        GPIO.setup(pin, GPIO.OUT)

        #  frequency = 50Hz
        self.pin = GPIO.PWM(pin,50)

    # Turns the servo x degrees
    def turnDegrees (self,degrees):

        if (degrees > 270 or degrees < 0):
            raise Exception("Degrees parameter must be between 0 and 270!. You entered:", degrees)

        self.pin = GPIO.PWM(self.pin, 50)

        try:
            self.pin.start(self.startValue)
            location = 5 
            self.pin.ChangeDutyCycle(location)  

            if self.debugging:
                print("Turning Servo on pin %i " % (self.pin))
        except Exception as e:
            print ("something went wrong, error: ", str(e))
        finally:
            if (self.keepCurrentOn == False):    
                self.pin.stop()
            time.sleep(0.100)    ## necessary delay to allow setup of servos
            #Try reducing wait time at end to optimize performance

    # Poweroff for servo # backup 
    def powerOff (self):
        self.pin.stop()