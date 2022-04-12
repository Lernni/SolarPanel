from pathlib import Path
import math
from datetime import timedelta

from globals import DB_PATH, RESOLUTION_DEPTH, MAX_RECORDS_PER_PARTITION
from data_objects.record import Record
from data_access.database_partition import DBPartition


class DatabaseHandler:

  partitions = [[] for _ in range(RESOLUTION_DEPTH + 1)]
  
  def init():

    '''
    * Creates dir structure for database
    * Loads metadata of all existing partitions
    '''

    DB_PATH.mkdir(parents = True, exist_ok = True)

    for i in range(RESOLUTION_DEPTH + 1):
      resolution_db_path = Path(DB_PATH, str(int(math.pow(2, i))))
      resolution_db_path.mkdir(parents = True, exist_ok = True)

      csv_files = [f.name for f in resolution_db_path.iterdir() if f.suffix == '.csv']
      csv_files.sort()

      for csv_file in csv_files:
        DatabaseHandler.partitions[i].append(DBPartition(csv_file))

  
  def add_records(records):

    '''
    * Adds list of records to the database
    * Decides which partition to add the records to
    '''

    if len(records) == 0: return True

    partition_index = int(math.log2(records[0].resolution))

    if len(DatabaseHandler.partitions[partition_index]) == 0:
      # There are no partitions for this resolution yet

      DatabaseHandler.partitions[partition_index].append(DBPartition())

    partition = DatabaseHandler.partitions[partition_index][-1]
    if partition.record_count + len(records) <= MAX_RECORDS_PER_PARTITION:
      # The last partition has enough space to add all records

      if not partition.add_records(records):
        # Records could not be added to partition, so create a new partition
        # Adding records fails, if the new records do not follow the old ones

        DatabaseHandler.partitions[partition_index].append(DBPartition())
        DatabaseHandler.add_records(records)
    else:
      # The last partition does not have enough space to add all records
      # Only add as much records as possible to the last partition
      # Create a new partition with the remaining records

      cut_index = MAX_RECORDS_PER_PARTITION - partition.record_count

      if not partition.add_records(records[:cut_index]):
        # Records could not be added to partition, so create a new partition
        # Adding records fails, if the new records do not follow the old ones

        DatabaseHandler.partitions[partition_index].append(DBPartition())
        DatabaseHandler.add_records(records)
      else:
        # Add the remaining records to a new partition

        DatabaseHandler.partitions[partition_index].append(DBPartition())
        DatabaseHandler.add_records(records[cut_index:])

  
  def get_latest_record(resolution) -> Record:

    '''
    * Returns the newest record from the database for a given resolution
    '''

    partition_index = int(math.log2(resolution))

    if len(DatabaseHandler.partitions[partition_index]) == 0: return None

    partition = DatabaseHandler.partitions[partition_index][-1]
    if partition.record_count == 0: return None

    return partition.get_latest_record()
