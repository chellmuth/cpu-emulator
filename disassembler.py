import sys

from byte_stream import ByteStream

def disassemble(filename):
    disassembled_lines = []

    stream = ByteStream(filename)
    op_code, = stream.read(1)

    if op_code & 0b1111 == 0b0000:
        print("ADD")
    elif op_code & 0b1111 == 0b0001:
        print("SUB")

    if op_code & 0b1110000 == 0b0100000:
        print("REGISTER")
    elif op_code & 0b1110000 == 0b0110000:
        print("CONSTANT")

    print(disassembled_lines)


if __name__ == "__main__":
    disassemble(sys.argv[1])
