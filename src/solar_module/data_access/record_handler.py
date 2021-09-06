import time
import logging
from threading import Thread
from datetime import datetime, timedelta

import schedule

from data_objects.record_buffer import RecordBuffer
from data_objects.record import Record
from data_objects.date_time_range import DateTimeRange
from data_access.database_handler import DatabaseHandler
from module import Module

class RecordHandler:
    
    read_cache = RecordBuffer(60)
    recording = False
    write_cache = []
    record_scheduler = None
    cache_scheduler = None


    # control scheduler

    def start_recording():
        if not RecordHandler.recording:
            RecordHandler.recording = True

            DatabaseHandler.current_entity_index = None
            RecordHandler.record_scheduler.start()
            RecordHandler.cache_scheduler.start()

    def stop_recording():
        if RecordHandler.recording:
            RecordHandler.recording = False
            RecordHandler.record_scheduler.stop()
            RecordHandler.cache_scheduler.stop()


    # handle requests

    def add_record(record):
        if isinstance(record, Record):
            RecordHandler.write_cache.append(record)
            RecordHandler.read_cache.add(record)
            logging.info(f"Len: Write cache {len(RecordHandler.write_cache)}")
        else:
            raise TypeError("RecordHandler.add() requires a Record object")
    
    def latest(n = 1):
        if n == 1:
            return RecordHandler.read_cache.top()
        elif n > 1:
            end_date_time = datetime.now()
            start_date_time = end_date_time - timedelta(seconds = n)

            return RecordHandler.get_records(DateTimeRange(start_date_time, end_date_time))

    def get_records(date_time_range):
        logging.info(date_time_range)
        end_date_time = date_time_range.end_date_time
        start_date_time = date_time_range.start_date_time

        if end_date_time < start_date_time:
            raise ValueError("end_date_time must be greater than start_time")

        buffer_bottom = RecordHandler.read_cache.bottom()
        logging.info("buffer bottom: " + str(buffer_bottom.recorded_time) if buffer_bottom is not None else "None")
        if buffer_bottom is not None:
            buffer_start_time = buffer_bottom.recorded_time

            if end_date_time > buffer_start_time:
                # requested time frame is located in cache (or parts of it)

                logging.info("start: " + str(start_date_time) + " buffer_start: " + str(buffer_start_time))
                if start_date_time >= buffer_start_time:
                    # requested time frame is entirely in cache
                    logging.info("request entirely in cache")
                    return [RecordHandler.read_cache.get_records(date_time_range)]
                
                else:
                    # only some of the requested time frame is in cache
                    logging.info("only some of the requested time frame is in cache")
                    cache_records = RecordHandler.read_cache.get_records(date_time_range)

                    # get remaining records from database
                    db_records = DatabaseHandler.get_records(DateTimeRange(start_date_time, buffer_start_time - timedelta(seconds = 1)))

                    # combine records
                    last_db_time = db_records[-1].recorded_time
                    first_cache_time = cache_records[0].recorded_time

                    if last_db_time + timedelta(seconds = 1) == first_cache_time:
                        db_records[-1].extend(cache_records)
                    else:
                        db_records.append(cache_records)
                    
                    return db_records

        # requested time frame is not in cache, get data from database
        return DatabaseHandler.get_records(date_time_range)

class RecordScheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.name = "RecordScheduler"

        schedule.every().second.do(self.create_record)
    
    def run(self):
        while self.running:
            # sleep as long as needed to run at an exact one second interval
            time.sleep(1.0 - time.time() % 1.0)

            schedule.run_pending()

    def stop(self):
        self.running = False

    def create_record(self):
        raw_record = Module.input_ina.measure()
        record = Record(
            voltage = raw_record.voltage,
            input_current = raw_record.current,
            output_current = 0,
            recorded_time = raw_record.recorded_time
        )

        RecordHandler.add_record(record)

class CacheScheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.name = "CacheScheduler"

        schedule.every(20).seconds.do(self.save_cache)
    
    def run(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def save_cache(self):
        logging.info("save cache")

        # remember number of records that will be saved
        # in case of the operation taking a long time, this makes sure no new records are lost

        record_count = len(RecordHandler.write_cache)
        if record_count > 0:
            if DatabaseHandler.add_records(RecordHandler.write_cache):
                logging.info(f"new write cache {RecordHandler.write_cache[record_count:]}")
                RecordHandler.write_cache = RecordHandler.write_cache[record_count:]


RecordHandler.record_scheduler = RecordScheduler()
RecordHandler.cache_scheduler = CacheScheduler()