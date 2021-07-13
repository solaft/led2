import RPi.GPIO as GPIO         
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(24, GPIO.OUT) 
GPIO.setup(3, GPIO.IN)
class bdbd:
    def ff(self):
        while True:                     
            if GPIO.input(3) == False: 
                GPIO.output(12, 1)
                GPIO.output(24, 1)
            else:                       
                GPIO.output(12, 0)
                GPIO.output(24, 0) 