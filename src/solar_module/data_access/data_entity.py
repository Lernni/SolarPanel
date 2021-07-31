import os
import logging
from datetime import datetime, timedelta

from data_access.globals import DB_PATH
from data_objects.record import Record

class DataEntity:

    DATE_TIME_FORMAT = '%d.%m.%Y %H:%M:%S'

    def __init__(self, name):
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
        self.start_date_time = datetime.strptime(start_date + ' ' + start_time, '%d-%m-%Y %H%M%S')

        end_date = entity_info[4]
        end_time = entity_info[5]
        self.end_date_time = datetime.strptime(end_date + ' ' + end_time, '%d-%m-%Y %H%M%S')

        if self.start_date_time > self.end_date_time:
            raise ValueError("Invalid time frame in entity name")

        # time delta in seconds
        time_delta_seconds = int(datetime.timedelta.total_seconds(self.end_date_time - self.start_date_time))
        self.record_count = time_delta_seconds // self.interval

        # count lines in file
        line_count = sum(1 for _ in open(DB_PATH + "/" + self.name))

        if line_count != self.record_count:
            raise ValueError("Invalid record count in entity")

    def __init__(self, interval = 1):
        self.interval = interval
        self.record_count = 0
        self.name = None
        self.start_date_time = None
        self.end_date_time = None

    def add_records(self, records) -> bool:
        if self.name is None:
            self.start_date_time = records[0].recorded_time
            self.end_date_time = records[-1].recorded_time
            
            self.name = "solarpanel_" + str(self.interval) + "_" + \
                self.start_date_time.strftime('%d-%m-%Y_%H%M%S') + "_" + \
                self.end_date_time.strftime('%d-%m-%Y_%H%M%S') + ".csv"
        else:
            # check if new records are within allowed bounds
            if self.start_date_time > records[0].recorded_time:
                raise ValueError("Records older than begin of entity")
            # latest record must be older all other records of the entity
            if self.end_date_time > records[-1].recorded_time:
                raise ValueError("Records older than end of entity")

            # check if new records follow the exsiting timeline
            new_calculated_from = self.end_date_time + timedelta(seconds = self.interval)
            logging.info(f"berechneter nächster Wert: {new_calculated_from}, nächster Wert: {records[0].recorded_time}")
            if new_calculated_from != records[0].recorded_time:
                raise ValueError("Records do not follow timeline")

            self.end_date_time = records[-1].recorded_time

            old_name = self.name
            self.name = "solarpanel_" + str(self.interval) + "_" + \
                self.start_date_time.strftime('%d-%m-%Y_%H%M%S') + "_" + \
                self.end_date_time.strftime('%d-%m-%Y_%H%M%S') + ".csv"

            # rename old file
            os.rename(str(DB_PATH) + "/" + old_name, str(DB_PATH) + "/" + self.name)

        # add new records to file
        with open(str(DB_PATH) + "/" + self.name, 'a') as f:
            for record in records:
                f.write(record.recorded_time.strftime(DataEntity.DATE_TIME_FORMAT) + "," + str(record.voltage) + ","
                    + str(record.input_current) + "," + str(record.output_current) + "\n")

        self.record_count += len(records)
        return True


    def get_records(self, start_date_time, end_date_time):
        if self.start_date_time is None or self.end_date_time is None or self.name is None:
            raise ValueError("Entity not initialized")
        
        if start_date_time < self.start_date_time or end_date_time > self.end_date_time:
            raise ValueError("time frame outside of entity")

        records = []
        with open(str(DB_PATH) + "/" + self.name, 'r') as f:
            for line in f:
                line_info = line.split(',')
                recorded_time = datetime.strptime(line_info[0], '%d-%m-%Y %H%M%S')
                if start_date_time <= recorded_time <= end_date_time:
                    records.append(
                        Record(interval = self.interval, recorded_time = datetime.strptime(recorded_time, DataEntity.DATE_TIME_FORMAT),
                            voltage = float(line_info[1]), input_current = float(line_info[2]),
                            output_current = float(line_info[3])
                        )
                    )
        
        return records

    def has_date_time(self, date_time):
        if self.start_date_time is None or self.end_date_time is None or self.name is None:
            raise ValueError("Entity not initialized")
        
        return (date_time >= self.start_date_time and date_time <= self.end_date_time)