import smbus2

from submodules.submodule import Submodule

class MCP23017Module(Submodule):

    def __init__(self, description):
        super().__init__(name = "MCP23017", description = description)

        self.mcp = smbus2.SMBus(1)
        self.mcp.write_byte_data(0x20, 0x01, 0x00)

    def set(self, address, on):
        try:
            led_state = self.mcp.read_byte_data(0x20, 0x15)
            if ((led_state & address == address) and not on) or ((led_state & address != address) and on):
                self.mcp.write_byte_data(0x20, 0x15, led_state ^ address)
        except: pass

    def reset(self):
        self.mcp.write_byte_data(0x20, 0x01, 0x00)