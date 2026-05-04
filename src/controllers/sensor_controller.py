from math import sqrt

from drivers.mpu6050 import accel

from utils.config import (
    Sensitivities,
    Thresholds,
    Status
)

# Cria a classe do controller do sensor MPU5060
class SensorController:
    def __init__(self, i2c):
        self.sensor = accel(i2c)

    # Define a função para extrair os valores de leitura do sensor e
    # processá-los para obter métricas importantes
    def get_metrics(self):
        data = self.sensor.get_values()

        accel_x = data['AcX'] / Sensitivities.ACCEL
        accel_y = data['AcY'] / Sensitivities.ACCEL
        accel_z = data['AcZ'] / Sensitivities.ACCEL

        gyro_x = data['GyX'] / Sensitivities.GYRO
        gyro_y = data['GyY'] / Sensitivities.GYRO
        gyro_z = data['GyZ'] / Sensitivities.GYRO

        accel_total = sqrt(accel_x**2 + accel_y**2 + accel_z**2)
        accel_max = max(abs(accel_x), abs(accel_y), abs(accel_z))
        gyro_total = sqrt(gyro_x**2 + gyro_y**2 + gyro_z**2)
        gyro_max = max(abs(gyro_x), abs(gyro_y), abs(gyro_z))

        return {
            'accel_total': accel_total,
            'accel_max': accel_max,
            'gyro_total': gyro_total,
            'gyro_max': gyro_max,
            'temperature': data['Tmp']
        }

    # Define a função para obter os status do acelerômetro e giroscópio
    # a partir das métricas calculadas pela função get_metrics()
    def get_status(self):
        metrics = self.get_metrics()

        if metrics['accel_total'] > Thresholds.ACCEL_CRITICAL or \
        metrics['accel_max'] > Thresholds.ACCEL_CRITICAL_SINGLE:
            accel_status = Status.CRITICAL
        elif metrics['accel_total'] > Thresholds.ACCEL_DANGER:
            accel_status = Status.DANGER
        else:
            accel_status = Status.OK

        if metrics['gyro_total'] > Thresholds.GYRO_CRITICAL or \
        metrics['gyro_max'] > Thresholds.GYRO_CRITICAL_SINGLE:
            gyro_status = Status.CRITICAL
        elif metrics['gyro_total'] > Thresholds.GYRO_DANGER:
            gyro_status = Status.DANGER
        else:
            gyro_status = Status.OK

        return {
            'accel': accel_status,
            'gyro': gyro_status
        }
