import sys

from byte_stream import BitStream
from core import Register, Word

def disassemble(filename):
    stream = BitStream(filename)
    op_code, = stream.read_int(7)

    if op_code & 0b1111 == 0b0000:
        op_name = "add"
    elif op_code & 0b1111 == 0b0001:
        op_name = "sub"

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
        source_out = source_word.hex_str()

        skip, = stream.read_int(3)

        assert(skip == 0)

    print(f"{op_name} {dest_out}, {source_out}")


if __name__ == "__main__":
    disassemble(sys.argv[1])
