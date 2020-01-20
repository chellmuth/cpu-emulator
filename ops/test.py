import instruction_base
from core import Flag, MachineUpdate
from ops.bitwise_and import bitwise_and

class TestRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("TST", dest_register, source_register)

    def run(self, machine):
        _, flags = bitwise_and(
            machine.registers[self.dest_register],
            machine.registers[self.source_register]
        )

        return MachineUpdate(
            registers={
                self.dest_register: result
            },
            flags=flags
        )

class TestConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("TST", dest_register, source_word)

    def run(self, machine):
        _, flags = bitwise_and(
            machine.registers[self.dest_register],
            self.source_word
        )

        return MachineUpdate(
            flags=flags
        )
