import instruction_base
from core import MachineUpdate

class StoreByteRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("STB", dest_register, source_register)

    def run(self, machine):
        result = machine.registers[self.dest_register].low_byte()
        return MachineUpdate(
            memory={
                machine.registers[self.source_register]: result
            }
        )

class StoreByteConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("STB", dest_register, source_word)

    def run(self, machine):
        result = machine.registers[self.dest_register].low_byte()
        return MachineUpdate(
            memory={
                self.source_word: result
            }
        )

class StoreWordRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("STR", dest_register, source_register)

    def run(self, machine):
        result = machine.registers[self.dest_register]
        return MachineUpdate(
            memory={
                machine.registers[self.source_register]: result
            }
        )

class StoreWordConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("STR", dest_register, source_word)

    def run(self, machine):
        result = machine.registers[self.dest_register]
        return MachineUpdate(
            memory={
                self.source_word: result
            }
        )
