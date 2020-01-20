import instruction_base
from core import Byte, MachineUpdate, Flag, Word

class SubtractRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("SUB", dest_register, source_register)

    def run(self, machine):
        result, flags = subtract_word(
            machine.registers[self.dest_register],
            machine.registers[self.source_register]
        )

        return MachineUpdate(
            registers={
                self.dest_register: result,
            },
            flags=flags
        )

class SubtractConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("SUB", dest_register, source_word)

    def run(self, machine):
        result, flags = subtract_word(
            machine.registers[self.dest_register],
            self.source_word
        )

        return MachineUpdate(
            registers={
                self.dest_register: result,
            },
            flags=flags
        )

def subtract_word(word1, word2):
    flags = set()

    int_result = word1.int_value() - word2.int_value()

    if int_result == 0:
        flags.add(Flag.ZF)

    sign_bit = 1 << 27

    if int_result & sign_bit:
        flags.add(Flag.SF)

    return Word.from_int(int_result), flags
