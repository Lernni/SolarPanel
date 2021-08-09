import logging

from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from rest_service.records import LatestRecord, LatestNRecords


flask_app = Flask(__name__)
CORS(flask_app)
api = Api(flask_app)

flask_app.logger.addHandler(logging.StreamHandler())
flask_app.logger.setLevel(logging.INFO)

api.add_resource(LatestRecord, '/latest')
api.add_resource(LatestNRecords, '/latest/<int:n>')