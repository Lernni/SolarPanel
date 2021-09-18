from hardware_access.submodules.ina219_module import INA219Module
from hardware_access.submodules.mcp23017_module import MCP23017Module
from config.config import Config

class Module:

	input_ina = None
	output_ina = None
	mcp = None

	def init():
		input_shunt = None
		output_shunt = None

		with Config() as parser:
			record_config = dict(parser.items("record_config"))
			input_shunt = float(record_config["input_shunt"])
			output_shunt = float(record_config["output_shunt"])
			max_input_current = int(record_config["max_input_current"])
			max_output_current = int(record_config["max_output_current"])

		Module.input_ina = INA219Module(input_shunt, max_input_current, 0x40, "Input Current Module")
		Module.output_ina = INA219Module(output_shunt, max_output_current, 0x41, "Output Current Module")
		Module.mcp = MCP23017Module("LED Control Module")