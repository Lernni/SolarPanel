from flask_restx import Resource

from data_access.record_handler import RecordHandler

class LatestRecord(Resource):
    def get(self):
        record = RecordHandler.latest()
        return record.to_dict()

class LatestNRecords(Resource):
    def get(self, n):
        records = RecordHandler.latest(n)
        return [r.to_dict() for r in records]