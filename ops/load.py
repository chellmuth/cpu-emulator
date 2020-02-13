import instruction_base
from core import MachineUpdate

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
        address = self.source_word.int_value()
        loaded_word = machine.memory.read_word(address)

        return MachineUpdate(
            registers={
                self.dest_register: loaded_word
            }
        )
