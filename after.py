   def switch_leds(self):
        if self.__switchModel.get_position() == 1:
            self.__positionOffLed.switch_off()
            self.__positionOnLed.delay1()
            self.__positionOnLed.switch_on()
        if self.__switchModel.get_position() == 0:
            self.__positionOnLed.switch_off()
            self.__positionOffLed.delay2()
            self.__positionOffLed.switch_on() 