from submodules.ina219_module import INA219Module

class Module:

    input_ina = None

    def init():
        Module.input_ina = INA219Module(0.1, "Test Module")