import assembler
from byte_stream import ByteStream
from core import Byte

class Instruction:
    def human(self):
        raise Exception("Unimplemented")

    def words(self):
        raise Exception("Unimplemented")

    def run(self, machine):
        raise Exception("Unimplemented")

class Type1RegisterInstruction(Instruction):
    def __init__(self, op_name, source_register, dest_register):
        self.op_name = op_name
        self.source_register = source_register
        self.dest_register = dest_register

    def human(self):
        source_out = self.source_register.name
        dest_out = self.dest_register.name

        return f"{self.op_name} {source_out}, {dest_out}"

    def bytes(self):
        bin_str = assembler.assemble_line(self.human())
        stream = ByteStream(bin_str)

        return [
            Byte(byte) for byte in stream.read(3)
        ]

class Type1ConstantInstruction(Instruction):
    def __init__(self, op_name, dest_register, source_word):
        self.op_name = op_name
        self.dest_register = dest_register
        self.source_word = source_word

    def human(self):
        source_out = self.source_word.hex_str(padded=False)
        dest_out = self.dest_register.name

        return f"{self.op_name} {dest_out}, {source_out}"

    def bytes(self):
        bin_str = assembler.assemble_line(self.human())
        stream = ByteStream(bin_str)

        return [
            Byte(byte) for byte in stream.read(6)
        ]

class Type2RegisterInstruction(Instruction):
    def __init__(self, op_name, value_register):
        self.op_name = op_name
        self.value_register = value_register

    def human(self):
        value_out = self.value_register.name

        return f"{self.op_name} {value_out}"

class Type2ConstantInstruction(Instruction):
    def __init__(self, op_name, value_word):
        self.op_name = op_name
        self.value_word = value_word

    def human(self):
        value_out = self.value_word.hex_str(padded=False)

        return f"{self.op_name} {value_out}"
