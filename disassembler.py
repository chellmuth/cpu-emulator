import sys

from byte_stream import BitStream
from core import Register, Word

def disassemble(filename):
    stream = BitStream(filename)

    while not stream.is_empty():
        _disassemble_instruction(stream)

op_names = {
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

def _disassemble_instruction(stream):
    op_code, = stream.read_int(7)
    op_name = op_names[op_code & 0b1111]

    if op_code & 0b1110000 == 0b0100000:
        source, = stream.read_int(4)
        source_out = Register(source).name

        dest, = stream.read_int(4)
        dest_out = Register(dest).name

        skip, = stream.read_int(6)

        assert(skip == 0)
    elif op_code & 0b1110000 == 0b0110000:
        dest, = stream.read_int(4)
        dest_out = Register(dest).name

        source, = stream.read_str(28)
        source_word = Word.from_int(int(source, 2))
        source_out = source_word.hex_str(padded=False)

        skip, = stream.read_int(3)

        assert(skip == 0)
    else:
        raise ValueError

    print(f"{op_name} {dest_out}, {source_out}")


if __name__ == "__main__":
    disassemble(sys.argv[1])
