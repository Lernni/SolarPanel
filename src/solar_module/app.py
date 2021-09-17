import logging

from data_access.database_handler import DatabaseHandler
from data_access.record_handler import RecordHandler
from rest_service.rest import flask_app
from hardware_access.module import Module

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%d.%m.%Y %I:%M:%S %p"
    )

logging.info("init application")

logging.info("check module...")
Module.init()

logging.info("analyze database...")
DatabaseHandler.init()

logging.info("start recording...")
RecordHandler.init()

if __name__ == '__main__':
    flask_app.run(debug = True, use_reloader = False, host = '0.0.0.0', port = 5001)