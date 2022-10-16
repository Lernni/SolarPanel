from datetime import datetime, timedelta, timezone

from flask_restx import Resource
from flask import request

from data_access.database_handler import DatabaseHandler

MAX_RECORDS = 150

class DBRecords(Resource):
  def get(self):
    units = request.args.getlist("units[]")
    
    # convert timestamps from frontend to pandas datetime objects
    start_time = datetime.strptime(request.args.get("start_time"), "%Y-%m-%d_%H-%M")
    end_time = datetime.strptime(request.args.get("end_time"), "%Y-%m-%d_%H-%M")

    # get matching record resolution for request
    time_delta_seconds = int(timedelta.total_seconds(end_time - start_time))
    if time_delta_seconds == 0: return []

    resolution = time_delta_seconds // MAX_RECORDS
    if resolution == 0: resolution = 1

    # get partitions
    partitions = DatabaseHandler.get_partitions(start_time, end_time, resolution)

    # Iterate through all relevant partitions and gather the records in sections
    record_data = {
      "timestamps": [],
      "values": {}
    }

    for partition in partitions:
      new_records = partition.get_records(start_time, end_time)

      record_data["timestamps"].extend(
        int(record.timestamp.replace(tzinfo = timezone.utc).timestamp()) for record in new_records
      )

      for unit in units:
        record_data["values"][unit] = [
          record.data[unit] for record in new_records
        ]

    return record_data