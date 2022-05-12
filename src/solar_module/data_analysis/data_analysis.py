from datetime import timedelta
import math

from data_objects.record import Record
from data_access.database_handler import DatabaseHandler
from data_analysis.analysis_helper import AnalysisHelper
from globals import MAX_RESOLUTION


class DataAnalysis:

  def get_average(start_time, end_time, metric = None) -> None or float or Record:

    '''
    * Returns the average value for a given metric over a specific time
    * Or, if metric isn't specified, return exact average record for a specific time
    '''

    # calculate the time difference in seconds
    time_delta_seconds = int(timedelta.total_seconds(end_time - start_time))
    if time_delta_seconds == 0: return None

    # get gcd() to identify lowest resolution that could contain time period exactly and if not,
    #  the resulting error will small in comparison to the computing effort
    resolution = math.gcd(time_delta_seconds, MAX_RESOLUTION)

    # get values
    records = DatabaseHandler.get_records(start_time, end_time, resolution)
    if len(records) == 0: return None

    if metric is None:
      # calc average of all metrics
      record_metrics = AnalysisHelper.separate_metrics(records)
      averaged_record = Record(
        timestamp = records[0].timestamp,
        data = {
          key: round(sum(record_metrics[key]) / len(records), 2) for key in record_metrics
        },
        resolution = time_delta_seconds
      )

      return averaged_record

    else:
      # calc average of one metric
      metric_list = AnalysisHelper.separate_metrics(records, filter = [metric])
      return round(sum(metric_list) / len(metric_list), 2)
    