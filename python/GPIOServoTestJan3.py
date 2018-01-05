import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(40, GPIO.OUT)

  # channel=12 frequency=50Hz
while (1):
    GPIO.setup(40, GPIO.OUT)
    p = GPIO.PWM(40, 50)
    option = input("Enter 1 or 0")
    print (option)
    if (option == "1" or option == 1):
        p.start(6.5)
        dutyCycles = [4,1.6,7.62,11.24,12.5,7.62,4]      ## This is for WHEEL 2
        try:   # so 90 degree range both ways would be 1.6 - 7.62
                for dc in dutyCycles:
                    p.ChangeDutyCycle(dc)
                    print("Dutycycle: ",dc)
                    time.sleep(1.45)
                p.stop()

        except KeyboardInterrupt:
            pass
        time.sleep(1.0)    ## necessary delay to allow setup of servos
    else:
        print("not running servos")
        time.sleep(1.0)
GPIO.cleanup()
