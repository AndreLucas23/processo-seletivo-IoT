from machine import Pin, SoftI2C, PWM
from time import sleep_ms
from math import sqrt

from mpu6050 import accel
from ssd1306 import SSD1306_I2C
from config import *

def set_led_color(led_red_percent, led_green_percent, led_blue_percent):
    led_red_duty = int(led_red_percent / 100 * 1023)
    led_green_duty = int(led_green_percent / 100 * 1023)
    led_blue_duty = int(led_blue_percent / 100 * 1023)

    led_red.duty(led_red_duty)
    led_green.duty(led_green_duty)
    led_blue.duty(led_blue_duty)

i2c = SoftI2C(sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL))

mpu = accel(i2c)

oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)

led_red = PWM(Pin(Pins.LED_RED), freq=FREQUENCY)
led_green = PWM(Pin(Pins.LED_GREEN), freq=FREQUENCY)
led_blue = PWM(Pin(Pins.LED_BLUE), freq=FREQUENCY)

print('Teste')
print('Sensor MPU6050 iniciado')

while True:
    oled.fill(0)
    oled_line_index = 5

    try:
        mpu_values = mpu.get_values()

        mpu_accel_x = mpu_values['AcX'] / Sensitivities.ACCEL
        mpu_accel_y = mpu_values['AcY'] / Sensitivities.ACCEL
        mpu_accel_z = mpu_values['AcZ'] / Sensitivities.ACCEL

        mpu_gyro_x = mpu_values['GyX'] / Sensitivities.GYRO
        mpu_gyro_y = mpu_values['GyY'] / Sensitivities.GYRO
        mpu_gyro_z = mpu_values['GyZ'] / Sensitivities.GYRO

        mpu_temperature = mpu_values['Tmp']

        accel_total = sqrt(mpu_accel_x**2 + mpu_accel_y**2 + mpu_accel_z**2)
        gyro_total = sqrt(mpu_gyro_x**2 + mpu_gyro_y**2 + mpu_gyro_z**2)
        accel_max = max(abs(mpu_accel_x), abs(mpu_accel_y), abs(mpu_accel_z))

        is_acceleration_critical = False

        if accel_total > Thresholds.ACCEL_CRITICAL or \
        accel_max > Thresholds.ACCEL_CRITICAL_SINGLE:
            oled.text('POSSIVEL IMPACTO', 0, oled_line_index)
            oled_line_index += 15
            oled.text('OU QUEDA', 0, oled_line_index)
            oled_line_index += 30

            led_red_percent, led_green_percent, led_blue_percent = 100, 0, 0
            set_led_color(led_red_percent, led_green_percent, led_blue_percent)

            is_acceleration_critical = True
        elif accel_total > Thresholds.ACCEL_DANGER or \
        accel_max > Thresholds.ACCEL_DANGER_SINGLE:
            oled.text('ACELERACAO', 0, oled_line_index)
            oled_line_index += 15
            oled.text('PERIGOSA', 0, oled_line_index)
            oled_line_index += 30

            led_red_percent, led_green_percent, led_blue_percent = 100, 100, 0
            set_led_color(led_red_percent, led_green_percent, led_blue_percent)

        if gyro_total > Thresholds.GYRO_DANGER:
            oled.text('GIRO PERIGOSO', 0, oled_line_index)
            oled_line_index += 15
            
            if not is_acceleration_critical:
                led_red_percent, led_green_percent, led_blue_percent = 100, 100, 0
                set_led_color(led_red_percent, led_green_percent, led_blue_percent)
            
        if oled_line_index == 5:
            oled.text('STATUS: OK', 0, oled_line_index)

            led_red_percent, led_green_percent, led_blue_percent = 0, 100, 0
            set_led_color(led_red_percent, led_green_percent, led_blue_percent)

    except OSError as error:
        print('Erro ao ler o sensor: ', error)

    oled.show()
    sleep_ms(100)
