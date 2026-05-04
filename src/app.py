from time import sleep_ms

# Cria a classe App responsável pelo fluxo principal do programa
class App:
    def __init__(self, sensor, display, led):
        self.sensor = sensor
        self.display = display
        self.led = led
        self.running = True

    def run(self):
        while self.running:
            try:
                sensor_status = self.sensor.get_status()

                self.display.show_message_by_status(sensor_status)
                self.led.set_color_by_status(sensor_status)
            except OSError as error:
                print(f'Erro ao ler o sensor: {error}')

            sleep_ms(350)
