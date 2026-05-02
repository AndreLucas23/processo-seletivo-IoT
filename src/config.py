FREQUENCY = 1000
PWM_MAX_DUTY = 1023

class Pins:
    I2C_SDA = 21
    I2C_SCL = 22
    LED_RED = 25
    LED_GREEN = 26
    LED_BLUE = 27

class Thresholds:
    ACCEL_DANGER = 2
    ACCEL_DANGER_SINGLE = 1.48
    ACCEL_CRITICAL = 2.8
    ACCEL_CRITICAL_SINGLE = 1.84
    GYRO_DANGER = 150

class Sensitivities:
    ACCEL = 16384
    GYRO = 131
