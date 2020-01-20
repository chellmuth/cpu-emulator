import instruction_base
from core import Register, Word
from emulator import MachineUpdate

class PrintRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("OUT", value_register)

    def run(self, machine):
        char = machine.registers[self.value_register].low_byte()

        return MachineUpdate(stdout=char)

class PrintConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("OUT", value_word)

    def run(self, machine):
        char = self.value_word.low_byte()

        return MachineUpdate(stdout=char)
