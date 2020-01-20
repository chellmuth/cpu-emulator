import instruction_base
from core import Byte, Flag, Word
from emulator import MachineUpdate

class AddRegisterInstruction(instruction_base.Type1RegisterInstruction):
    def __init__(self, dest_register, source_register):
        super().__init__("ADD", dest_register, source_register)

    def run(self, machine):
        result, flags = add(
            machine.registers[self.dest_register].low_byte(),
            machine.registers[self.source_register].low_byte()
        )

        return MachineUpdate(
            registers={
                self.dest_register: Word(result, Byte(0b0), Byte(0b0), Byte(0b0))
            },
            flags=flags
        )

class AddConstantInstruction(instruction_base.Type1ConstantInstruction):
    def __init__(self, dest_register, source_word):
        super().__init__("ADD", dest_register, source_word)

    def run(self, machine):
        result, flags = add(
            machine.registers[self.dest_register].low_byte(),
            self.source_word.low_byte()
        )

        return MachineUpdate(
            registers={
                self.dest_register: Word(result, Byte(0b0), Byte(0b0), Byte(0b0))
            },
            flags=flags
        )

def add(byte1, byte2):
    flags = set()

    summed = byte1.int_value + byte2.int_value
    if summed == 0:
        flags.add(Flag.ZF)

    sign_bit = 1 << 6
    overflow_bit = 1 << 7

    if summed & sign_bit:
        flags.add(Flag.SF)

    if summed & overflow_bit:
        flags.add(Flag.CF)

        if not ((byte1.int_value & sign_bit) ^ (byte2.int_value & sign_bit)):
            flags.add(Flag.OF)

    return Byte(summed & 0b1111111), flags
