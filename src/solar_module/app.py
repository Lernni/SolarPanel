import logging

from data_access.database_handler import DatabaseHandler
from data_access.record_handler import RecordHandler
from rest_service.rest import flask_app
from module import Module

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
RecordHandler.start_recording()

if __name__ == '__main__':
    flask_app.run(debug = True)