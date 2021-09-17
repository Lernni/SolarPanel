from enum import Enum

class Submodule:

    class State(Enum):
        IDLE = 1
        BUSY = 2
        ERROR = 3
        UNKNOWN = 4

    def __init__(self, name, description):
        self.state = Submodule.State.UNKNOWN
        self.name = name
        self.description = description

    def __str__(self):
        return "Name: '" + self.name + "' Description: '" + self.description + "' State: '" + str(self.state.name) + "'"