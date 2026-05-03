from machine import Pin, SoftI2C

from utils.config import Pins

from app import App
from controllers.led_controller import LedController
from controllers.sensor_controller import SensorController
from controllers.display_controller import DisplayController

def main():
    i2c = SoftI2C(sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL))

    sensor = SensorController(i2c)

    display = DisplayController(i2c)

    led = LedController()

    print('Sensores e atuadores iniciados')

    app = App(sensor, display, led)
    app.run()

if __name__ == '__main__':
    main()
