from machine import Pin, SoftI2C, PWM
from time import sleep_ms
from math import sqrt
import sys

if '/src' not in sys.path:
    sys.path.append('./src')

from mpu6050 import accel
from ssd1306 import SSD1306_I2C

def set_led_color(led_percent_red, led_percent_green, led_percent_blue):
    led_red_duty = int(led_percent_red / 100 * 1023)
    led_green_duty = int(led_percent_green / 100 * 1023)
    led_blue_duty = int(led_percent_blue / 100 * 1023)

    led_red.duty(led_red_duty)
    led_green.duty(led_green_duty)
    led_blue.duty(led_blue_duty)

FREQUENCY = 1000

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))

mpu = accel(i2c)

oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)

led_red = PWM(Pin(25), freq=FREQUENCY)
led_green = PWM(Pin(26), freq=FREQUENCY)
led_blue = PWM(Pin(27), freq=FREQUENCY)

ACCEL_DANGER_THRESHOLD = 2
ACCEL_SINGLE_DANGER_THRESHOLD = 1.48
ACCEL_CRITICAL_THRESHOLD = 2.8
ACCEL_SINGLE_THRESHOLD = 1.84
GYRO_DANGER_THRESHOLD = 150
ACCEL_SENSITIVITY = 16384
GYRO_SENSITIVITY = 131

print('Teste')
print('Sensor MPU6050 iniciado')

while True:
    oled.fill(0)
    oled_line_index = 5

    try:
        mpu_values = mpu.get_values()

        mpu_accel_x = mpu_values['AcX'] / ACCEL_SENSITIVITY
        mpu_accel_y = mpu_values['AcY'] / ACCEL_SENSITIVITY
        mpu_accel_z = mpu_values['AcZ'] / ACCEL_SENSITIVITY

        mpu_gyro_x = mpu_values['GyX'] / GYRO_SENSITIVITY
        mpu_gyro_y = mpu_values['GyY'] / GYRO_SENSITIVITY
        mpu_gyro_z = mpu_values['GyZ'] / GYRO_SENSITIVITY

        mpu_temperature = mpu_values['Tmp']

        accel_total = sqrt(mpu_accel_x**2 + mpu_accel_y**2 + mpu_accel_z**2)
        gyro_total = sqrt(mpu_gyro_x**2 + mpu_gyro_y**2 + mpu_gyro_z**2)
        accel_max = max(abs(mpu_accel_x), abs(mpu_accel_y), abs(mpu_accel_z))

        is_acceleration_critical = False

        if accel_total > ACCEL_CRITICAL_THRESHOLD or \
        accel_max > ACCEL_SINGLE_THRESHOLD:
            oled.text('POSSIVEL IMPACTO', 0, oled_line_index)
            oled_line_index += 15
            oled.text('OU QUEDA', 0, oled_line_index)
            oled_line_index += 30

            led_percent_red, led_percent_green, led_percent_blue = 100, 0, 0
            set_led_color(led_percent_red, led_percent_green, led_percent_blue)

            is_acceleration_critical = True
        elif accel_total > ACCEL_DANGER_THRESHOLD or \
        accel_max > ACCEL_SINGLE_DANGER_THRESHOLD:
            oled.text('ACELERACAO', 0, oled_line_index)
            oled_line_index += 15
            oled.text('PERIGOSA', 0, oled_line_index)
            oled_line_index += 30

            led_percent_red, led_percent_green, led_percent_blue = 100, 100, 0
            set_led_color(led_percent_red, led_percent_green, led_percent_blue)

        if gyro_total > GYRO_DANGER_THRESHOLD:
            oled.text('GIRO PERIGOSO', 0, oled_line_index)
            oled_line_index += 15
            
            if not is_acceleration_critical:
                led_percent_red, led_percent_green, led_percent_blue = 100, 100, 0
                set_led_color(led_percent_red, led_percent_green, led_percent_blue)
            
        if oled_line_index == 5:
            oled.text('STATUS: OK', 0, oled_line_index)

            led_percent_red, led_percent_green, led_percent_blue = 0, 100, 0
            set_led_color(led_percent_red, led_percent_green, led_percent_blue)

    except OSError as error:
        print('Erro ao ler o sensor: ', error)

    oled.show()
    sleep_ms(100)
