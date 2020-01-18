import sys

from byte_stream import BitStream

def disassemble(filename):
    disassembled_lines = []

    stream = BitStream(filename)
    op_code, = stream.read_int(7)

    if op_code & 0b1111 == 0b0000:
        print("ADD")
    elif op_code & 0b1111 == 0b0001:
        print("SUB")

    if op_code & 0b1110000 == 0b0100000:
        print("REGISTER")

        source, = stream.read_int(4)
        dest, = stream.read_int(4)
        skip, = stream.read_int(6)

        assert(skip == 0)

        print("SOURCE:", source)
        print("DEST:", dest)

    elif op_code & 0b1110000 == 0b0110000:
        print("CONSTANT")

        dest, = stream.read_int(4)
        source, = stream.read_str(7)
        skip, = stream.read_int(3)

        assert(skip == 0)

        print("SOURCE:", source)
        print("DEST:", dest)

    print(disassembled_lines)


if __name__ == "__main__":
    disassemble(sys.argv[1])
