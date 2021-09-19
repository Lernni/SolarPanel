import json
from datetime import datetime

from flask_restx import Resource, reqparse

from data_access.database_handler import DatabaseHandler
from data_objects.date_time_range import DateTimeRange

parser = reqparse.RequestParser()
parser.add_argument("range")
parser.add_argument("units[]", action="append")
parser.add_argument("interval", type=int)

def wrap_records(records, units):
  wrapped_data = {
      "time": []
    }

  requested_frame = {
    "time": []
  }

  for unit in units:
    wrapped_data[unit] = []
    requested_frame[unit] = []

  for record_frame in records:
    for record in record_frame:
      requested_frame["time"].append(datetime.timestamp(record.recorded_time_avg) * 1000)
      for unit in units:
        requested_frame[unit].append(getattr(record, unit))

    wrapped_data["time"].append(requested_frame["time"])
    requested_frame["time"] = []

    for unit in units:
      wrapped_data[unit].append(requested_frame[unit])
      requested_frame[unit] = []

  return wrapped_data


class DBRecords(Resource):
  def get(self):
    args = parser.parse_args()
    date_time_range = json.loads(args["range"])
    units = args["units[]"]
    interval = args["interval"]

    records = DatabaseHandler.get_records(
      DateTimeRange(datetime.fromtimestamp(date_time_range["min"] / 1000), datetime.fromtimestamp(date_time_range["max"] / 1000)),
      interval
    )

    return wrap_records(records, units)