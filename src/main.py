from machine import Pin, SoftI2C

from utils.config import Pins

from app import App
from controllers.led_controller import LedController
from controllers.sensor_controller import SensorController
from controllers.display_controller import DisplayController

# Define a função main responsável por instanciar os controllers e iniciar o fluxo principal do programa
def main():
    # Instancia uma conexão I2C
    i2c = SoftI2C(sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL))

    # Instancia um controller de sensor MPU5060
    sensor = SensorController(i2c)

    # Instancia um controller de display SSD1306
    display = DisplayController(i2c)

    # Instancia um controller de LED RGB
    led = LedController()

    print('Sensores e atuadores iniciados')

    # Instancia uma aplicação do fluxo do programa
    app = App(sensor, display, led)
    # Roda o fluxo principal
    app.run()

if __name__ == '__main__':
    main()
