from typing import Optional

import ops

class Instruction:
    size: Optional[int] = None

    def human(self):
        raise Exception("Unimplemented")

    def debug_str(self):
        return "HI"

    def run(self, machine):
        raise Exception("Unimplemented")

class Type1RegisterInstruction(Instruction):
    size = 3

    def __init__(self, op_name, source_register, dest_register):
        self.op_name = op_name
        self.source_register = source_register
        self.dest_register = dest_register

    def debug_str(self):
        return "010-" \
            + str(ops.op_codes[self.op_name]) + "-" \
            + str(int(self.source_register)) + "-" \
            + str(int(self.dest_register))

    def human(self):
        source_out = self.source_register.name
        dest_out = self.dest_register.name

        return f"{self.op_name} {source_out}, {dest_out}"

class Type1ConstantInstruction(Instruction):
    size = 6

    def __init__(self, op_name, dest_register, source_word):
        self.op_name = op_name
        self.dest_register = dest_register
        self.source_word = source_word

    def debug_str(self):
        return "011-" \
            + str(ops.op_codes[self.op_name]) + "-" \
            + str(int(self.dest_register)) + "-" \
            + str(self.source_word.int_value())

    def human(self):
        source_out = self.source_word.hex_str()
        dest_out = self.dest_register.name

        return f"{self.op_name} {dest_out}, {source_out}"

class Type2RegisterInstruction(Instruction):
    size = 2

    def __init__(self, op_name, value_register):
        self.op_name = op_name
        self.value_register = value_register

    def debug_str(self):
        return "100-" \
            + str(ops.op_codes[self.op_name]) + "-" \
            + str(int(self.value_register))

    def human(self):
        value_out = self.value_register.name

        return f"{self.op_name} {value_out}"

class Type2ConstantInstruction(Instruction):
    size = 5

    def __init__(self, op_name, value_word):
        self.op_name = op_name
        self.value_word = value_word

    def human(self):
        value_out = self.value_word.hex_str(padded=False)

        return f"{self.op_name} {value_out}"
