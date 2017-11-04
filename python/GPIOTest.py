import bluetooth
import RPi.GPIO as GPIO        #calling for header file which helps in using GPIOs of PI
LED=21
 
GPIO.setmode(GPIO.BCM)     #programming the GPIO by BCM pin numbers. (like PIN40 as GPIO21)
GPIO.setwarnings(False)
GPIO.setup(LED,GPIO.OUT)  #initialize GPIO21 (LED) as an output Pin
GPIO.output(LED,0)
 
server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
 
port = 1
server_socket.setsockopt(server_socket.SOL_SOCKET,server_socket.SO_REUSEADDR,1)

server_socket.bind(("",port))
print ("great success")
server_socket.listen(1)
print ("great success2")

client_socket,address = server_socket.accept()
print ("great success3")
print "Accepted connection from ",address
while 1:
 
 data = client_socket.recv(1024)
 print "Received: %s" % data
 if (data == "0"):    #if '0' is sent from the Android App, turn OFF the LED
  print ("GPIO 21 LOW, LED OFF")
  GPIO.output(LED,0)
 if (data == "1"):    #if '1' is sent from the Android App, turn OFF the LED
  print ("GPIO 21 HIGH, LED ON")
  GPIO.output(LED,1)
 if (data == "q"):
  print ("Quit")
  break
 
client_socket.close()
server_socket.close()