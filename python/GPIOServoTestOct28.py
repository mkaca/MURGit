import time
import RPi.GPIO as GPIO

LED = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(LED,GPIO.OUT)

  # channel=12 frequency=50Hz
while (1):
    GPIO.setup(12, GPIO.OUT)
    p = GPIO.PWM(12, 50)
    GPIO.output(LED,0)
    option = input("Enter 1 or 0")
    if (option == "1"):
        p.start(6.5)
        ##dutyCycles = [10,6.5,4]   ##THIS IS FOR WHEEL 1
        dutyCycles = [8,6.5,4]      ## This is for WHEEL 2
        try:
                for dc in dutyCycles:
                    p.ChangeDutyCycle(dc)
                    print("Dutycycle: ",dc)
                    time.sleep(0.8)
                p.stop()
##                time.sleep(2.5)
##                p.start(7.5)
##                for dc in range(0, 71, 5):
##                   p.ChangeDutyCycle(dc)
##                   print("Dutycycle: ",dc)
##                   time.sleep(1.0)
##                p.stop()
        except KeyboardInterrupt:
            pass
        time.sleep(1.0)    ## necessary delay to allow setup of servos
    else:
        print("not running servos")
        GPIO.output(LED,1)
        time.sleep(1.0)
GPIO.cleanup()
