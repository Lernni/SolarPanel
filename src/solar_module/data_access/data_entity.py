import os
from datetime import datetime, timedelta

from globals import DB_PATH
from data_objects.record import Record
from data_objects.date_time_range import DateTimeRange

class DataEntity:

    def __init__(self, arg = 1):
        if isinstance(arg, str):
            self.initExistingEntity(arg)
        elif isinstance(arg, int):
            self.initNewEntity(arg)


    def initExistingEntity(self, name):
        self.name = name
        entity_info = self.name.split('.')[0]
        entity_info = entity_info.split('_')

        if len(entity_info) != 6:
            raise ValueError("Invalid entity name")

        if entity_info[0] != 'solarpanel':
            raise ValueError("Invalid entity name")

        self.interval = int(entity_info[1])
        if self.interval < 1:
            raise ValueError("Invalid interval in entity name")

        start_date = entity_info[2]
        start_time = entity_info[3]
        start_date_time = datetime.strptime(start_date + ' ' + start_time, '%d-%m-%Y %H%M%S')

        end_date = entity_info[4]
        end_time = entity_info[5]
        end_date_time = datetime.strptime(end_date + ' ' + end_time, '%d-%m-%Y %H%M%S')

        if start_date_time > end_date_time:
            raise ValueError("Invalid time frame in entity name")

        self.range = DateTimeRange(start_date_time, end_date_time)

        # time delta in seconds
        time_delta_seconds = int(timedelta.total_seconds(end_date_time - start_date_time))
        self.record_count = time_delta_seconds // self.interval

        # count lines in file
        line_count = sum(1 for _ in open(str(DB_PATH) + "/" + self.name)) - 1

        if line_count != self.record_count:
            raise ValueError("Invalid record count in entity")

    def initNewEntity(self, interval = 1):
        self.interval = interval
        self.record_count = 0
        self.name = None
        self.range = None

    def __str__(self):
        return "DataEntity[name = " + (self.name if self.name is not None else "None") \
            + ", interval = " + str(self.interval) \
            + ", range = " + str(self.range if self.range is not None else "None") + "]\n"

    def add_records(self, records) -> bool:
        if len(records) == 0:
            return True

        if self.interval is None:
            self.interval = records[0].interval

        if self.range is None:
            start_date_time = records[0].recorded_time.start_date_time
        else:
            start_date_time = self.range.start_date_time

        end_date_time = records[-1].recorded_time.end_date_time

        self.range = DateTimeRange(start_date_time, end_date_time)

        if self.name is None:
            self.name = "solarpanel_" + str(self.interval) + "_" + \
                start_date_time.strftime('%d-%m-%Y_%H%M%S') + "_" + \
                end_date_time.strftime('%d-%m-%Y_%H%M%S') + ".csv"
        else:
            # check if new records are within allowed bounds
            if start_date_time > records[0].recorded_time.start_date_time:
                raise ValueError("Records older than begin of entity")
            # latest record must be older all other records of the entity
            if end_date_time > records[-1].recorded_time.end_date_time:
                raise ValueError("Records older than end of entity")

            # check if new records follow the exsiting timeline
            # new_calculated_from = end_date_time + timedelta(seconds = self.interval)
            # if new_calculated_from != records[0].recorded_time:
                # raise ValueError("Records do not follow timeline")

            old_name = self.name
            self.name = "solarpanel_" + str(self.interval) + "_" + \
                start_date_time.strftime('%d-%m-%Y_%H%M%S') + "_" + \
                end_date_time.strftime('%d-%m-%Y_%H%M%S') + ".csv"

            # rename old file
            os.rename(str(DB_PATH) + "/" + old_name, str(DB_PATH) + "/" + self.name)

        # add new records to file
        with open(str(DB_PATH) + "/" + self.name, 'a') as f:
            if self.interval == 1:
                for record in records:
                    f.write(str(record.voltage) + "," + str(record.input_current) + ","
                        + str(record.output_current) + ","
                        + "0.0,"
                        + str(int(datetime.timestamp(record.recorded_time.start_date_time))) + "\n")
            else:
                for record in records:
                    f.write(str(record.voltage) + "," + str(record.input_current) + ","
                        + str(record.output_current) + ","
                        + "0.0,"
                        + str(int(datetime.timestamp(record.recorded_time.start_date_time))) + ","
                        + str(int(datetime.timestamp(record.recorded_time.end_date_time))) + "\n")

        self.record_count += len(records)
        return True


    def get_records(self, date_time_range):
        if self.range is None or self.name is None:
            raise ValueError("Entity not initialized")
        
        if not self.range.covers(date_time_range):
            raise ValueError("time frame outside of entity")

        records = []
        with open(str(DB_PATH) + "/" + self.name, 'r') as f:
            for line in f:
                line_info = line.split(',')

                if self.interval == 1:
                    timestamp = datetime.fromtimestamp(int(line_info[4]))
                    recorded_time = DateTimeRange(timestamp, timestamp)
                else:
                    recorded_time = DateTimeRange(
                        datetime.fromtimestamp(int(line_info[4])),
                        datetime.fromtimestamp(int(line_info[5]))
                    )

                if date_time_range.covers(recorded_time):
                    records.append(
                        Record(interval = self.interval, recorded_time = recorded_time,
                            voltage = float(line_info[0]), input_current = float(line_info[1]),
                            output_current = float(line_info[2])
                        )
                    )
        
        return records