import time
import RPi.GPIO as GPIO

LED = 40
ECHO1 = 18
TRIGG1 = 22

ECHO2 = 24
TRIGG2 = 26

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LED,GPIO.OUT)


## Sense for HC-SR04 ...requires 10 us pulse to trigger module which will cause sensor to start (8 ultrasound bursts at 40 kHz)
#And then obtains the echo response which we receive....so set trig high for 10us then set it low again
def sense(echo,trig):
    GPIO.setup(echo, GPIO.IN)
    GPIO.setup(trig, GPIO.OUT)
    GPIO.output(trig,0) # ensures that trigger is off
    time.sleep(2.0) #waits for sensors to settle
    GPIO.output(trig,1) # sets trig on
    time.sleep(0.00001) #waits 10us
    GPIO.output(trig,0)
    while (GPIO.input(echo)) ==0:
           pulse_start =time.time()
    while (GPIO.input(echo)) ==1:
           pulse_end =time.time()
    pulse_duration = pulse_end - pulse_start
    distance = round(pulse_duration * 17150,  2) ## this gives us the distance rounded to 2 decimals in cm assuming speed = 343m/s
    print ("distance: " , distance, " cm")
    
while (1):
    GPIO.output(LED,0)
    option = str(input("Enter 1 to sense"))
    if (option == "1"):
        print("measuring distance On Red Sensor")
        sense(ECHO1,TRIGG1)
        print("measuring distance On Blue Sensor")
        sense(ECHO2,TRIGG2)
        
    elif (option == "2"):
        pass
    elif (option == "3"):
        pass
    else:
        print( "incorrect action selected")
        GPIO.output(LED,1)
        time.sleep(2.0)
GPIO.cleanup()
