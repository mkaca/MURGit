import RPi.GPIO as GPIO #calling for header file which helps in using GPIOs of PI
import time

LED=21
 
GPIO.setmode(GPIO.BCM)     #programming the GPIO by BCM pin numbers. (like PIN40 as GPIO21)
GPIO.setwarnings(False)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)#initialize GPIO21 (LED) as an output Pin
GPIO.output(LED,0)
p= GPIO.PWM(20,50)
p.start(7.5)  #double check the right pwm for your application
while(1):
     print("enter input")
     data = input()
     if (data == "0"):    #if '0' is sent from the Android App, turn OFF the LED
      print ("GPIO 21 LOW, LED OFF")
      GPIO.output(LED,0)
     elif (data == "1"):    #if '1' is sent from the Android App, turn OFF the LED
      print ("GPIO 21 HIGH, LED ON")
      GPIO.output(LED,1)
      p.ChangeDutyCycle(7.5)
      time.sleep(3)
      p.ChangeDutyCycle(2.5)
     else:
      print ("Bruh")
      break
