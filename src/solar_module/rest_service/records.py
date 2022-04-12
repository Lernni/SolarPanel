from flask_restx import Resource

from data_access.record_handler import RecordHandler

class LatestRecord(Resource):
  def get(self):
    record = RecordHandler.get_latest_record()
    
    return {
      "voltage": round(record.data["voltage"], 2),
      "input_current": round(record.data["input_current"], 2),
      "output_current": round(record.data["output_current"], 2),
    }

class LatestNRecords(Resource):
  def get(self, n):
    records = RecordHandler.get_latest_records(n)

    requested_records = {
      "voltage": [],
      "input_current": [],
      "output_current": [],
    }

    for record in records:
      requested_records["voltage"].append(round(record.data["voltage"], 2))
      requested_records["input_current"].append(round(record.data["input_current"], 2))
      requested_records["output_current"].append(round(record.data["output_current"], 2))

    return requested_records