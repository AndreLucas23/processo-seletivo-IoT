from machine import Pin, SoftI2C
from time import sleep_ms

from config import Pins

from led_controller import LedController
from sensor_controller import SensorController
from display_controller import DisplayController

i2c = SoftI2C(sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL))

sensor = SensorController(i2c)

display = DisplayController(i2c)

led = LedController()

print('Sensores e atuadores iniciados')

while True:
    try:
        sensor_status = sensor.get_status()
        
        display.show_message_by_status(sensor_status)
        led.set_color_by_status(sensor_status)
    except OSError as error:        
        print('Erro ao ler o sensor: ', error)

    sleep_ms(350)
