import time
import os
from threading import Thread
from datetime import datetime, timedelta
import logging
import collections

import schedule

import data_access.database_handler as db
from config.config import Config
from hardware_access.module import Module
from hardware_access.led_control import LEDControl, LED

class RecordHandler:
    
    read_cache = collections.deque(maxlen = 60)
    recording = False
    write_cache = []
    record_scheduler = None

    def init():
        with Config() as parser:
            if parser.getboolean("system", "recording"):
                RecordHandler.start_recording()

    # control scheduler
    def start_recording():
        if not RecordHandler.recording:
            RecordHandler.recording = True
            RecordHandler.record_scheduler = RecordScheduler()
            RecordHandler.record_scheduler.start()

    def stop_recording():
        if RecordHandler.recording:
            RecordHandler.recording = False
            RecordHandler.record_scheduler.stop()


    # handle requests

    def add_record(record):
        RecordHandler.write_cache.append(record)
        RecordHandler.read_cache.append(record)

    def get_records_from_cache(start_date, end_date):
        read_cache = list(RecordHandler.read_cache)
        requested_records = []
        for i in range(len(read_cache)):
            if start_date <= read_cache[i][0] <= end_date:
                requested_records.append(read_cache[i])

        return read_cache

    def latest(n = 1):
        if n == 1:
            return RecordHandler.read_cache[0]
        elif n > 1:
            end_date = datetime.now()
            start_date = end_date - timedelta(seconds = n)

            return RecordHandler.get_records(start_date, end_date)

    def get_records(start_date, end_date):

        if end_date < start_date:
            raise ValueError("end_date must be greater than start_time")

        buffer_bottom = RecordHandler.read_cache[-1]
        if buffer_bottom is not None:
            buffer_start_date = buffer_bottom.recorded_time.start_date

            if end_date > buffer_start_date:
                # requested time frame is located in cache (or parts of it)

                if start_date >= buffer_start_date:
                    # requested time frame is entirely in cache
                    return RecordHandler.get_records_from_cache(start_date, end_date)
               
                else:
                    # only some of the requested time frame is in cache
                    cache_records = RecordHandler.get_records_from_cache(start_date, end_date)

                    # get remaining records from database
                    db_records = []
                    if start_date < buffer_start_date - timedelta(seconds = 1):
                        db_records = db.get_records(start_date, buffer_start_date - timedelta(seconds = 1))

                    # combine records
                    combined_records = []

                    if len(db_records) > 0:
                        combined_records.extend(db_records)
                        combined_records.extend(cache_records)
                        return combined_records
                    else:
                        return cache_records

        # requested time frame is not in cache, get data from database
        db_records = db.get_records(start_date, end_date)
        return db_records

class RecordScheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.name = "RecordScheduler"

        # run the save_cache operation in extra thread
        # otherwise, scheduler would wait for save_cache to finish, which takes a couple seconds
        # in this time, no record would be created
        
        schedule.every(20).seconds.do(RecordScheduler.run_threaded, self.save_cache)

    def run_threaded(job_func):
        job_thread = Thread(target = job_func, name = "SaveCacheThread")
        job_thread.start()
    
    def run(self):
        while self.running:
            # sleep as long as needed to run at an exact one second interval
            time.sleep(1.0 - time.time() % 1.0)
            self.create_record()
            schedule.run_pending()

    def stop(self):
        self.running = False

    def create_record(self):
        LEDControl.set(LED.YELLOW, True)

        raw_input_record = Module.input_ina.measure()
        raw_output_record = Module.output_ina.measure()

        record = [
            raw_input_record.recorded_time,
            (raw_input_record.voltage + raw_output_record.voltage) / 2,
            raw_input_record.current,
            raw_output_record.current,
            0
        ]

        logging.info("create record...")

        RecordHandler.add_record(record)
        LEDControl.set(LED.YELLOW, False)

    def save_cache(self):
        LEDControl.set(LED.YELLOW, True)

        logging.info("save cache...")

        # remember number of records that will be saved
        # in case of the operation taking a long time, this makes sure no new records are lost

        record_count = len(RecordHandler.write_cache)
        if record_count > 0:
            if db.add_record_list(RecordHandler.write_cache):
                RecordHandler.write_cache = RecordHandler.write_cache[record_count:]

        LEDControl.set(LED.YELLOW, False)

# checks if this thread runs in child process to only start RecordScheduler once
# otherwise RecordScheduler will be initialized twice, resulting in calling save_cache twice

# source: https://stackoverflow.com/a/25519547
# TODO: Check if this test is necessary when flask is active in dev mode

if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    RecordHandler.record_scheduler = RecordScheduler()