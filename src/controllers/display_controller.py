from drivers.ssd1306 import SSD1306_I2C

from utils.config import (
    Status,
    DisplayDimensions,
    Text,
    DISPLAY_EMPTY
)

# Cria a classe do controller do display SSD1306
class DisplayController:
    # Declara as possíveis mensagens a serem mostradas pelo display
    status_msgs = {
        Status.OK: 'OK',
        Status.DANGER: 'PERIGO',
        Status.CRITICAL: 'CRITICO'
    }

    def __init__(self, i2c):
        self.display = SSD1306_I2C(DisplayDimensions.WIDTH, DisplayDimensions.HEIGHT, i2c)
        self.reset_line()

    # Define a função que mostra mensagens no display a partir dos status do acelerômetro e giroscópio
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

    # Define a função para pular o equivalente a uma linha no cursor do display
    def jump_line(self):
        self.line_index += Text.JUMP_PIXELS

    # Define a função para voltar o cursor do display de volta à posição inicial
    def reset_line(self):
        self.line_index = Text.LINE_OFFSET
    