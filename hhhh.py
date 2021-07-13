import tkinter as tk
import RPi.GPIO as GPIO
import time
from itertools import cycle
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO.setup(12, GPIO.OUT)
# GPIO.setup(24, GPIO.OUT) 
# GPIO.setup(3, GPIO.IN)
# 
# while True:
#     GPIO.setup(12, GPIO.OUT)
#     GPIO.setup(24, GPIO.OUT) 
#     GPIO.setup(3, GPIO.IN)
#     if GPIO.input(3) == False:
#         GPIO.output(12, GPIO.HIGH)
#         time.sleep(1)
#         GPIO.output(24, GPIO.LOW)
#     else:
#         GPIO.output(24, GPIO.HIGH)
#         time.sleep(1)
#         GPIO.output(12, GPIO.LOW)


# 
# class ButtonModel:
#     __value = 0
# 
#     def toggle(self):
#         if self.__value == 0:
#             self.__value = 1
#         else:
#             self.__value = 0
# # меняет состояние кнопки при нажатии
#     def get_value(self):
#         return self.__value
# # возвращает состояние кнопки    
#
#     def button_press(self):
# GPIO.setup(12, GPIO.OUT)
# GPIO.setup(24, GPIO.OUT) 
# GPIO.setup(3, GPIO.IN)
# while True:
#     if GPIO.input(3) == False:
#         GPIO.output(12, 1)
#         GPIO.output(24, 1)            
#     else:
#         GPIO.output(12, 0)
#         GPIO.output(24, 0) 
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
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)
        """Cчитывается """
        if type(position) == int:
            if position < 0 or position > 3:
                raise Exception("Invalid position. Position must be integer in range [0, 3]")
            self.__position = position
#         if type(position) == str:
#             if position in self.pos_enum:
#                 position = self.pos_enum.index(position)
#             else:
#                 raise Exception("Invalid position")
        else:
            self.__position = self.INTERMEDIATE
        self.__delay = delay
        
    def delay(self):
        time.sleep(self.__delay)   
#     def __repr__(self):
#         return repr(self.pos_enum[self.__position])
# 
#     def __str__(self):
#         return self.pos_enum[self.__position]
# 
#     def __int__(self):
#         return int(self.__position)
# 
#     def toJSON(self):
#         return int(self.__position)
# 
#     def as_int(self):
#         return int(self.__position)
# 
#     def as_mms_var(self):
#         return self.as_int()
#     def switch(self):
#         if self.__position == self.ON:
#             self.__position = self.OFF
#         else:
#             self.__position = self.ON
            
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
 #   def turn_on(self):
 #        self.__position == 1
        
 #   def turn_off(self):
 #       self.__position = 0
        
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
        while True:
            if GPIO.input(self.__gpio_pin_btn) == GPIO.LOW:
                GPIO.output(12, GPIO.LOW)
                time.sleep(1)
                GPIO.output(24, GPIO.HIGH)                
            if GPIO.input(self.__gpio_pin_btn) == GPIO.HIGH:
                GPIO.output(24, GPIO.LOW)
                time.sleep(1)
                GPIO.output(12, GPIO.HIGH)
#     def btn_cycle_condition(self):
#     def cycle(self):
#         if self.__position == 0:
#             self.__position = 1
#         elif self.__position == 1:
#             self.position = 2
#         elif self.__position == 2:
#             self.__position = 3
#         elif self.__position == 3:
#             self.__position = 0
#     def cycle(self):
#         if self.position == self.pos_enum.index(self.pos_enum[-1]):
#             self.position = 0
#         else:
#             self.position += 1

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
#         if self.sw == self.__status:
#         # if self.__switch_on_handler is not None:
#             self.__switch_on_handler() 

    # функция, которая применяется позже для изменения состояния лампочек(включает)
    def switch_off(self):
        GPIO.output(self.__gpio_pin, GPIO.LOW)
        self.__status = 0
#         if self.sw == self.__status:
#         # if self.__switch_off_handler is not None:
#             self.__switch_off_handler()
#     def delay1(self):
#         """Задержка для 1 лампочки"""
#         time.sleep(9)
#         
#     def delay2(self):
#         """Задержка для 2 лампочки"""
#         time.sleep(2)

    def toggle(self):
        if self.__status == 0:
            self.switch_on()
        else:
            self.switch_off()

class ButtonView(tk.Tk):
#    __caption1 = "Circle"
#    __caption2 = "Switch"
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
#        self.__caption1 = text
#        self.__caption2 = text
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

class SwitchController:
    
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
            
#     def switch_leds(self):
#         """ Задерживает включение следующей лампочки """
#         if self.__switchModel.get_position() == 1:
#             self.__positionOffLed.switch_off()
#             self.__positionOnLed.delay1()
#             self.__positionOnLed.switch_on()
#         if self.__switchModel.get_position() == 0:
#             self.__positionOnLed.switch_off()
#             self.__positionOffLed.delay2()
#             self.__positionOffLed.switch_on()
            
#     def switch_leds(self):
        """ Задерживает отключение включенной лампочки """
#         if self.__switchModel.get_position() == 1:
#             self.__positionOnLed.delay1()            
#             self.__positionOffLed.switch_off()
#             self.__positionOnLed.switch_on()
#         if self.__switchModel.get_position() == 0:
#             self.__positionOffLed.delay2()
#             self.__positionOnLed.switch_off()
#             self.__positionOffLed.switch_on()

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
        self.__switchModel.btn_switch_condition()
        
#     def handle_button_cycle(self):
#         self.__switchModel.btn_cycle_condition()
#         self.update_leds()

        
        
if __name__ == "__main__":
    
    l1 = LED (12, 1)
    
    l2 = LED (24, 0)
    
    sw = Switch (1, 3, 1)

    sw_ctl = SwitchController(switch = sw, ledOn = l1, ledOff = l2)
    
    sw_ctl.handle_button_switch()
    
    SwitchController(switch = sw, ledOn = l1, ledOff = l2)    
    btVirtual = ButtonView("Circle", "Switch", command1 = sw_ctl.handleClick, command2 = sw_ctl.handleClickSwitch)
    btVirtual.mainloop()
    
    