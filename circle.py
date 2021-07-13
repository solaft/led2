import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(24, GPIO.OUT) 
GPIO.setup(11, GPIO.IN)
while True:
    if GPIO.input(11) == GPIO.LOW:
        GPIO.output(12, GPIO.LOW)
        GPIO.output(24, GPIO.HIGH)
    elif GPIO.input(11) == GPIO.HIGH:
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
    elif GPIO.input(11) == GPIO.HIGH:
        GPIO.output(12, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
    elif GPIO.input(11) == GPIO.LOW:
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
