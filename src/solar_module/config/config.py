import configparser
import os
import traceback
from shutil import copyfile

from globals import CONFIG_TEMPLATE_PATH, CONFIG_DIR_PATH


def reload():
	from data_access.record_handler import RecordHandler
	from hardware_access.module import Module
	
	RecordHandler.stop_recording()
	Module.init()
	RecordHandler.init()

class Config:
	def __init__(self):
		self.parser = configparser.ConfigParser()
		self.config_dest = os.path.join(CONFIG_DIR_PATH, "config.ini")
		CONFIG_DIR_PATH.mkdir(parents = True, exist_ok = True)

		if not os.path.isfile(self.config_dest):
			copyfile(CONFIG_TEMPLATE_PATH, self.config_dest)

	def __enter__(self):
		self.parser.read(self.config_dest)
		return self.parser

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type is not None:
			traceback.print_exception(exc_type, exc_val, exc_tb)
			return False

		with open(self.config_dest, "w") as f: self.parser.write(f)
		return True