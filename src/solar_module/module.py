from submodules.ina219_module import INA219Module
from submodules.mcp23017_module import MCP23017Module

class Module:

    input_ina = None
    output_ina = None
    mcp = None

    def init():
        Module.input_ina = INA219Module(0.0001, 0x40, "Input Current Module")
        Module.output_ina = INA219Module(0.0001, 0x41, "Output Current Module")
        Module.mcp = MCP23017Module("LED Control Module")