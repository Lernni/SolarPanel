from ina219 import INA219, DeviceRangeError

from data_objects.record import RawRecord
from submodules.submodule import Submodule

class INA219Module(Submodule):

    def __init__(self, shunt_ohms, address, description):
        super().__init__(name = "INA219", description = description)
        
        self.ina = INA219(shunt_ohms, 0.4, address = address)
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)

        self.state = Submodule.State.IDLE
    
    def measure(self):
        self.state = Submodule.State.BUSY

        try:
            voltage = self.ina.voltage()

            # current is measured in mA
            current = self.ina.current() / 1000
            if current < 0: current = 0

            return RawRecord(voltage, current)
        except DeviceRangeError as e:
            print(e)

        self.state = Submodule.State.IDLE
