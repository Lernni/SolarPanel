from datetime import datetime, timedelta
import os

from globals import DB_PATH
from data_objects.record import Record


class DBPartition:

  '''
  * Handles reading and writing of records into the database as partitions.
  * Partitions are stored as CSV files.
  * The filename contains following metadata:
        - resolution: The resolution of the data in seconds
        - start_time: The start time of the partition
        - end_time: The end time of the partition
        - e.g. solarpanel_128_2022-04-10_17-53-19_2022-04-10_18-50-55.csv
  * All records in a partition are ordered and continuous.
  '''

  def __init__(self, name = None):
    self.name = name
    self.record_count = 0

    if self.name is not None:
      file_info = self.name.split(".")[0]
      file_info = file_info.split("_")

      self.resolution = int(file_info[1])
      self.start_time = datetime.strptime(file_info[2] + '_' + file_info[3], '%Y-%m-%d_%H-%M-%S')
      self.end_time = datetime.strptime(file_info[4] + '_' + file_info[5], '%Y-%m-%d_%H-%M-%S')

      time_delta_seconds = int(timedelta.total_seconds(self.end_time - self.start_time))
      self.record_count = time_delta_seconds // self.resolution


  def add_records(self, records) -> bool:

    '''
    * Adds a list of records to a new or existing partition.
    * The metadata of the partition gets updated.
    '''

    if len(records) == 0: return True
    old_name = self.name

    if self.name is None:
      # Add records to a new partition

      self.start_time = records[0].timestamp
    else:
      # Add records to an existing partition

      expected_next_record_time = self.end_time + timedelta(seconds = self.resolution)
      if records[0].timestamp != expected_next_record_time: return False

    self.resolution = records[0].resolution
    self.end_time = records[-1].timestamp
    self.record_count += len(records)

    self.name = "solarpanel_" \
      + str(self.resolution) \
      + "_" + self.start_time.strftime("%Y-%m-%d_%H-%M-%S") \
      + "_" + self.end_time.strftime("%Y-%m-%d_%H-%M-%S") \
      + ".csv"

    if old_name is not None:
      # Partition file only gets renamed, if it already exists

      os.rename(
        str(DB_PATH) + "/" + str(self.resolution) + "/" + old_name,
        str(DB_PATH) + "/" + str(self.resolution) + "/" + self.name
      )
    
    with open(str(DB_PATH) + "/" + str(self.resolution) + "/" + str(self.name), "a") as file:
      for record in records:
        file.write(record.timestamp.strftime("%d.%m.%Y %H:%M:%S") + "," \
          + str(record.data["voltage"]) + "," \
          + str(record.data["input_current"]) + "," \
          + str(record.data["output_current"]) + "," \
          + str(record.data["soc"]) + "\n"
        )


    return True
    

  def get_records(self, start_time, end_time) -> list:

    '''
    * Returns a list of records from a partition.
    * Returns an empty list, if the partition does not cover the requested time range
      or if the partition does not contain any records.
    '''

    if start_time > self.end_time or end_time < self.start_time: return []

    records = []
    with open(str(DB_PATH) + "/" + str(self.resolution) + "/" + str(self.name), "r") as file:
      for line in file:
        line = line.split(",")
        timestamp = datetime.strptime(line[0], '%d.%m.%Y %H:%M:%S')

        if start_time <= timestamp <= end_time:
          records.append(
            Record(
              timestamp = timestamp,
              data = {
                "voltage": float(line[1]),
                "input_current": float(line[2]),
                "output_current": float(line[3]),
                "soc": float(line[4])
              },
              resolution = self.resolution
            )
          )

    return records


  def get_latest_record(self) -> Record:

    '''
    * Returns the last (newest) record from a partition.
    * Returns None if the partition does not contain any records.
    '''

    if self.record_count == 0: return None

    with open(str(DB_PATH) + "/" + str(self.resolution) + "/" + str(self.name), "rb") as file:

      # see https://stackoverflow.com/a/54278929/8230614

      try:  # catch OSError in case of a one line file 
        file.seek(-2, os.SEEK_END)
        while file.read(1) != b'\n':
          file.seek(-2, os.SEEK_CUR)
      except OSError:
        file.seek(0)

      last_line = file.readline().decode()
      last_line = last_line.split(",")

      return Record(
        timestamp = datetime.strptime(last_line[0], '%d.%m.%Y %H:%M:%S'),
        data = {
          "voltage": float(last_line[1]),
          "input_current": float(last_line[2]),
          "output_current": float(last_line[3]),
          "soc": float(last_line[4])
        },
        resolution = self.resolution
      )
