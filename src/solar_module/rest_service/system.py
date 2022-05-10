import os
import json

from flask_restx import Resource
from flask import request

from config.config import reload, Config

class SystemShutdown(Resource):
  def post(self):
    os.system('echo "sudo shutdown -h now" > /data/host_cmd_interface')
    return

class SystemRestart(Resource):
  def post(self):
    os.system('echo "sudo reboot" > /data/host_cmd_interface')
    return

class SystemCalibrationState(Resource):
  def post(self, state):
    with Config() as parser:
      parser.set("system", "calibrating_capacity", str(bool(state)))

    return

class Settings(Resource):
  def get(self):
    settings = None

    with Config() as parser:
      settings = {
        "recording": parser.getboolean("system", "recording"),
        "calibrating": parser.getboolean("system", "calibrating_capacity"),
        "input_shunt": float(parser["record_config"]["input_shunt"]),
        "output_shunt": float(parser["record_config"]["output_shunt"]),
        "max_input_current": int(parser["record_config"]["max_input_current"]),
        "max_output_current": int(parser["record_config"]["max_output_current"]),
        "capacity_correction": float(parser.getfloat("battery_state", "capacity_correction")),
      }

    return settings

  def post(self):
    new_config = json.loads(request.data)

    with Config() as parser:
      parser["system"] = {
        "recording": str(new_config["recording"]),
        "calibrating_capacity": str(new_config["calibrating"]),
      }

      parser["record_config"] = {
        "input_shunt": str(new_config["input_shunt"]),
        "output_shunt": str(new_config["output_shunt"]),
        "max_input_current": str(new_config["max_input_current"]),
        "max_output_current": str(new_config["max_output_current"]),
      }

      parser["battery_state"]["capacity_correction"] = str(new_config["capacity_correction"])

      reload()
    return