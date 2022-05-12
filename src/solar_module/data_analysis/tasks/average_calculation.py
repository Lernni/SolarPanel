import logging
from datetime import datetime, timedelta

from data_analysis.data_analysis import DataAnalysis
from config.config import Config

class AverageCalculationTask:

  '''
  * Calculates averages for every metric for the past day and week
  '''

  def __init__(self):
    logging.debug("init AverageCalculationTask...")

    self.run()


  def run(self):

    current_time = datetime.now()

    # averages past day
    past_day_time = current_time - timedelta(days = 1)
    average_record_past_day = DataAnalysis.get_average(past_day_time, current_time)
    if average_record_past_day is None: return

    with Config() as parser:
      parser["averages_yesterday"] = {
        key: str(average_record_past_day.data[key]) for key in average_record_past_day.data
      }


    # averages past week
    past_week_time = current_time - timedelta(weeks = 1)
    average_record_past_week = DataAnalysis.get_average(past_week_time, current_time)
    if average_record_past_week is None: return

    with Config() as parser:
      parser["averages_past_week"] = {
        key: str(average_record_past_week.data[key]) for key in average_record_past_week.data
      }
