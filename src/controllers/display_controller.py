from drivers.ssd1306 import SSD1306_I2C

from utils.config import (
    Status,
    DisplayDimensions,
    Text,
    DISPLAY_EMPTY
)

class DisplayController:
    status_msgs = {
        Status.OK: 'OK',
        Status.DANGER: 'PERIGO',
        Status.CRITICAL: 'CRITICO'
    }

    def __init__(self, i2c):
        self.display = SSD1306_I2C(DisplayDimensions.WIDTH, DisplayDimensions.HEIGHT, i2c)
        self.reset_line()

    def show_message_by_status(self, sensor_status):
        self.display.fill(DISPLAY_EMPTY)
        self.reset_line()
    
        self.display.text('ACELEROMETRO:', Text.LINE_OFFSET, self.line_index)
        self.jump_line()

        message = self.status_msgs[sensor_status['accel']]
        self.display.text(message, Text.LINE_OFFSET, self.line_index)
        self.jump_line()

        self.display.text('GIROSCOPIO:', Text.LINE_OFFSET, self.line_index)
        self.jump_line()

        message = self.status_msgs[sensor_status['gyro']]
        self.display.text(message, Text.LINE_OFFSET, self.line_index)
        self.jump_line()

        self.display.show()

    def jump_line(self):
        self.line_index += Text.JUMP_PIXELS

    def reset_line(self):
        self.line_index = Text.LINE_OFFSET
    