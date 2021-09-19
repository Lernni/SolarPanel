import os
import json

from flask_restx import Resource
from flask import request

from config import config

class SystemShutdown(Resource):
  def post(self):
    os.system('echo "sudo shutdown -h now" > /data/host_cmd_interface')
    return

class SystemRestart(Resource):
  def post(self):
    os.system('echo "sudo reboot" > /data/host_cmd_interface')
    return

class Settings(Resource):
  def get(self):
    settings = None

    with config.Config() as parser:
      settings = {
        "recording": parser.getboolean("system", "recording"),
        "input_shunt": float(parser["record_config"]["input_shunt"]),
        "output_shunt": float(parser["record_config"]["output_shunt"]),
        "max_input_current": int(parser["record_config"]["max_input_current"]),
        "max_output_current": int(parser["record_config"]["max_output_current"]),
      }

    return settings

  def post(self):
    new_config = json.loads(request.data)

    with config.Config() as parser:
      parser["system"]["recording"] = str(new_config["recording"])
      parser["record_config"] = {
        "input_shunt": str(new_config["input_shunt"]),
        "output_shunt": str(new_config["output_shunt"]),
        "max_input_current": str(new_config["max_input_current"]),
        "max_output_current": str(new_config["max_output_current"]),
      }

    config.reload()
    return