from datetime import datetime, timedelta, timezone
import math

from flask_restx import Resource, reqparse

from data_access.database_handler import DatabaseHandler
from globals import MAX_RECORD_COUNT, RESOLUTION_DEPTH


MAX_RECORDS = 150

parser = reqparse.RequestParser()
parser.add_argument("start_time")
parser.add_argument("end_time")
parser.add_argument("units[]", action="append")


class DBRecords(Resource):
  def get(self):
    args = parser.parse_args()
    units = args["units[]"]
    
    # convert timestamps from frontend to pandas datetime objects
    start_time = datetime.strptime(args["start_time"], "%Y-%m-%d_%H-%M")
    end_time = datetime.strptime(args["end_time"], "%Y-%m-%d_%H-%M")

    # get matching record resolution for request
    time_delta_seconds = int(timedelta.total_seconds(end_time - start_time))
    if time_delta_seconds == 0: return []

    resolution = time_delta_seconds // MAX_RECORDS
    if resolution == 0: resolution = 1

    partition_index = math.log2(resolution)

    if not partition_index.is_integer():
      partition_index = int(math.ceil(partition_index))
      resolution = int(math.pow(2, partition_index))

      if partition_index > RESOLUTION_DEPTH:
        partition_index = RESOLUTION_DEPTH
        resolution = MAX_RECORD_COUNT

    partition_index = int(partition_index)


    # get records from db
    sub_partitions = DatabaseHandler.partitions[partition_index]
    if len(sub_partitions) == 0: return []

    start_partition_index = None
    end_partition_index = None

    # Search for partitions that match the time range and mark the first and last match in the list

    for i in range(len(sub_partitions)):
      if sub_partitions[i].start_time >= start_time and sub_partitions[i].start_time <= end_time:
        if start_partition_index is None:
          start_partition_index = i

      elif start_partition_index is not None:
        end_partition_index = i - 1
        break

    # No partition containing the start time means that all partitions are before the start time,
    #   so no partition is included
    # No partition containing the end time means that all partitions after the start partition are included

    if start_partition_index is None: return []
    if end_partition_index is None: end_partition_index = len(sub_partitions) - 1

    # Iterate through all relevant partitions and gather the records in sections

    sections = []
    records = []
    for i in range(start_partition_index, end_partition_index + 1):
      new_records = sub_partitions[i].get_records(start_time, end_time)

      for j in range(len(new_records)):
        record_data = []
        for unit in units:
          record_data.append(new_records[j].data[unit])

        new_records[j] = [int(new_records[j].timestamp.replace(tzinfo = timezone.utc).timestamp())]
        new_records[j].extend(record_data)
          
      if len(records) == 0:
        records = new_records
      elif new_records[0][0] == records[-1][0] + resolution:
        records.extend(new_records)
      else:
        sections.append(records)
        records = new_records

    return sections