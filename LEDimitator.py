import tkinter as tk
import RPi.GPIO as GPIO
import threading
import time
from itertools import cycle
from threading import Lock
import multiprocessing
from multiprocessing import Process
import sys
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lock = threading.Lock()

class Switch:
    __position = None
    __gpio_pin_btn = None
    pos_enum = [0, 1, 2, 3]
    """задаём массив значенийБ для переключения в 4 разных положениях"""
 ##   OFF = pos_enum.index(1)
 ##   ON = pos_enum.index(2)
 ##   INTERMEDIATE = pos_enum.index(0)
 ##   INVALID = pos_enum.index(3)
 ##   flag = True
    def __init__(self, position, gpio_pin_btn, delay=0):
        self.__gpio_pin_btn = gpio_pin_btn
        GPIO.setup(gpio_pin_btn, GPIO.IN)  
        if type(position) == int:
            if position < 0 or position > 3:
                raise Exception("Invalid position. Position must be integer in range [0, 3]")
            self.__position = position
        """Проверка заданного значения"""

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
            
    def btn_cycle_condition(self):
        """Переключатель для реальной кнопки(cycle)"""
        if GPIO.input(self.__gpio_pin_btn) == GPIO.LOW:
            return 0
        elif GPIO.input(self.__gpio_pin_btn) == GPIO.HIGH:
            return 1      
        elif GPIO.input(self.__gpio_pin_btn) == GPIO.LOW:            
            return 2
        elif GPIO.input(self.__gpio_pin_btn) == GPIO.HIGH:
            return 3
        
    def get_position(self):
        """Функция, возвращающая позицию, полученную при нажатии кнопки"""
        return self.__position
    
    def set_position(self, cur_pos):
        self.__position = cur_pos
    
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
        """Переключатель для реальной кнопки"""
        if GPIO.input(self.__gpio_pin_btn) == GPIO.LOW:
            return 1
        elif GPIO.input(self.__gpio_pin_btn) == GPIO.HIGH:
            return 0
        else:
            return 1
        
  
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
        lock = threading.Lock()
        GPIO.setup(gpio_pin, GPIO.OUT)
        if status == 1:
            self.switch_on()
        else:
            self.switch_off()

    def switch_on(self):
        """Включает лампочку"""
        GPIO.output(self.__gpio_pin, GPIO.HIGH)
        self.__status = 1

    def switch_off(self):
        """Выключает лампочку"""
        GPIO.output(self.__gpio_pin, GPIO.LOW)
        self.__status = 0

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
        """Нажатие на виртуальную кнопку, переключащую лампочки в два состояния с задержкой(цикл toggle). Функция релизуется через Switch Controller"""
        self.__clickHandler()
    def click2(self):
        """Нажатие на виртуальную, переключающую лампочки в 4 разных состояния(цикл Cycle). Функция релизуется через Switch Controller""" 
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
        """ Передача позиции кнопки для включения и отключения лампочек для цикла Cycle"""
        if self.__switchModel.get_position() == 2:
            self.__positionOnLed.switch_off()
            
            self.__positionOffLed.switch_off()
        if self.__switchModel.get_position() == 1:
            self.__positionOnLed.switch_off()
    
            self.__positionOffLed.switch_on()
        if self.__switchModel.get_position() == 0:
            self.__positionOnLed.switch_on()

            self.__positionOffLed.switch_off()
        if self.__switchModel.get_position() == 3:
            self.__positionOnLed.switch_on()
            self.__positionOffLed.switch_on()

    def switch_leds(self):
        """Передача позиции кнопки для включения и отключения лампочек для цикла toggle"""
        if self.__switchModel.get_position() == 1:
            self.__positionOffLed.switch_off()
            self.__switchModel.delay()
            self.__positionOnLed.switch_on()
        if self.__switchModel.get_position() == 0:
            self.__positionOnLed.switch_off()
            self.__switchModel.delay()
            self.__positionOffLed.switch_on()            

    def handleClick(self):
        """Нажатие на виртуальную кнопку, переключающую лампочки в 4 разных состояния(функция Cycle)"""        
        lock.acquire()
        self.__switchModel.cycle()
        self.update_leds()
        lock.release()
    def handleClickSwitch(self):
        """Нажатие на виртуальную на кнопку, переключащую лампочки в два состояния с задержкой(функция toggle)"""        
        lock.acquire()
        self.__switchModel.toggle()
        self.switch_leds()
        lock.release()
    def handle_button_switch(self):
        """Нажатие на реальную кнопку, переключащую лампочки в два состояния с задержкой(функция btn_switch_condition)"""                
        while True:            
            if self.__switchModel.btn_switch_condition():
                lock.acquire()
                before = bool(self.__switchModel.get_position())
                self.__switchModel.set_position(before)
                while self.__switchModel.btn_switch_condition():
                    print(self.__switchModel.get_position())
                    self.switch_leds()
                self.__switchModel.set_position(not before)                    
                lock.release()
    

if __name__ == "__main__":
    

    l1 = LED (12, 0)

    l2 = LED (24, 1)

    sw = Switch (1, 9, 1)
        
    sw_ctl = SwitchController(switch = sw, ledOn = l1, ledOff = l2)
     
    def vb():
        bt = ButtonView("Circle", "Switch", command1 = sw_ctl.handleClick, command2 = sw_ctl.handleClickSwitch)
        bt.mainloop()
    def rb():
        sw_ctl.handle_button_switch()

        
    t1 = threading.Thread(target=rb)
    
    t2 = threading.Thread(target=vb)
    
    t1.start()
    
    t2.start()
    
    t1.join()
    
    t2.join()


   