from enum import Enum

from hardware_access.module import Module

class LED(Enum):
    GREEN = 0x04
    YELLOW = 0x02
    RED = 0x01

class LEDControl:

    def set(led, state):
        Module.mcp.set(led.value, state)