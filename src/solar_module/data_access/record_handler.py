import time
import logging
from threading import Thread

import schedule

from data_objects.record_buffer import RecordBuffer
from data_objects.record import Record
from data_access.database_handler import DatabaseHandler
from module import Module

class RecordHandler:
    
    read_cache = RecordBuffer(10)
    recording = False
    write_cache = []
    record_scheduler = None
    cache_scheduler = None


    # control scheduler

    def start_recording():
        if not RecordHandler.recording:
            RecordHandler.recording = True

            DatabaseHandler.new_entity()
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
    
    def latest():
        return RecordHandler.read_cache.top()

    def get_records(start_time, end_time):
        if end_time < start_time:
            raise ValueError("end_time must be greater than start_time")

        buffer_start_time = RecordHandler.read_cache.bottom().record_time

        if end_time > buffer_start_time:
            # requested time frame is located in cache (or parts of it)

            if start_time > buffer_start_time:
                # requested time frame is entirely in cache
                return RecordHandler.read_cache.get_records(start_time, end_time)
            
            else:
                # only some of the requested time frame is in cache
                cache_records = RecordHandler.read_cache.get_records(start_time, end_time)

                # get remaining records from database
                db_records = DatabaseHandler.get_records(start_time, buffer_start_time)

                db_records.extend(cache_records)
                return db_records
        else:
            # requested time frame is not in cache, get data from database
            return DatabaseHandler.get_records(start_time, end_time)

class RecordScheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True

        schedule.every().second.do(self.create_record)
    
    def run(self):
        while self.running:
            schedule.run_pending()

            # sleep as long as needed to run at an exact one second interval
            time.sleep(1.0 - time.time() % 1.0)

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

        schedule.every(20).seconds.do(self.save_cache)
    
    def run(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def save_cache(self):
        logging.info("save cache")

        # remember number of records that will be saved
        # in case of the wire operation taking a long time, this makes sure no new records are lost

        record_count = len(RecordHandler.write_cache)
        if record_count > 0:
            if DatabaseHandler.add_records(RecordHandler.write_cache):
                logging.info(f"new write cache {RecordHandler.write_cache[record_count:]}")
                RecordHandler.write_cache = RecordHandler.write_cache[record_count:]


RecordHandler.record_scheduler = RecordScheduler()
RecordHandler.cache_scheduler = CacheScheduler()