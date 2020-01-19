import sys

from byte_stream import BitStream
from core import Register, Word

def disassemble(filename):
    stream = BitStream(filename)

    while not stream.is_empty():
        _disassemble_instruction(stream)

type_1_op_names = {
    0: "ADD",
    1: "SUB",
    2: "MUL",
    3: "DIV",
    4: "CMP",
    5: "TST",
    6: "AND",
    7: "ORR",
    8: "XOR",
    9: "STR",
    10: "STB",
    11: "LOD",
}

type_2_op_names = {
    0: "JMP",
}

op_names = {
    0b010: type_1_op_names,
    0b011: type_1_op_names,
    0b100: type_2_op_names,
    0b101: type_2_op_names,
}

def _disassemble_instruction(stream):
    type_code, = stream.read_int(3)
    op_code, = stream.read_int(4)

    if stream.is_empty():
        # Our file was padded with 7 bits to complete the byte
        # Made it look like we had an instruction when we don't
        return

    op_name = op_names[type_code][op_code]
    if type_code == 0b010:
        source, = stream.read_int(4)
        source_out = Register(source).name

        dest, = stream.read_int(4)
        dest_out = Register(dest).name

        skip, = stream.read_int(6)
        assert(skip == 0)

        print(f"{op_name} {dest_out}, {source_out}")
    elif type_code == 0b011:
        dest, = stream.read_int(4)
        dest_out = Register(dest).name

        source, = stream.read_str(28)
        source_word = Word.from_int(int(source, 2))
        source_out = source_word.hex_str(padded=False)

        skip, = stream.read_int(3)
        assert(skip == 0)

        print(f"{op_name} {dest_out}, {source_out}")
    elif type_code == 0b100:
        value, = stream.read_int(4)
        value_out = Register(value).name

        skip, = stream.read_int(3)
        assert(skip == 0)

        print(f"{op_name} {value_out}")
    elif type_code == 0b101:
        value, = stream.read_str(28)
        value_word = Word.from_int(int(value, 2))
        value_out = value_word.hex_str(padded=False)

        print(f"{op_name} {value_out}")
    else:
        raise ValueError



if __name__ == "__main__":
    disassemble(sys.argv[1])
