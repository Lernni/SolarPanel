import logging
from flask_restx import Resource

from data_access.record_handler import RecordHandler

class LatestRecord(Resource):
  def get(self):
    record = RecordHandler.latest()
    logging.info("Latest record: %s", record)
    return {
      "voltage": round(record[1], 2),
      "input_current": round(record[2], 2),
      "output_current": round(record[3], 2),
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
      requested_records["voltage"].append(round(record[1], 2))
      requested_records["input_current"].append(round(record[2], 2))
      requested_records["output_current"].append(round(record[3], 2))

    return requested_records