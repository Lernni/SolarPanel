from datetime import datetime
import logging

class RawRecord:

    def __init__(self, voltage, current):
        self.voltage = voltage
        self.current = current
        self.recorded_time = datetime.now().replace(microsecond = 0)

    @property
    def power(self):
        return round(self.current * self.voltage, 2)

class Record:

    def __init__(self, input_record, output_record):
        if (isinstance(input_record, RawRecord) and isinstance(output_record, RawRecord)):
            self.voltage = round((input_record.voltage + output_record.voltage) / 2, 2)
            self.input_current = round(input_record.current, 2)
            self.output_current = round(output_record.current, 2)
            self.interval = 1

            # only time of input record is used, timing doesn't need to be exactly between records
            # could lead to misuse, if input and output records have different times
            self.recorded_time = input_record.recorded_time
        else:
            raise ValueError('Input and output records must be RawRecord objects')

    
    def __init__(self, voltage, input_current, output_current, interval = 1, recorded_time = None):
        self.voltage = round(voltage, 2)
        self.input_current = round(input_current, 2)
        self.output_current = round(output_current, 2)

        if interval < 1:
            raise ValueError('Interval must be greater than 1')

        self.interval = interval

        if recorded_time is None:
            self.recorded_time = datetime.now().replace(microsecond = 0)
        else:
            self.recorded_time = recorded_time

    @property
    def input_power(self):
        return round(self.input_current * self.voltage, 2)

    @property
    def output_power(self):
        return round(self.output_current * self.voltage, 2)

    def compress(records, sort = True):
        if sort: records.sort(key = lambda x: x.recorded_time)

        start_date_time = records[0].recorded_time
        end_date_time = records[-1].recorded_time

        average_delta = (end_date_time - start_date_time) / 2
        average_date_time = start_date_time + average_delta

        average_voltage = 0
        average_input_current = 0
        average_output_current = 0

        for record in records:
            average_voltage += record.voltage
            average_input_current += record.input_current
            average_output_current += record.output_current

        average_voltage /= len(records)
        average_input_current /= len(records)
        average_output_current /= len(records)

        return Record(
            average_voltage,
            average_input_current,
            average_output_current,
            interval = len(records),
            recorded_time = average_date_time
        )