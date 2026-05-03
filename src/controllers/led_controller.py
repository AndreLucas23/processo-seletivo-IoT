from machine import Pin, PWM

from utils.config import (
    Pins,
    Status,
    Colors,
    FREQUENCY,
    PWM_MAX_DUTY
)

class LedController:
    def __init__(self):
        self.pwm_red = PWM(Pin(Pins.LED_RED),freq=FREQUENCY)
        self.pwm_green = PWM(Pin(Pins.LED_GREEN),freq=FREQUENCY)
        self.pwm_blue = PWM(Pin(Pins.LED_BLUE),freq=FREQUENCY)

    def set_color(self, percent_red, percent_green, percent_blue):
        pwm_red_duty = int(percent_red / 100 * PWM_MAX_DUTY)
        pwm_green_duty = int(percent_green / 100 * PWM_MAX_DUTY)
        pwm_blue_duty = int(percent_blue / 100 * PWM_MAX_DUTY)

        self.pwm_red.duty(pwm_red_duty)
        self.pwm_green.duty(pwm_green_duty)
        self.pwm_blue.duty(pwm_blue_duty)

    def set_color_by_status(self, sensor_status):
        if Status.CRITICAL in sensor_status.values():
            self.set_color(*Colors.RED)
        elif Status.DANGER in sensor_status.values():
            self.set_color(*Colors.YELLOW)
        else:
            self.set_color(*Colors.GREEN)
