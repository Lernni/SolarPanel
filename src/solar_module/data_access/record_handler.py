import time
from threading import Thread
import logging
import math

import schedule

from data_access.database_handler import DatabaseHandler
from data_objects.record import Record
from config.config import Config
from hardware_access.module import Module
from hardware_access.led_control import LEDControl, LED
from globals import RESOLUTION_DEPTH, MAX_CACHE_SIZE, MAX_RESOLUTION, LOW_BATTERY_THRESHOLD


class RecordScheduler(Thread):

  '''
  * Schedules creation of new records exactly once per second
  * Schedules calculation of averages once per day at midnight
  '''

  def __init__(self, job):
    Thread.__init__(self)
    self.name = "RecordScheduler"
    self.running = True
    self.job = job

    self.calc_averages_job = schedule.every().day.at("00:00").do(RecordScheduler.run_threaded, RecordHandler.calc_averages)
  

  def run_threaded(job_func):
    job_thread = Thread(target = job_func, name= "JobThread")
    job_thread.start()

  def run(self):
    while self.running:
      # sleep as long as needed to run at an exact one second interval
      self.job()
      schedule.run_pending()
      time.sleep(1.0 - time.time() % 1.0)

  def stop(self):
    self.running = False
    schedule.cancel_job(self.calc_averages_job)


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

      if RecordHandler.current_capacity is None:
        with Config() as parser:
          RecordHandler.current_capacity = parser.getfloat("battery_state", "capacity")

      if RecordHandler.current_soc is None:
        with Config() as parser:
          RecordHandler.current_soc = parser.getfloat("battery_state", "soc")

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


  def get_latest_record() -> Record:

    '''
    * Returns the latest record with resolution 1 from cache.
    '''

    return RecordHandler.record_cache[0][-1]

  def get_latest_records(n: int):
      
    '''
    * Returns the latest n records with resolution 1 from cache.
    '''

    if 1 <= n <= len(RecordHandler.record_cache[0]):
      return RecordHandler.record_cache[0][-n:]
    elif n > len(RecordHandler.record_cache[0]):
      return RecordHandler.record_cache[0]


  def add_record(record: Record):

    '''
    * Adds given record to cache and its lower resolution versions, if possible.
    * If the cache is full, first half of the cache will be saved.
    '''

    # add record to the appropriate sub-list in the cache
    # the sub-list is determined by the resolution of the record
    # all possible resolutions are multiples of 2, so log base 2
    #   of the record resolution sorts the records in sub-lists accordingly
    
    cache_index = int(math.log2(record.resolution))
    RecordHandler.record_cache[cache_index].append(record)

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

    if (RecordHandler.record_count % (record.resolution * 2) == 0) & ((record.resolution * 2) <= MAX_RESOLUTION):
      # There are two records with the current resolution, so they can be averaged

      other_record = None
      averaged_record = None

      if len(RecordHandler.record_cache[cache_index]) >= 2:
        # Both records are in cache
        other_record = RecordHandler.record_cache[cache_index][-2]

      else:
        # The other record is not in cache, so it must be read from the db

        other_record = DatabaseHandler.get_latest_record(record.resolution)
      

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
      
      # Add the averaged record of lower resolution to the cache recursively
      # The recursive call allows even lower resolution records to be added to the cache, if possible

      RecordHandler.add_record(averaged_record)


    if RecordHandler.record_count == MAX_RESOLUTION:
      # Record count reached value to calculate the lowest resolution record
      logging.debug("record count reached maximum, resetting...")

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
      for i in range(len(RecordHandler.record_cache)):
        if len(RecordHandler.record_cache[i]) == 1:
          DatabaseHandler.add_records([RecordHandler.record_cache[i][0]])
          RecordHandler.record_cache[i] = []

        elif len(RecordHandler.record_cache[i]) > 1:
          DatabaseHandler.add_records(RecordHandler.record_cache[i][:len(RecordHandler.record_cache[i]) // 2])
          RecordHandler.record_cache[i] = RecordHandler.record_cache[i][len(RecordHandler.record_cache[i]) // 2:]
        else:
          break
    else:
      for sub_list in RecordHandler.record_cache:
        if len(sub_list) != 0:
          DatabaseHandler.add_records(sub_list)
        else:
          break

      RecordHandler.record_cache = [[] for _ in range(RESOLUTION_DEPTH + 1)]


  def create_record():

    '''
    * Creates a new record by measuring the current and voltage of the solar module.
    * The yellow LED will be turned on for the duration of the measurement and processing.
    * TODO: The record also contains the current state of charge.
    '''

    logging.debug("creating record...")

    LEDControl.set(LED.YELLOW, True)

    # measure voltage and current
    input_record = Module.input_ina.measure()
    output_record = Module.output_ina.measure()

    # calculate state of charge (soc) and capacity
    current_difference = (input_record.current - output_record.current) / 3600
    RecordHandler.current_soc += current_difference

    if RecordHandler.current_soc > RecordHandler.current_capacity:
      RecordHandler.current_capacity = RecordHandler.current_soc

    if RecordHandler.current_soc < 0:
      RecordHandler.current_capacity += abs(RecordHandler.current_soc)
      RecordHandler.current_soc = 0.0

    # create record with new data and add it to cache
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

    RecordHandler.add_record(record)

    # update battery state and highscores
    with Config() as parser:

      # battery state
      if round(RecordHandler.current_capacity, 2) != RecordHandler.old_capacity:
        parser.set("battery_state", "capacity", str(round(RecordHandler.current_capacity, 2)))

      if round(RecordHandler.current_soc, 2) != RecordHandler.old_soc:
        parser.set("battery_state", "soc", str(round(RecordHandler.current_soc, 2)))


      # battery highscores
      if current_difference > 0:
        max_soc_gain_s = parser.getfloat("highscores", "max_soc_gain_s")
        if current_difference > max_soc_gain_s:
          parser.set("highscores", "max_soc_gain_s", str(current_difference))
          parser.set("highscores", "max_soc_gain_s_date", str(record.timestamp))
      else:
        max_soc_loss_s = parser.getfloat("highscores", "max_soc_loss_s")
        if abs(current_difference) > max_soc_loss_s:
          parser.set("highscores", "max_soc_loss_s", str(abs(current_difference)))
          parser.set("highscores", "max_soc_loss_s_date", str(record.timestamp))


      # voltage highscores
      max_voltage = parser.getfloat("highscores", "max_voltage")
      if record.data["voltage"] > max_voltage:
        parser.set("highscores", "max_voltage", str(record.data["voltage"]))
        parser.set("highscores", "max_voltage_date", str(record.timestamp))

      min_voltage = parser.getfloat("highscores", "min_voltage")
      if record.data["voltage"] < min_voltage or min_voltage == 0:
        parser.set("highscores", "min_voltage", str(record.data["voltage"]))
        parser.set("highscores", "min_voltage_date", str(record.timestamp))


      # input_current highscores
      max_input_current = parser.getfloat("highscores", "max_input_current")
      if record.data["input_current"] > max_input_current:
        parser.set("highscores", "max_input_current", str(record.data["input_current"]))
        parser.set("highscores", "max_input_current_date", str(record.timestamp))


      # output_current highscores
      max_output_current = parser.getfloat("highscores", "max_output_current")
      if record.data["output_current"] > max_output_current:
        parser.set("highscores", "max_output_current", str(record.data["output_current"]))
        parser.set("highscores", "max_output_current_date", str(record.timestamp))
      

    RecordHandler.old_capacity = round(RecordHandler.current_capacity, 2)
    RecordHandler.old_soc = round(RecordHandler.current_soc, 2)

    # calculate current battery charging level
    low_battery_level = True
    if RecordHandler.current_capacity != 0:
      RecordHandler.charging_level = math.trunc(RecordHandler.current_soc / RecordHandler.current_capacity * 100)
      low_battery_level = RecordHandler.charging_level <= LOW_BATTERY_THRESHOLD

    battery_charging = input_record.current > output_record.current

    # update LED indicators
    LEDControl.set(LED.RED, low_battery_level)
    LEDControl.set(LED.GREEN, battery_charging)
    LEDControl.set(LED.YELLOW, False)


  def calc_averages():

    '''
    * Calculates averages for every metric for the past day and last week
    '''

    logging.debug("calculating averages...")

    voltage_yesterday = DatabaseHandler.get_average()