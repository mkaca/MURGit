import time
import RPi.GPIO as GPIO


## CLASS FOR MOVING THE VEHICLE
class Move (object):
    def __init__(self, pin, cleanup = False, setWarnings = False, debugging = False, keepCurrentOn = False, startValue = 4, reverse = False , offset = 0):
        self.pin = pin
        self.cleanup = cleanup
        self.setWarnings = setWarnings
        self.debugging = debugging
        self.keepCurrentOn = keepCurrentOn
        self.startValue = startValue         # Experiment with this value 
        self.reverse = reverse
        self.offset = offset

        #set GPIO mode
        GPIO.setmode(GPIO.BOARD)

        if not setWarnings:
            GPIO.setwarnings(False)
        if cleanup:
            GPIO.cleanup()

        GPIO.setup(pin, GPIO.OUT)

        #  frequency = 50Hz
        #self.pin = GPIO.PWM(pin,50)

    # Turns the servo x degrees
    def turnDegrees (self,degrees, degreeFactor = 0.035, keepCurrentOn = False):

        if (degrees > 90 or degrees < -90):
            raise Exception("Degrees parameter must be between 0 and 270!. You entered:", degrees)
        
        print("   :",self.pin)
        p = GPIO.PWM(int(self.pin), 50)

        try:
            # 1.6 to 4 OR  4 to 6.4
            # 0.0267 ....... since 4 = 0 degree point 
            if self.reverse:
                location = 4 -degrees *degreeFactor + self.offset
            else:
                location = degrees *degreeFactor + 4 + self.offset
            if (location < 1.6 or location > 12.5):
                raise Exception("Degrees parameter out of bounds! Max allowable:")
                # TO DO ,,,,change error messsage with more detail
            
            p.start(self.startValue)
            p.ChangeDutyCycle(location)  

            if self.debugging:
                print("Turning Servo on pin %i " % (self.pin))
                print("location:",location)
                #print(self.reverse)
                print(degrees)
        except Exception as e:
            print ("something went wrong, error: ", str(e))
        finally:
            if (self.keepCurrentOn == False and keepCurrentOn == False):    
                p.stop()
            time.sleep(0.100)    ## necessary delay to allow setup of servos
            #Try reducing wait time at end to optimize performance

    # Poweroff for servo # backup 
    def powerOff (self):
        p = GPIO.PWM(self.pin, 50)
        p.stop()