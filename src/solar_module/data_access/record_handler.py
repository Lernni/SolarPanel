import time
import os
from threading import Thread
import collections
import itertools

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
            return RecordHandler.read_cache[-1]
        elif n > 1:
            return list(itertools.islice(
                RecordHandler.read_cache, max(len(RecordHandler.read_cache) - n, 0), len(RecordHandler.read_cache))
            )


class RecordScheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.name = "RecordScheduler"
        self.save_job = None

        # run the save_cache operation in extra thread
        # otherwise, scheduler would wait for save_cache to finish, which takes a couple seconds
        # in this time, no record would be created
        
        self.save_job = schedule.every(20).seconds.do(RecordScheduler.run_threaded, self.save_cache)

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
        schedule.cancel_job(self.save_job)

    def create_record(self):
        LEDControl.set(LED.YELLOW, True)

        raw_input_record = Module.input_ina.measure()
        raw_output_record = Module.output_ina.measure()

        record = [
            raw_input_record.recorded_time,
            (raw_input_record.voltage + raw_output_record.voltage) / 2,
            raw_input_record.current,
            raw_output_record.current,
            float(0)
        ]

        RecordHandler.add_record(record)
        LEDControl.set(LED.YELLOW, False)

    def save_cache(self):
        LEDControl.set(LED.YELLOW, True)

        # remember number of records that will be saved
        # in case of the operation taking a long time, this makes sure no new records are lost

        record_count = len(RecordHandler.write_cache)
        if record_count > 0:
            if db.append_records(RecordHandler.write_cache):
                RecordHandler.write_cache = RecordHandler.write_cache[record_count:]

        LEDControl.set(LED.YELLOW, False)

# checks if this thread runs in child process to only start RecordScheduler once
# otherwise RecordScheduler will be initialized twice, resulting in calling save_cache twice

# source: https://stackoverflow.com/a/25519547
# TODO: Check if this test is necessary when flask is active in dev mode

if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    RecordHandler.record_scheduler = RecordScheduler()