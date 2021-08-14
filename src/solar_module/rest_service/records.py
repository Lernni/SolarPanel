from flask_restx import Resource

from data_access.record_handler import RecordHandler

class LatestRecord(Resource):
    def get(self):
        record = RecordHandler.latest()
        return {
            "voltage": record.voltage,
            "input_current": record.input_current,
            "output_current": record.output_current,
        }

class LatestNRecords(Resource):
    def get(self, n):
        records = RecordHandler.latest(n)

        requested_records = {
            "voltage": [],
            "input_current": [],
            "output_current": [],
        }

        for record in records:
            requested_records["voltage"].append(record.voltage)
            requested_records["input_current"].append(record.input_current)
            requested_records["output_current"].append(record.output_current)

        return requested_records