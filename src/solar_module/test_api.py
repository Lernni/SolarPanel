from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS

from submodules.ina219_module import INA219Module

app = Flask(__name__)
CORS(app)
api = Api(app)

ina = INA219Module(0.1, "Test Module")


class LatestRecord(Resource):
    def get(self):
        measurement = ina.measure()
        return {
            "voltage": measurement.voltage,
            "input_current": measurement.current,
            "output_current": 0,
            "power": measurement.power,
        }

api.add_resource(LatestRecord, '/latest')

if __name__ == '__main__':
    app.run(debug=True)
