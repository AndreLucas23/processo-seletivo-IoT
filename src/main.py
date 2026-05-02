from machine import Pin, SoftI2C
from time import sleep_ms

from ssd1306 import SSD1306_I2C
from config import Pins, Status

from led_controller import LedController
from sensor_controller import SensorController

i2c = SoftI2C(sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL))

sensor = SensorController(i2c)

oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)

led = LedController()

print('Teste')
print('Sensores e atuadores iniciados')

while True:
    oled.fill(0)
    oled_line_index = 5

    try:
        sensor_status = sensor.get_status()
        accel_status = sensor_status['accel_status']
        gyro_status = sensor_status['gyro_status']

        if accel_status == Status.CRITICAL:
            oled.text('POSSIVEL ACIDENTE', 5, oled_line_index)
            oled_line_index += 30

            led.set_color(100, 0, 0)
        elif accel_status == Status.DANGER:
            oled.text('ACELERACAO PERIGOSA', 5, oled_line_index)
            oled_line_index += 30

            led.set_color(100, 100, 0)
        if gyro_status == Status.DANGER:
            oled.text('GIRO PERIGOSO', 5, oled_line_index)
            oled_line_index += 15

            if accel_status == Status.OK:
                led.set_color(100, 100, 0)

        if (accel_status, gyro_status) == (Status.OK, Status.OK):
            oled.text('Status: OK', 5, oled_line_index)
            oled_line_index += 15

            led.set_color(0, 100, 0)

        oled.show()

    except OSError as error:
        print('Erro ao ler o sensor: ', error)

    oled.show()
    sleep_ms(100)
