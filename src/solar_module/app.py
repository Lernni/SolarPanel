import logging

import data_access.database_handler as db
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
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d.%m.%Y %I:%M:%S %p"
  )

logging.info("init application")

logging.info("check module...")
Module.init()

logging.info("analyze database...")
db.init()
db.repartition()

logging.info("load record handler...")
RecordHandler.init()

if __name__ == '__main__':
  pass
  flask_app.run(debug = True, use_reloader = False, host = '0.0.0.0', port = 5001)