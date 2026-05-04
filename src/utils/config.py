# Constantes únicas
FREQUENCY = 1000
PWM_MAX_DUTY = 1023
PERCENTAGE_MAX = 100
DISPLAY_EMPTY = 0

# Números dos pinos do programa
class Pins:
    I2C_SDA = 21
    I2C_SCL = 22
    LED_RED = 25
    LED_GREEN = 26
    LED_BLUE = 27

# Limites de faixas de perigo do sensor
class Thresholds:
    ACCEL_DANGER = 1.48
    ACCEL_CRITICAL = 2.4
    ACCEL_CRITICAL_SINGLE = 1.84
    GYRO_DANGER = 149.9
    GYRO_CRITICAL = 330
    GYRO_CRITICAL_SINGLE = 219.9

# Valores a transformar valores lidos
class Sensitivities:
    ACCEL = 16384
    GYRO = 131

# Status de acelerômetro e giroscópio
class Status:
    OK = 0
    DANGER = 1
    CRITICAL = 2

# Porcentagens de cores a serem mostradas no LED
class Colors:
    GREEN  = (0, 100, 0)
    YELLOW = (100, 100, 0)
    RED = (100, 0, 0)

# Dimensões do display SSD1306
class DisplayDimensions:
    WIDTH = 128
    HEIGHT = 64

# Predefinições de linha e coluna do display
class Text:
    LINE_OFFSET = 5
    JUMP_PIXELS = 15
