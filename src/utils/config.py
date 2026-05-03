FREQUENCY = 1000
PWM_MAX_DUTY = 1023

class Pins:
    I2C_SDA = 21
    I2C_SCL = 22
    LED_RED = 25
    LED_GREEN = 26
    LED_BLUE = 27

class Thresholds:
    ACCEL_DANGER = 1.48
    ACCEL_CRITICAL = 2.4
    ACCEL_CRITICAL_SINGLE = 1.84
    GYRO_DANGER = 149.9
    GYRO_CRITICAL = 330
    GYRO_CRITICAL_SINGLE = 219.9

class Sensitivities:
    ACCEL = 16384
    GYRO = 131

class Status:
    OK = 0
    DANGER = 1
    CRITICAL = 2

class Colors:
    GREEN  = (0, 100, 0)
    YELLOW = (100, 100, 0)
    RED = (100, 0, 0)
