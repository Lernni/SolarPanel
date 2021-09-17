import os
import logging
import json

from flask_restx import Resource
from flask import request

from config import config

class SystemShutdown(Resource):
  def post(self):
    os.systen('echo "sudo shutdown -h now" > /data/host_cmd_interface')
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
      }

    return settings

  def post(self):
    new_config = json.loads(request.data)

    with config.Config() as parser:
      parser["system"]["recording"] = str(new_config["recording"])
      parser["record_config"] = {
        "input_shunt": str(new_config["input_shunt"]),
        "output_shunt": str(new_config["output_shunt"]),
      }

    config.reload()
    return