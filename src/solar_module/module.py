from submodules.ina219_module import INA219Module

class Module:

    input_ina = None
    output_ina = None

    def init():
        Module.input_ina = INA219Module(0.0001, 0x40, "Input Current Module")
        Module.output_ina = INA219Module(0.0001, 0x41, "Output Current Module")