from datetime import timedelta
from threading import Thread
import time

from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS
import schedule
import logging

from data_access.database_handler import DatabaseHandler
from data_access.record_handler import RecordHandler
from submodules.ina219_module import INA219Module
from data_objects.record import Record

app = Flask(__name__)
CORS(app)
api = Api(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d.%m.%Y %I:%M:%S %p"
)
logging.info("test")

ina = INA219Module(0.1, "Test Module")
DatabaseHandler.init()
RecordHandler.start_recording()


class TaskScheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True

        schedule.every().second.do(self.record_update)

    def run(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1.0 - time.time() % 1.0)

    def stop(self):
        self.running = False

    def record_update(self):
        raw_record = ina.measure()
        record = Record(
            voltage = raw_record.voltage,
            input_current = raw_record.current,
            output_current = 0,
            recorded_time = raw_record.recorded_time
        )

        RecordHandler.add_record(record)

TaskScheduler().start()

class LatestRecord(Resource):
    def get(self):
        record = RecordHandler.latest()
        return {
            "voltage": record.voltage,
            "input_current": record.input_current,
            "output_current": record.output_current,
            "power": record.output_power,
        }

api.add_resource(LatestRecord, '/latest')

if __name__ == '__main__':
    app.run(debug=True)
