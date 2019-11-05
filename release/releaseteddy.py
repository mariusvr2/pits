import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
print "Starting burn..."
GPIO.output(21,GPIO.HIGH)
time.sleep(20)
print "Stopping burn..."
GPIO.output(21,GPIO.LOW)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
