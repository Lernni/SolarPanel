from datetime import datetime

class RawMeasurement:

    def __init__(self, voltage, current):
        self.voltage = voltage
        self.current = current
        self.recorded_time = datetime.now()

    @property
    def power(self):
        return round(self.current * self.voltage, 2)

class Measurement:

    def __init__(self, input_measurement, output_measurement):
        if (isinstance(input_measurement, RawMeasurement) and isinstance(output_measurement, RawMeasurement)):
            self.voltage = round((input_measurement.voltage + output_measurement.voltage) / 2, 2)
            self.input_current = round(input_measurement.current, 2)
            self.ouput_current = round(output_measurement.current, 2)

            # only time of input measurement is used, timing doesn't need to be exactly between measurements
            # could lead to misuse, if input and output measurements have different times
            self.recorded_time = input_measurement.recorded_time
        else:
            raise ValueError('Input and output measurements must be RawMeasurement objects')

    
    def __init__(self, voltage, input_current, ouput_current, recorded_time = None):
        self.voltage = round(voltage, 2)
        self.input_current = round(input_current, 2)
        self.ouput_current = round(ouput_current, 2)

        if recorded_time is None:
            self.recorded_time = datetime.now()
        else:
            self.recorded_time = recorded_time

    @property
    def input_power(self):
        return round(self.input_current * self.voltage, 2)

    @property
    def output_power(self):
        return round(self.ouput_current * self.voltage, 2)


