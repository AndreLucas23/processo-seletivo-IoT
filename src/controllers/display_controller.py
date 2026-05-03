from ssd1306 import SSD1306_I2C

from config import Status

class DisplayController:
    status_msgs = {
        Status.OK: 'OK',
        Status.DANGER: 'PERIGO',
        Status.CRITICAL: 'CRITICO'
    }

    def __init__(self, i2c):
        self.display = SSD1306_I2C(128, 64, i2c)
        self.reset_line()

    def show_message_by_status(self, sensor_status):
        self.display.fill(0)
        self.reset_line()
    
        self.display.text('ACELEROMETRO:', 0, self.line_index)
        self.jump_line()

        message = self.status_msgs[sensor_status['accel']]
        self.display.text(message, 0, self.line_index)
        self.jump_line()

        self.display.text('GIROSCOPIO:', 0, self.line_index)
        self.jump_line()

        message = self.status_msgs[sensor_status['gyro']]
        self.display.text(message, 0, self.line_index)
        self.jump_line()

        self.display.show()

    def jump_line(self):
        self.line_index += 15

    def reset_line(self):
        self.line_index = 5
    