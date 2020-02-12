import instruction_base
from core import Flag, MachineUpdate
from ops.subtract import subtract_word

class CompareRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("CMP", dest_register, source_register)

    def run(self, machine):
        result, flags = subtract_word(
            machine.registers[self.dest_register],
            machine.registers[self.source_register]
        )

        return MachineUpdate(flags=flags)

class CompareConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("CMP", dest_register, source_word)

    def run(self, machine):
        result, flags = subtract_word(
            machine.registers[self.dest_register],
            self.source_word
        )

        return MachineUpdate(flags=flags)
