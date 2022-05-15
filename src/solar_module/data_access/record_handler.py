import time
from threading import Thread
import logging
import math

import schedule

from data_access.database_handler import DatabaseHandler
from data_access.capacity_correction import CapacityCorrection
from data_objects.record import Record
from config.config import Config
from hardware_access.module import Module
from hardware_access.led_control import LEDControl, LED
from globals import RESOLUTION_DEPTH, MAX_CACHE_SIZE, MAX_RECORD_COUNT, LOW_BATTERY_THRESHOLD, CORRECTION_INTERVAL


class RecordScheduler(Thread):

  '''
  * Schedules creation of new records exactly once per second
  * Schedules capacity correction every 5 minutes
  '''

  def __init__(self, job):
    Thread.__init__(self)
    self.name = "RecordScheduler"
    self.running = True
    self.job = job

    self.capacity_correction_job = schedule.every(CORRECTION_INTERVAL).seconds.do(
      RecordScheduler.run_threaded, RecordHandler.run_capacity_correction
    )
  
  
  def run_threaded(job_func):
    job_thread = Thread(target = job_func, name = "ThreadedJob")
    job_thread.start()

  def run(self):
    while self.running:
      # sleep as long as needed to run at an exact one second interval
      th = Thread(target = self.job, name = "RecordSchedulerJob")
      th.start()

      schedule.run_pending()
      time.sleep(1.0 - time.time() % 1.0)

  def stop(self):
    self.running = False
    schedule.cancel_job(self.capacity_correction_job)

# checks if this thread runs in child process to only start RecordScheduler once
# otherwise RecordScheduler will be initialized twice

# source: https://stackoverflow.com/a/25519547
# TODO: Check if this test is necessary when flask is active in dev mode

# if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
#     RecordHandler.record_scheduler = RecordScheduler()


class RecordHandler:

  '''
  * Creates records every second and stores them in cache.
  * Does incrementell calculation of lower resolution records.
  * Provides latest "live" data of records.
  * State can be handled by system config.
  '''

  record_cache = [[] for _ in range(RESOLUTION_DEPTH + 1)]
  record_count = 0
  recording = False
  record_scheduler = None

  current_capacity = None
  current_soc = None
  capacity_correction = 0.0
  old_capacity = 0.0
  old_soc = 0.0
  charging_level = 0


  def init():

    '''
    * Initializes the record handler.
    * Starts recording according to the config file.
    '''

    with Config() as parser:
      if parser.getboolean("system", "recording"):
        RecordHandler.start_recording()


  def start_recording():

    '''
    * If not already recording, starts recording.
    * Resets record cache and record count.
    * Loads capacity and soc from config.
    '''

    logging.info("start recording...")

    if not RecordHandler.recording:
      RecordHandler.record_cache = [[] for _ in range(RESOLUTION_DEPTH + 1)]
      RecordHandler.record_count = 0
      RecordHandler.record_scheduler = RecordScheduler(RecordHandler.create_record)

      with Config() as parser:
        RecordHandler.current_capacity = parser.getfloat("battery_state", "capacity")
        RecordHandler.current_soc = parser.getfloat("battery_state", "soc")
        RecordHandler.capacity_correction = parser.getfloat("battery_state", "capacity_correction")

      RecordHandler.record_scheduler.start()
      RecordHandler.recording = True


  def stop_recording():

    '''
    * If recording, stops recording.
    * Saves the remaining cache to the database.
    '''

    logging.info("stop recording...")

    if RecordHandler.recording:
      RecordHandler.record_scheduler.stop()
      RecordHandler.save_cache(half = False)
      RecordHandler.recording = False


  def get_latest_record(resolution: int = 1) -> Record:

    '''
    * Returns the latest record with given resolution from cache.
    '''

    cache_index = int(math.log2(resolution))
    return RecordHandler.record_cache[cache_index][-1]

  def get_latest_records(n: int, resolution: int = 1):
      
    '''
    * Returns the latest n records with given resolution from cache.
    '''

    cache_index = int(math.log2(resolution))
    if 1 <= n <= len(RecordHandler.record_cache[cache_index]):
      return RecordHandler.record_cache[cache_index][-n:]
    elif n > len(RecordHandler.record_cache[cache_index]):
      return RecordHandler.record_cache[cache_index]


  def add_record(record: Record):

    '''
    * Adds given record to cache and its lower resolution versions, if possible.
    * If the cache is full, first half of the cache will be saved.
    '''

    # add record to the appropriate sub-list in the cache
    # the sub-list is determined by the resolution of the record
    # all possible resolutions are multiples of 2, so log base 2
    #   of the record resolution sorts the records in sub-lists accordingly
    
    try:
      cache_index = int(math.log2(record.resolution))
      RecordHandler.record_cache[cache_index].append(record)
    except:
      logging.error("record resolution not supported!")
      logging.error("record_resolution: " + str(record.resolution))
      logging.error("cache_index: " + str(cache_index))

    if record.resolution == 1:
      RecordHandler.record_count += 1


    # if the record_count is divisible by the next lower record resolution of the current record,
    #   there must be at least two records with the current resolution that can be averaged to
    #   create a new record with the next lower resolution
    # Ideally both records are in cache, so no reading from the database is necessary
    # If not, at least one record is guaranteed to be in cache (it's the record that was added just now),
    #   the other must be read from the db
    # In general, records only need to be read from the db if the cache was previously saved
    # To reduce necessary db reads, only the first half of the cache is saved, so there is a buffer
    #   for calculating lower resolution records

    if (RecordHandler.record_count % (record.resolution * 2) == 0) and ((record.resolution * 2) <= MAX_RECORD_COUNT):
      # There are two records with the current resolution, so they can be averaged

      other_record = None
      averaged_record = None

      if len(RecordHandler.record_cache[cache_index]) >= 2:
        # Both records are in cache
        try:
          other_record = RecordHandler.record_cache[cache_index][-2]
        except:
          logging.error("could not get other record from cache!")
          logging.error("cache_index: " + str(cache_index))
          logging.error("record_count: " + str(RecordHandler.record_count))
          logging.error("record_cache: " + str(RecordHandler.record_cache))
          logging.error("record_resolution: " + str(record.resolution))

      else:
        # The other record is not in cache, so it must be read from the db
        try:
          other_record = DatabaseHandler.get_latest_record(record.resolution)
        except:
          logging.error("could not get other record from db!")
          logging.error("cache_index: " + str(cache_index))
          logging.error("record_count: " + str(RecordHandler.record_count))
          logging.error("record_cache: " + str(RecordHandler.record_cache))
          logging.error("record_resolution: " + str(record.resolution))
      
      try:
        averaged_record = Record(
          timestamp = other_record.timestamp,
          data = {
            "voltage": round((other_record.data["voltage"] + record.data["voltage"]) / 2, 2),
            "input_current": round((other_record.data["input_current"] + record.data["input_current"]) / 2, 2),
            "output_current": round((other_record.data["output_current"] + record.data["output_current"]) / 2, 2),
            "soc": round((other_record.data["soc"] + record.data["soc"]) / 2, 2)
          },
          resolution = record.resolution * 2
        )
      except:
        logging.error("could not average records!")
        logging.error("record.timestamp: " + str(record.timestamp))
        logging.error("other_record.timestamp: " + str(other_record.timestamp))
        logging.error("record_count: " + str(RecordHandler.record_count))

      
      # Add the averaged record of lower resolution to the cache recursively
      # The recursive call allows even lower resolution records to be added to the cache, if possible

      RecordHandler.add_record(averaged_record)


    if RecordHandler.record_count == MAX_RECORD_COUNT:
      # Record count reached value to calculate the lowest resolution record
      logging.info("record count reached maximum, resetting...")

      RecordHandler.record_count = 0
    

    if len(RecordHandler.record_cache[0]) == MAX_CACHE_SIZE:
      # First half of the cache will be saved to the database
      logging.debug("cache reached maximum, saving the first half...")

      RecordHandler.save_cache(half = True)


  def save_cache(half: bool):

    logging.debug("saving cache...")
    
    '''
    * Saves half or all of the cache to the database.
    * The saved parts of the cache will be deleted afterwards.
    '''

    if half:
      try:
        for i in range(len(RecordHandler.record_cache)):
          if len(RecordHandler.record_cache[i]) == 1:
            DatabaseHandler.add_records([RecordHandler.record_cache[i][0]])
            RecordHandler.record_cache[i] = []

          elif len(RecordHandler.record_cache[i]) > 1:
            DatabaseHandler.add_records(RecordHandler.record_cache[i][:len(RecordHandler.record_cache[i]) // 2])
            RecordHandler.record_cache[i] = RecordHandler.record_cache[i][len(RecordHandler.record_cache[i]) // 2:]
          else:
            break
      except:
        logging.error("could not save half of cache!")
        logging.error("len(RecordHandler.record_cache): " + str(len(RecordHandler.record_cache)))
        logging.error("i: " + str(i))
        logging.error("len(RecordHandler.record_cache[i])", str(len(RecordHandler.record_cache[i])))
        logging.error("record_count: " + str(RecordHandler.record_count))

    else:
      try:
        for sub_list in RecordHandler.record_cache:
          if len(sub_list) != 0:
            DatabaseHandler.add_records(sub_list)
          else:
            break
      except:
        logging.error("could not save cache!")
        logging.error("len(RecordHandler.record_cache): " + str(len(RecordHandler.record_cache)))
        logging.error("record_count: " + str(RecordHandler.record_count))

      RecordHandler.record_cache = [[] for _ in range(RESOLUTION_DEPTH + 1)]


  def create_record():

    '''
    * Creates a new record by measuring the current and voltage of the solar module.
    * The yellow LED will be turned on for the duration of the measurement and processing.
    '''

    logging.debug("creating record...")

    LEDControl.set(LED.YELLOW, True)

    # measure voltage and current
    try:
      input_record = Module.input_ina.measure()
      output_record = Module.output_ina.measure()
    except: 
      logging.error("failed to measure input and output current!")

    # calculate state of charge (soc) and capacity
    try:
      current_difference = (input_record.current - RecordHandler.capacity_correction - output_record.current) / 3600
    except:
      logging.error("failed to calculate current difference!")
      logging.error("input_record.current: " + str(input_record.current))
      logging.error("RecordHandler.capacity_correction: " + str(RecordHandler.capacity_correction))
      logging.error("output_record.current: " + str(output_record.current))
    
    try:
      RecordHandler.current_soc += current_difference

      if RecordHandler.current_soc > RecordHandler.current_capacity:
        RecordHandler.current_capacity = RecordHandler.current_soc

      if RecordHandler.current_soc < 0:
        RecordHandler.current_capacity += abs(RecordHandler.current_soc)
        RecordHandler.current_soc = 0.0
    except:
      logging.error("failed to calculate current state of charge!")
      logging.error("current_difference: " + str(current_difference))
      logging.error("RecordHandler.current_soc: " + str(RecordHandler.current_soc))
      logging.error("RecordHandler.current_capacity: " + str(RecordHandler.current_capacity))

    # create record with new data and add it to cache

    try:
      record = Record(
        timestamp = input_record.recorded_time,
        data = {
          "voltage": round((input_record.voltage + output_record.voltage) / 2, 2),
          "input_current": round(input_record.current, 2),
          "output_current": round(output_record.current, 2),
          "soc": round(RecordHandler.current_soc, 2)
        },
        resolution = 1
      )
    except:
      logging.error("failed to create record!")
      logging.error("input_record.voltage: " + str(input_record.voltage))
      logging.error("output_record.voltage: " + str(output_record.voltage))
      logging.error("input_record.current: " + str(input_record.current))
      logging.error("output_record.current: " + str(output_record.current))
      logging.error("RecordHandler.current_soc: " + str(RecordHandler.current_soc))


    RecordHandler.add_record(record)

    # save new capacity and soc to config file if necessary

    try:
      if round(RecordHandler.current_capacity, 2) != RecordHandler.old_capacity:
        with Config() as parser:
          parser.set("battery_state", "capacity", str(round(RecordHandler.current_capacity, 2)))

      if round(RecordHandler.current_soc, 2) != RecordHandler.old_soc:
        with Config() as parser:
          parser.set("battery_state", "soc", str(round(RecordHandler.current_soc, 2)))

      RecordHandler.old_capacity = round(RecordHandler.current_capacity, 2)
      RecordHandler.old_soc = round(RecordHandler.current_soc, 2)
    except:
      logging.error("failed to save new capacity and soc to config file!")
      logging.error("RecordHandler.current_capacity: " + str(RecordHandler.current_capacity))
      logging.error("RecordHandler.current_soc: " + str(RecordHandler.current_soc))
      logging.error("RecordHandler.old_capacity: " + str(RecordHandler.old_capacity))
      logging.error("RecordHandler.old_soc: " + str(RecordHandler.old_soc))

    # calculate current battery charging level
    try:
      low_battery_level = True
      if RecordHandler.current_capacity != 0:
        RecordHandler.charging_level = math.trunc(RecordHandler.current_soc / RecordHandler.current_capacity * 100)
        low_battery_level = RecordHandler.charging_level <= LOW_BATTERY_THRESHOLD

      battery_charging = input_record.current > output_record.current
    except:
      logging.error("failed to calculate battery charging level!")
      logging.error("input_record.current: " + str(input_record.current))
      logging.error("output_record.current: " + str(output_record.current))
      logging.error("RecordHandler.current_soc: " + str(RecordHandler.current_soc))
      logging.error("RecordHandler.current_capacity: " + str(RecordHandler.current_capacity))

    # update LED indicators
    try:
      LEDControl.set(LED.RED, low_battery_level)
      LEDControl.set(LED.GREEN, battery_charging)
      LEDControl.set(LED.YELLOW, False)
    except:
      logging.error("failed to update LED indicators!")
      logging.error("low_battery_level: " + str(low_battery_level))
      logging.error("battery_charging: " + str(battery_charging))


  def run_capacity_correction():

    '''
    * Runs capacity correction if necessary.
    '''

    logging.debug("running capacity correction...")

    with Config() as parser:
      calibration_state = parser.getboolean("system", "calibrating_capacity")

    if calibration_state:
      if CapacityCorrection.run(CORRECTION_INTERVAL):
        old_correction_value = RecordHandler.capacity_correction

        with Config() as parser:
          RecordHandler.capacity_correction = parser.getfloat("battery_state", "capacity_correction")
          parser["system"]["calibrating_capacity"] = "False"

        logging.info("capacity correction value was changed from {}A to {}A".format(old_correction_value, RecordHandler.capacity_correction))