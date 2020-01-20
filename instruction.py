from core import Word, Byte
from emulator import MachineUpdate
from ops.add import add

class Instruction:
    def human(self):
        raise Exception("Unimplemented")

    def run(self, machine):
        raise Exception("Unimplemented")

class Type1RegisterInstruction(Instruction):
    @classmethod
    def factory(cls, op_name, source_register, dest_register):
        cls_lookup = {
            "ADD": AddRegisterInstruction,
        }

        if op_name in cls_lookup:
            return cls_lookup[op_name](source_register, dest_register)
        else:
            return cls(op_name, source_register, dest_register)

    def __init__(self, op_name, source_register, dest_register):
        self.op_name = op_name
        self.source_register = source_register
        self.dest_register = dest_register

    def human(self):
        source_out = self.source_register.name
        dest_out = self.dest_register.name

        return f"{self.op_name} {source_out}, {dest_out}"

class Type1ConstantInstruction(Instruction):
    @classmethod
    def factory(cls, op_name, dest_register, source_word):
        cls_lookup = {
            "ADD": AddConstantInstruction
        }

        if op_name in cls_lookup:
            return cls_lookup[op_name](dest_register, source_word)
        else:
            return cls(op_name, dest_register, source_word)

    def __init__(self, op_name, dest_register, source_word):
        self.op_name = op_name
        self.dest_register = dest_register
        self.source_word = source_word

    def human(self):
        source_out = self.source_word.hex_str(padded=False)
        dest_out = self.dest_register.name

        return f"{self.op_name} {dest_out}, {source_out}"

class Type2RegisterInstruction(Instruction):
    @classmethod
    def factory(cls, op_name, value_register):
        cls_lookup = {
        }

        if op_name in cls_lookup:
            return cls_lookup[op_name](value_register)
        else:
            return cls(op_name, value_register)

    def __init__(self, op_name, value_register):
        self.op_name = op_name
        self.value_register = value_register

    def human(self):
        value_out = self.value_register.name

        return f"{self.op_name} {value_out}"

class Type2ConstantInstruction(Instruction):
    @classmethod
    def factory(cls, op_name, value_word):
        cls_lookup = {
        }

        if op_name in cls_lookup:
            return cls_lookup[op_name](value_word)
        else:
            return cls(op_name, value_word)

    def __init__(self, op_name, value_word):
        self.op_name = op_name
        self.value_word = value_word

    def human(self):
        value_out = self.value_word.hex_str(padded=False)

        return f"{self.op_name} {value_out}"

class NopInstruction(Instruction):
    def human(self):
        return "NOP"

class RetInstruction(Instruction):
    def human(self):
        return "RET"

class AddRegisterInstruction(Type1RegisterInstruction):
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

class AddConstantInstruction(Type1ConstantInstruction):
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
