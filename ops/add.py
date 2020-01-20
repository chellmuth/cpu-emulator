import instruction_base
from core import Byte, MachineUpdate, Flag, Word

class AddRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("ADD", dest_register, source_register)

    def run(self, machine):
        result, flags = add_word(
            machine.registers[self.dest_register],
            machine.registers[self.source_register]
        )

        return MachineUpdate(
            registers={
                self.dest_register: result,
            },
            flags=flags
        )

class AddConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("ADD", dest_register, source_word)

    def run(self, machine):
        result, flags = add_word(
            machine.registers[self.dest_register],
            self.source_word
        )

        return MachineUpdate(
            registers={
                self.dest_register: result,
            },
            flags=flags
        )

def add_word(word1, word2):
    flags = set()

    int_sum = word1.int_value() + word2.int_value()

    if int_sum == 0:
        flags.add(Flag.ZF)

    sign_bit = 1 << 27
    overflow_bit = 1 << 28

    if int_sum & sign_bit:
        flags.add(Flag.SF)

    if int_sum & overflow_bit:
        flags.add(Flag.CF)

        if not ((word1.int_value() & sign_bit) ^ (word2.int_value() & sign_bit)):
            flags.add(Flag.OF)

    return Word.from_int(int_sum), flags
