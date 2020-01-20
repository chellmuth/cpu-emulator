import instruction_base
from emulator import MachineUpdate

class LoadRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("LOD", dest_register, source_register)

    def run(self, machine):
        payload = machine.registers[self.source_register]
        return MachineUpdate(
            registers={
                self.dest_register: payload
            }
        )

class LoadConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("LOD", dest_register, source_word)

    def run(self, machine):
        return MachineUpdate(
            registers={
                self.dest_register: self.source_word
            }
        )
