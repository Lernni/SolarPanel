from datetime import datetime

from data_objects.date_time_range import DateTimeRange

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
            self.recorded_time = DateTimeRange(input_record.recorded_time, input_record.recorded_time)
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
            now = datetime.now().replace(microsecond = 0)
            self.recorded_time = DateTimeRange(now, now)
        else:
            self.recorded_time = recorded_time

    @property
    def input_power(self):
        return round(self.input_current * self.voltage, 2)

    @property
    def output_power(self):
        return round(self.output_current * self.voltage, 2)

    @property
    def recorded_time_avg(self):
        if self.interval == 1:
            return self.recorded_time.start_date_time
        else:
            return self.recorded_time.average()

    def compress(records, sort = True):
        if sort: records.sort(key = lambda x: x.recorded_time.start_date_time)

        start_date_time = records[0].recorded_time.start_date_time
        end_date_time = records[-1].recorded_time.end_date_time
        recorded_time = DateTimeRange(start_date_time, end_date_time)

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
            interval = len(records) * records[0].interval,
            recorded_time = recorded_time
        )

    def to_dict(self):
        return {
            'voltage': self.voltage,
            'input_current': self.input_current,
            'output_current': self.output_current,
            'interval': self.interval,
            'recorded_time': self.recorded_time
        }