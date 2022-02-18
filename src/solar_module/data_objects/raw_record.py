from datetime import datetime

class RawRecord:

    def __init__(self, voltage, current):
        self.voltage = voltage
        self.current = current
        self.recorded_time = datetime.now().replace(microsecond = 0)

    @property
    def power(self):
        return round(self.current * self.voltage, 2)