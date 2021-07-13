import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(24, GPIO.OUT) 
GPIO.setup(3, GPIO.IN)

def j():
    GPIO.input(3) == False
    GPIO.output(12, GPIO.LOW)
    time.sleep(1)
    GPIO.output(24, GPIO.HIGH)
if __name__ == '__main__' :       
    j()

        
                


 