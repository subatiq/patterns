from threading import Thread
import random
import time

TEMP = 25.0

class Environment(Thread):
    def run(self):
        global TEMP
        while True:
            time.sleep(0.05)
            TEMP += 0.005

class Sensor(Thread):
    def __init__(self) -> None:
        super().__init__()

    def get_current_temperature(self):
        return TEMP


class Heater(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.working = False

    def set_state(self, working: bool) -> None:
        self.working = working

    def run(self) -> None:
        global TEMP
        while True:
            time.sleep(0.01)
            if not self.working:
                continue

            TEMP += random.random() * 0.01


class Cooler(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.working = False

    def set_state(self, working: bool) -> None:
        self.working = working

    def run(self) -> None:
        global TEMP
        while True:
            time.sleep(0.01)
            if not self.working:
                continue

            TEMP -= random.random() * 0.01

class TemperatureControl:
    def __init__(self,
         desired_temperature: float,
         interval: float,
         sensor: Sensor,
         heater: Heater,
         cooler: Cooler,
    ):
        self.desired_temperature = desired_temperature
        self.interval = interval
        self.sensor = sensor
        self.heater = heater
        self.cooler = cooler

    def control_heater(self, temperature):
        if temperature < self.desired_temperature:
            self.heater.set_state(True)
        else:
            self.heater.set_state(False)

    def control_cooler(self, temperature):
        if temperature > self.desired_temperature:
            self.cooler.set_state(True)
        else:
            self.cooler.set_state(False)

        print(self.cooler.working)

    def run(self):
        while True:
            temperature = self.sensor.get_current_temperature()
            self.control_heater(temperature)
            self.control_cooler(temperature)

            print(f'Current temperature: {temperature}°C')
            print(f'Heater: {"On" if self.heater.working else "Off"}')
            print(f'Cooler: {"On" if self.cooler.working else "Off"}')

            time.sleep(self.interval)



if __name__ == "__main__":
    sensor = Sensor()
    heater = Heater()
    cooler = Cooler()

    sensor.start()
    heater.start()
    cooler.start()

    Environment().start()

    temperature_control = TemperatureControl(
        22.0,
        1 / 40,
        sensor,
        heater,
        cooler,
    )

    temperature_control.run()

