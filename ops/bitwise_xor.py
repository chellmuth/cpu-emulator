import instruction_base
from core import Flag, MachineUpdate

class BitwiseXorRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("XOR", dest_register, source_register)

    def run(self, machine):
        result, flags = bitwise_xor(
            machine.registers[self.dest_register],
            machine.registers[self.source_register]
        )

        return MachineUpdate(
            registers={
                self.dest_register: result
            },
            flags=flags
        )

class BitwiseXorConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("XOR", dest_register, source_word)

    def run(self, machine):
        result, flags = bitwise_xor(
            machine.registers[self.dest_register],
            self.source_word
        )

        return MachineUpdate(
            registers={
                self.dest_register: result
            },
            flags=flags
        )

def bitwise_xor(word1, word2):
    result = word1 ^ word2

    flags = set()
    if result.int_value() == 0:
        flags.add(Flag.ZF)

    sign_bit = 1 << 23
    if result.int_value() & sign_bit:
        flags.add(Flag.SF)

    return result, flags
