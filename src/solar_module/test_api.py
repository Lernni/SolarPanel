from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS
from ina219 import INA219, DeviceRangeError

app = Flask(__name__)
CORS(app)
api = Api(app)

SHUNT_OHM = 0.1
MAX_EXPECTED_AMPS = 0.4
ina = INA219(SHUNT_OHM, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V, ina.GAIN_1_40MV)

class Voltage(Resource):
    def get(self):
        try:
            voltage = round(ina.voltage() + ina.shunt_voltage() / 1000, 2);
        except DeviceRangeError as e:
            voltage = 0

        return {
            'voltage': voltage
        }

class InputCurrent(Resource):
    def get(self):
        try:
            current = round(ina.current(), 2);
        except DeviceRangeError as e:
            current = 0

        return {
            'input_current': current
        }

class OutputCurrent(Resource):
    def get(self):
        return {
            'output_current': 0
        }

class Power(Resource):
    def get(self):
        try:
            power = round(ina.power(), 2);
        except DeviceRangeError as e:
            power = 0

        return {
            'power': power
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
