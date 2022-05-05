import logging

from flask_restx import Resource

from data_access.record_handler import RecordHandler
from config.config import Config


class DashboardUpdate(Resource):
  def get(self):

    '''
    * This request is used to update the dashboard periodically
    * Returns the latest recording
    '''

    record = RecordHandler.get_latest_record()

    return {
      "timestamp": record.timestamp,
      "voltage": round(record.data["voltage"], 2),
      "input_current": round(record.data["input_current"], 2),
      "output_current": round(record.data["output_current"], 2),
      "soc": RecordHandler.current_soc,
      "capacity": RecordHandler.current_capacity,
    }


class MetricAnalysis(Resource):
  def get(self, metric, n):

    '''
    * This request is used to fetch data for a given metric that do not need to be updated periodically
    * Returns metric averages for the last day and week
    * Returns the last n recorded values as live data for the given metric
    '''

    response = {
      "data": [],
      "details": {}
    }

    latest_records = RecordHandler.get_latest_records(n)
    for record in latest_records:
      response["data"].append(record.data[metric])

    with Config() as parser:
      if metric == "voltage":
        response["details"] = {
          "max": parser.getfloat("highscores", "max_voltage"),
          "max_date": parser.get("highscores", "max_voltage_date"),
          "min": parser.getfloat("highscores", "min_voltage"),
          "min_date": parser.get("highscores", "min_voltage_date"),
          "avg_yesterday": parser.get("averages", "voltage_yesterday"),
          "avg_week": parser.get("averages", "voltage_last_week"),
        }
      elif metric == "input_current":
        response["details"] = {
          "max": parser.getfloat("highscores", "max_input_current"),
          "max_date": parser.get("highscores", "max_input_current_date"),
          "avg_yesterday": parser.get("averages", "input_current_yesterday"),
          "avg_week": parser.get("averages", "input_current_last_week"),
        }
      elif metric == "output_current":
        response["details"] = {
          "max": parser.getfloat("highscores", "max_output_current"),
          "max_date": parser.get("highscores", "max_output_current_date"),
          "avg_yesterday": parser.get("averages", "output_current_yesterday"),
          "avg_week": parser.get("averages", "output_current_last_week"),
        }
      elif metric == "soc":
        response["details"]= {
          "max_soc_gain": parser.getfloat("highscores, max_soc_gain_s"),
          "max_soc_loss": parser.getfloat("highscores, max_soc_loss_s"),
        }
      else:
        logging.warning("Invalid metric requested: {}".format(metric))

    return response


class LatestNRecords(Resource):
  def get(self, n):
    records = RecordHandler.get_latest_records(n)

    requested_records = {
      "voltage": [],
      "input_current": [],
      "output_current": [],
      "soc": []
    }

    for record in records:
      requested_records["voltage"].append(round(record.data["voltage"], 2))
      requested_records["input_current"].append(round(record.data["input_current"], 2))
      requested_records["output_current"].append(round(record.data["output_current"], 2))
      requested_records["soc"].append(round(record.data["soc"], 2))

    return requested_records