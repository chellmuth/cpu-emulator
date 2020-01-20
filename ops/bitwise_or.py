import instruction_base
from emulator import MachineUpdate

class BitwiseOrRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("ORR", dest_register, source_register)

    def run(self, machine):
        result, _ = bitwise_or(
            machine.registers[self.dest_register],
            machine.registers[self.source_register]
        )

        return MachineUpdate(
            registers={
                self.dest_register: result
            }
        )

class BitwiseOrConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("ORR", dest_register, source_word)

    def run(self, machine):
        result, _ = bitwise_or(
            machine.registers[self.dest_register],
            self.source_word
        )

        return MachineUpdate(
            registers={
                self.dest_register: result
            }
        )

def bitwise_or(word1, word2):
    return word1 | word2, set()
