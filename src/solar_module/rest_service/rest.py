import logging

from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from rest_service.records import DashboardUpdate, LatestNRecords
from rest_service.system import SystemShutdown, SystemRestart, Settings, SystemCalibrationState
from rest_service.db_records import DBRecords

flask_app = Flask(__name__)
CORS(flask_app)
api = Api(flask_app)

flask_app.logger.addHandler(logging.StreamHandler())
flask_app.logger.setLevel(logging.INFO)

api.add_resource(DashboardUpdate, '/dashboard')
api.add_resource(LatestNRecords, '/latest/<int:n>')

api.add_resource(DBRecords, '/db/records')

api.add_resource(SystemShutdown, '/system/shutdown')
api.add_resource(SystemRestart, '/system/restart')
api.add_resource(Settings, '/system/settings')
api.add_resource(SystemCalibrationState, '/system/calibration_state/<int:state>')