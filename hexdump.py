import sys

from byte_stream import ByteStream

def hexdump(filename):
    stream = ByteStream.from_filename(filename, reverse_bits=True)

    while not stream.is_empty():
        byte, = stream.read(1)
        print(hex(byte)[2:], end=" ")

    print()

if __name__ == "__main__":
    hexdump(sys.argv[1])
