from flask import Flask
from flask_restx import Resource, Api

import random

app = Flask(__name__)
api = Api(app)

class Voltage(Resource):
    def get(self):
        return {
            'voltage': round(random.uniform(12.0, 14.5), 2)
        }

class InputCurrent(Resource):
    def get(self):
        return {
            'input_current': round(random.uniform(0.0, 20.0), 2)
        }

class OutputCurrent(Resource):
    def get(self):
        return {
            'output_current': round(random.uniform(0.0, 150.0), 2)
        }

class Power(Resource):
    def get(self):
        return {
            'power': round(random.uniform(0.0, 2000.0), 2)
        }

class LatestRecord(Resource):
    def get(self):
        record = Voltage().get()
        record.update(InputCurrent().get())
        record.update(OutputCurrent().get())
        record.update(Power().get())
        return record


api.add_resource(Voltage, '/latest/voltage')
api.add_resource(InputCurrent, '/latest/input_current')
api.add_resource(OutputCurrent, '/latest/output_current')
api.add_resource(Power, '/latest/power')
api.add_resource(LatestRecord, '/latest')

if __name__ == '__main__':
    app.run(debug=True)
