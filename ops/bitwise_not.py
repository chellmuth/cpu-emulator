import instruction_base
from emulator import MachineUpdate

class BitwiseNotRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("NOT", value_register)

    def run(self, machine):
        result = bitwise_not(machine.registers[self.value_register])

        return MachineUpdate(
            registers={
                self.value_register: result
            }
        )

def bitwise_not(word):
    return ~word
