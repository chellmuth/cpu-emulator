import assembler
from byte_stream import ByteStream
from core import Byte

def get_bytes(instruction):
    bin_str = assembler.assemble_line(instruction.human())
    stream = ByteStream(bin_str)

    return [
        Byte(byte) for byte in stream.read(instruction.size)
    ]

def bytes_str(instruction):
    return "-".join([
        byte.hex_str(padded=True) for byte in get_bytes(instruction)
    ])
