import tkinter as tk
import RPi.GPIO as GPIO
import time
import threading
from itertools import cycle
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Switch:
    __position = None
    __gpio_pin_btn = None
    pos_enum = [0, 1, 2, 3]
    OFF = pos_enum.index(1)
    ON = pos_enum.index(2)
    INTERMEDIATE = pos_enum.index(0)
    INVALID = pos_enum.index(3)
    def __init__(self, position, gpio_pin_btn, delay=0):
        self.__gpio_pin_btn = gpio_pin_btn
        GPIO.setup(gpio_pin_btn, GPIO.IN)  
        """Cчитывается """
        if type(position) == int:
            if position < 0 or position > 3:
                raise Exception("Invalid position. Position must be integer in range [0, 3]")
            self.__position = position
        else:
            self.__position = self.INTERMEDIATE
        self.__delay = delay
        
    def delay(self):
        time.sleep(self.__delay)   
            
    def cycle(self):
        """Функция необходима для бесконечного переключения состояния кнопки
        в диапазоне [0, 1, 2, 3]
        """
        if self.__position == self.pos_enum.index(self.pos_enum[-1]):
            self.__position = 0
        else:
            self.__position += 1
            
    def get_position(self):
        return self.__position
        
    def toggle(self):
        """Переключатель
        Так как лампочки зависят от position
        необходимо указать для функции toggle
        состоянии "2" и "3" - Invalid position
        """
        if self.__position == 0:
            self.__position = 1
        elif self.__position == 1:
            self.__position = 0
        if self.__position == 2 or self.__position == 3:
            raise Exception("Invalid position")
        
    def btn_switch_condition(self):
        if GPIO.input(self.__gpio_pin_btn) == GPIO.LOW:
            self.__position = 1
        if GPIO.input(self.__gpio_pin_btn) == GPIO.HIGH:
            self.__position = 0
                
    def btn_cycle_condition(self):
        if GPIO.input(self.__gpio_pin_btn) == GPIO.LOW:
            self.__position = 1
        if GPIO.input(self.__gpio_pin_btn) == GPIO.HIGH:
            self.__position = 0
        if GPIO.input(self.__gpio_pin_btn) == GPIO.LOW:
            self.__position = 2
        if GPIO.input(self.__gpio_pin_btn) == GPIO.LOW:
            self.__position = 3

class LED:
    
    __status = 0
    __switch_on_handler = None
    __switch_off_handler = None
    __gpio_pin = None

    def __init__(self, gpio_pin, status=0, on_switch_on=None, on_switch_off=None):
        self.__gpio_pin = gpio_pin
        self.__status = status
        self.__switch_on_handler = on_switch_on
        self.__switch_off_handler = on_switch_off
        GPIO.setup(gpio_pin, GPIO.OUT)
        if status == 1:
            self.switch_on()
        else:
            self.switch_off()

    def switch_on(self):
        GPIO.output(self.__gpio_pin, GPIO.HIGH)
        self.__status = 1

    # функция, которая применяется позже для изменения состояния лампочек(включает)
    def switch_off(self):
        GPIO.output(self.__gpio_pin, GPIO.LOW)
        self.__status = 0

    def toggle(self):
        if self.__status == 0:
            self.switch_on()
        else:
            self.switch_off()

class ButtonView(tk.Tk):
    __clickHandler = None
    __clickHand = None

    def __init__(self, text1, text2, command1, command2):
        """ Создание двух кнопок
        Первая кнопка управляется с помощью функции def cycle():
        Функция передает состояния кнопки в диапазоне [0, 1, 2, 3]
        лампочкам и меняет их состояние
        Вторая кнопка меняет положения лампочек с задержкой
        """
        super().__init__()
        self.__clickHandler = command1
        self.__clickHand = command2
        self.btn1 = tk.Button(self, text="Circle", command=self.click1)
        self.btn1.pack(padx=120, pady=30)
        self.btn2 = tk.Button(self, text="Switch", command=self.click2)
        self.btn2.pack(padx=120, pady=30)
        
    def click1(self):
        self.__clickHandler()
        
    def click2(self):
        self.__clickHand()

class SwitchController():
    
    __positionOnLed = None
    __positionOffLed = None
    __switchModel = None

    def __init__(self, switch, ledOn, ledOff):
        self.__switchModel = switch
        self.__positionOnLed = ledOn
        self.__positionOffLed = ledOff
        self.update_leds()
        self.switch_leds()
        
    def update_leds(self):
        """ Передача позиции кнопки для включения и отключения лампочек """
        if self.__switchModel.get_position() == 0:
            self.__positionOnLed.switch_off()
            self.__positionOffLed.switch_off()
        if self.__switchModel.get_position() == 1:
            self.__positionOnLed.switch_off()
            self.__positionOffLed.switch_on()
        if self.__switchModel.get_position() == 2:
            self.__positionOnLed.switch_on()
            self.__positionOffLed.switch_off()
        if self.__switchModel.get_position() == 3:
            self.__positionOnLed.switch_on()
            self.__positionOffLed.switch_on()

    def switch_leds(self):
        if self.__switchModel.get_position() == 1:
            self.__positionOffLed.switch_off()
            self.__switchModel.delay()
            self.__positionOnLed.switch_on()
        if self.__switchModel.get_position() == 0:
            self.__positionOnLed.switch_off()
            self.__switchModel.delay()
            self.__positionOffLed.switch_on()
            
    def handleClick(self):
        self.__switchModel.cycle()
        self.update_leds()
        
    def handleClickSwitch(self):
        self.__switchModel.toggle()
        self.switch_leds()
        
    def handle_button_switch(self):
        while True:
            self.__switchModel.btn_switch_condition()
            self.switch_leds()    
        
if __name__ == "__main__":
    
    l1 = LED (12, 0)
    
    l2 = LED (24, 1)
    
    sw = Switch (1, 3, 1)
    
    sw_ctl = SwitchController(switch = sw, ledOn = l1, ledOff = l2)

#     sw_ctl.handle_button_switch()
"""Если убрать комментарий, то будет работать реальная кнопка, но надо заккоментировать нижнюю строчку"""

    btVirtual = ButtonView("Circle", "Switch", command1 = sw_ctl.handleClick, command2 = sw_ctl.handleClickSwitch)
    
