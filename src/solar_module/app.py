import logging

from data_access.database_handler import DatabaseHandler
from data_access.record_handler import RecordHandler
from rest_service.rest import flask_app
from hardware_access.module import Module
from globals import LOGS_PATH, DEBUG

if not DEBUG:
  LOGS_PATH.mkdir(parents = True, exist_ok=True)

  logging.basicConfig(
    filename=str(LOGS_PATH) + '/solar_module.log',
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d.%m.%Y %I:%M:%S %p"
  )
else:
  logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    datefmt="%d.%m.%Y %I:%M:%S %p"
  )

logging.info("checking modules...")
Module.init()

logging.info("loading database...")
DatabaseHandler.init()

logging.info("loading record handler...")
RecordHandler.init()

logging.info("starting flask app...")

if __name__ == '__main__':
  flask_app.run(debug = True, use_reloader = False, host = '0.0.0.0', port = 5001)