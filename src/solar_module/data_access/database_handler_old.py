import logging
from datetime import timedelta

from globals import DB_PATH
from data_access.data_entity import DataEntity
from data_objects.date_time_range import DateTimeRange
from data_objects.record import Record

class DatabaseHandler:

  entities = []
  current_entity_index = None
  RECORD_LIMIT = 3600

  def init():

    # check folder structure
    DB_PATH.mkdir(parents = True, exist_ok = True)

    # list of all csv files in folder
    csv_files = [f.name for f in DB_PATH.iterdir() if f.suffix == '.csv']

    # analyze and check database
    for csv_file in csv_files:
      try:
        DatabaseHandler.entities.append(DataEntity(csv_file))
      except ValueError as e:
        logging.info("found corrupted db entity '" + csv_file + "' Error: " + e.args[0])


  def add_entity(entity) -> int:
    DatabaseHandler.entities.append(entity)
    return len(DatabaseHandler.entities) - 1


  def add_records(records) -> bool:
    if len(records) == 0:
      return True

      # check interval
      # if interval is 1 -> continuous saving
      
    if records[0].interval == 1:
      if DatabaseHandler.current_entity_index is None:
        DatabaseHandler.current_entity_index = DatabaseHandler.add_entity(DataEntity())

      if DatabaseHandler.entities[DatabaseHandler.current_entity_index].record_count == DatabaseHandler.RECORD_LIMIT:
        DatabaseHandler.current_entity_index = DatabaseHandler.add_entity(DataEntity())

      current_entity = DatabaseHandler.entities[DatabaseHandler.current_entity_index]

      if current_entity.record_count + len(records) < DatabaseHandler.RECORD_LIMIT:
        return current_entity.add_records(records)
      else:
        place_remaining = DatabaseHandler.RECORD_LIMIT - current_entity.record_count
        current_entity.add_records(records[:place_remaining])

        # copy the last record of the current entity to a new entity
        # this prevents one second gaps in requested record data

        place_remaining -= 1
        records = records[place_remaining:]
        return DatabaseHandler.add_records(records)

    else:

      # if interval is greater than 1
      # -> check if time span and interval already exists in database
      # -> if not, create new entity and add records

      sorted_entities = sorted(DatabaseHandler.entities, key = lambda e: e.interval, reverse = True)

      for entity in sorted_entities:

        if entity.interval < records[0].interval: break
        if entity.interval != records[0].interval: continue

        record_range = DateTimeRange(records[0].recorded_time.start_date_time, records[-1].recorded_time.end_date_time)
        if entity.range.intersect(record_range) is None: continue

        # range already exists
        if entity.range.covers(record_range): return False

        # range exists partially
        remaining_range = entity.range.split_merge(record_range, subtract = True)[0]
        new_records = [record for record in records if remaining_range.covers(record.recorded_time)]
        return DatabaseHandler.add_records(new_records)

      # range does not exist -> create new entity and add records
      new_entity = DataEntity(records[0].interval)
      new_entity.add_records(records)
      DatabaseHandler.add_entity(new_entity)
      return True
        

  def get_records(date_time_range, interval = 1):

    logging.info(f"handle request for time frame {date_time_range} with interval {interval} ...")
    logging.info("# 1 - fill time frame with records...")

    requested_records = []

    end_date_time = date_time_range.end_date_time
    start_date_time = date_time_range.start_date_time

    sorted_entities = sorted(DatabaseHandler.entities, key = lambda e: e.interval, reverse = True)

    for entity in sorted_entities:
      if entity.range.start_date_time > end_date_time or \
        entity.range.end_date_time < start_date_time or \
        entity.interval > interval or \
        ((interval % entity.interval) != 0): continue

      fillable_range = date_time_range.intersect(entity.range)
      available_records = entity.get_records(fillable_range)

      if len(requested_records) == 0:
        requested_records.extend(available_records)
        logging.info(f"inserted {len(available_records)} records from entity '{entity.name}' with interval {entity.interval}")
      else:
        i = j = n = 0
        while i < len(requested_records) and len(available_records) > 0:

          found_gap = False

          if i == 0:
            found_gap = requested_records[0].recorded_time.start_date_time > available_records[j].recorded_time.end_date_time  
          elif i < len(requested_records) - 1:
            found_gap = (requested_records[i].recorded_time.end_date_time < available_records[j].recorded_time.start_date_time and \
            requested_records[i + 1].recorded_time.start_date_time > available_records[j].recorded_time.end_date_time)
          else: # i == len(requested_records) - 1
            found_gap = requested_records[i].recorded_time.end_date_time < available_records[j].recorded_time.start_date_time  

          if found_gap:
            if i != len(requested_records) - 1:
              if i != 0: i += 1
              requested_records.insert(i, available_records.pop(j))
              i += 1
              n += 1

              while len(available_records) > 0 and \
                requested_records[i].recorded_time.start_date_time > available_records[j].recorded_time.end_date_time:
                  requested_records.insert(i, available_records.pop(j))
                  i += 1
                  n += 1
            else:
              requested_records.extend(available_records)
              n += len(available_records)
              available_records = []
          else:
            if requested_records[i].recorded_time.end_date_time >= available_records[j].recorded_time.start_date_time:
              del available_records[j]
            else:
              i += 1

        logging.info(f"inserted {n} records from entity '{entity.name}' with interval {entity.interval}")


    logging.info("# 2 - compress records to requested interval...")

    i = 1
    record_frame = []
    while i < interval:

      logging.info(f"compressing on interval {i}...")
      j = 0

      while j <= len(requested_records):
        if len(record_frame) == 0:
          if j == len(requested_records): break
          if requested_records[j].interval != i:
            j += 1
            continue

        # get all records that have the same interval and that create a continuos timeline with no gaps

        if len(record_frame) == 0 or j != len(requested_records) and \
          (requested_records[j].recorded_time.start_date_time == record_frame[-1].recorded_time.end_date_time or \
          requested_records[j].recorded_time.start_date_time - timedelta(seconds = 1) == record_frame[-1].recorded_time.end_date_time) and \
          requested_records[j].interval == i:
            record_frame.append(requested_records.pop(j))
        else:
          
          # continous timeline of records with same interval is broken
          # -> compress records according to neighbour records intveral

          # check if record_frame is compressable
          if len(record_frame) <= 1:
            record_frame = []
            j += 1
            continue

          logging.info(f"found {len(record_frame)} records to compress")

          # when the neighbour interval is the current interval, there must be gap between the records
          # (all continous records with the same interval are already inside the record frame)
          # if the neighbour interval is not divisable by the current interval, the neighbour can't be used
          # (e.g. requested interval is 12, neighbour interval is 4, current interval is 3 -> neighbour can't be used)
          # if the neighbour interval is smaller than the current interval, the neighbour can't be used

          # get neighbour intervals
          if j == 0 or requested_records[j - 1].interval <= i or \
            ((requested_records[j - 1].interval % i) != 0):
              left_neighbour_interval = None
          else:
            left_neighbour_interval = requested_records[j - 1].interval

          if j >= len(requested_records) - 1: right_neighbour_interval = None
          elif requested_records[j + 1].interval <= i or \
            ((requested_records[j + 1].interval % i) != 0):
              right_neighbour_interval = None
          else:
            right_neighbour_interval = requested_records[j + 1].interval


          # decide which neighbour interval to use
          compress_direction = "L"
          if (left_neighbour_interval is None and right_neighbour_interval is None):
            leading_interval = next_interval(i, interval)

          elif left_neighbour_interval is None:
            leading_interval = right_neighbour_interval
            compress_direction = "R"

          elif right_neighbour_interval is None:
            leading_interval = left_neighbour_interval
            compress_direction = "L"

          else:
            leading_interval = min(left_neighbour_interval, right_neighbour_interval)
            compress_direction = "L" if left_neighbour_interval == leading_interval else "R"

          # compress records according to the chosen neighbour interval
          record_step = leading_interval // i
          compressed_records = compress_records(record_frame, record_step, compress_direction)

          logging.info(f"minimized record count by {len(record_frame) - len(compressed_records)}, " 
            + f"while compressing records from interval {i} to {leading_interval}")
          
          # insert compressed records back into requested_records
          for record in compressed_records:
            requested_records.insert(j, record)
            j += 1

          record_frame = []

      i += 1

    logging.info("# 3 - group continous time frames in sub-lists...")

    i = 0
    record_frame = []
    while i < len(requested_records):
      if len(record_frame) == 0 or \
        (requested_records[i].recorded_time.start_date_time == record_frame[-1].recorded_time.end_date_time or \
        requested_records[i].recorded_time.start_date_time - timedelta(seconds = 1) == record_frame[-1].recorded_time.end_date_time):
          record_frame.append(requested_records.pop(i))
      else:
        requested_records.insert(i, record_frame)
        record_frame = []
        i += 1

    requested_records.insert(i, record_frame)

    logging.info(f"number of grouped sub-lists: {len(requested_records)}")
      

    logging.info("# 4 - save new calculated time frames in database...")

    if len(requested_records) > 0 and interval != 1:
      for frame in requested_records:
        if len(frame) > 1:
            DatabaseHandler.add_records(frame)

    return requested_records


def compress_records(records, record_step, compress_direction = "L"):
  if record_step > len(records):
    return [Record.compress(records)]

  compress_iterations = len(records) // record_step
  record_offset = len(records) % record_step
  compressed_records = []

  for i in range(compress_iterations):
    if compress_direction == "L":
      compressed_records.append(Record.compress(records[i * record_step : (i + 1) * record_step]))
      if record_offset != 0 and i == compress_iterations - 1:
        compressed_records.append(Record.compress(records[-record_offset:]))
    else:
      if i == 0 and record_offset != 0:
        compressed_records.append(Record.compress(records[:record_offset]))
      else:
        compressed_records.append(Record.compress(records[record_offset + i * record_step : record_offset + (i + 1) * record_step]))

  return compressed_records


def next_interval(number, requested_interval):
  if number == 0 or number > requested_interval:
    return 1

  if number == requested_interval:
    return requested_interval

  for i in range(number + 1, requested_interval + 1):
    if (requested_interval % i) == 0 and (i % number) == 0:
      return i

  return requested_interval