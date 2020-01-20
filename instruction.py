import instruction_base
import ops.bitwise_or
from core import Word, Byte
from emulator import MachineUpdate
from ops.add import add

def type1_register_factory(op_name, source_register, dest_register):
    cls_lookup = {
        "ADD": AddRegisterInstruction,
        "ORR": ops.bitwise_or.BitwiseOrRegisterInstruction,
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](source_register, dest_register)
    else:
        return instruction_base.Type1RegisterInstruction(
            op_name,
            source_register,
            dest_register
        )

def type1_constant_factory(op_name, dest_register, source_word):
    cls_lookup = {
        "ADD": AddConstantInstruction,
        "ORR": ops.bitwise_or.BitwiseOrConstantInstruction,
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](dest_register, source_word)
    else:
        return instruction_base.Type1ConstantInstruction(
            op_name,
            dest_register,
            source_word
        )

def type2_register_factory(op_name, value_register):
    cls_lookup = {
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](value_register)
    else:
        return instruction_base.Type2RegisterInstruction(op_name, value_register)

def type2_constant_factory(op_name, value_word):
    cls_lookup = {
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](value_word)
    else:
        return instruction_base.Type2ConstantInstruction(op_name, value_word)

class NopInstruction(instruction_base.Instruction):
    def human(self):
        return "NOP"

class RetInstruction(instruction_base.Instruction):
    def human(self):
        return "RET"

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
