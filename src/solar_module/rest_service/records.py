from flask_restx import Resource

from data_access.record_handler import RecordHandler

class LatestRecord(Resource):
    def get(self):
        record = RecordHandler.latest()
        return {
            "voltage": record.voltage,
            "input_current": record.input_current,
            "output_current": record.output_current,
            "power": record.output_power,
        }