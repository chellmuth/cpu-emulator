import instruction_base
from emulator import MachineUpdate

class NopInstruction(instruction_base.Instruction):
    size = 1

    def human(self):
        return "NOP"

    def run(self, machine):
        return MachineUpdate()
