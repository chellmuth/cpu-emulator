import sys

from byte_stream import BitStream
from core import Byte, Word

def read_word(stream):
    b1, = stream.read_int(7)
    b2, = stream.read_int(7)
    b3, = stream.read_int(7)
    b4, = stream.read_int(7)

    return Word(Byte(b1), Byte(b2), Byte(b3), Byte(b4))

def read_byte(stream):
    b, = stream.read_int(7)

    return Byte(b)

def read_bool(stream):
    b, = stream.read_int(7)
    assert b == 0 or b == 1
    return b

def read_text(stream):
    text = ""

    char, = stream.read_int(7)
    while char != 0:
        text += chr(char)
        char, = stream.read_int(7)

    return text

def read_symbol(stream):
    name = read_text(stream)
    print("name:", name)

    is_defined = read_bool(stream)
    print("is defined:", is_defined)

    if is_defined:
        section = read_word(stream)
        offset = read_word(stream)

        print("section:", section)
        print("offset:", offset)

def read_symbol_table(stream):
    num_entries = read_word(stream)
    print("num_entries:", num_entries, num_entries.int_value())

    for i in range(num_entries.int_value()):
        print(f"symbol: {i}")
        read_symbol(stream)

def read_relocation(stream):
    section = read_word(stream)
    offset = read_word(stream)
    symbol = read_text(stream)
    plus = read_word(stream)

    print("section:", section)
    print("offset:", offset)
    print("symbol:", symbol)
    print("plus:", plus)

def read_relocation_table(stream):
    num_entries = read_word(stream).int_value()
    print("relocation entries:", num_entries)
    for _ in range(num_entries):
        read_relocation(stream)

def read_section(stream):
    permissions = read_byte(stream)
    print("permissions:", permissions.hex_str())

    offset = read_word(stream)
    name = read_text(stream)
    size = read_word(stream)

def read_section_table(stream):
    num_entries = read_word(stream).int_value()
    print("section entries:", num_entries)
    for _ in range(num_entries):
        read_section(stream)

def read_segment(stream):
    name = read_text(stream)
    offset = read_word(stream)
    base = read_word(stream)

    print("name:", name)
    print("offset:", offset)
    print("base:", base)

    permissions = read_byte(stream)
    print("permissions:", permissions.hex_str())

    segment_type = read_byte(stream)
    print("segment type:", segment_type.hex_str())

def read_segment_table(stream):
    num_entries = read_word(stream).int_value()
    for _ in range(num_entries):
        read_segment(stream)

def parse(filename):
    stream = BitStream.from_filename(filename, flip_bit_endianness=True)

    orc_header = read_text(stream)
    assert(orc_header == "orc")

    filetype, = stream.read_int(7)
    has_entry_point = read_bool(stream)

    print(filetype)
    print(has_entry_point)

    if has_entry_point == 1:
        entry_point = read_word(stream)
        print("entry point:", entry_point, entry_point.hex_str(), entry_point.int_value())

    symbol_table = read_symbol_table(stream)
    relocation_table = read_relocation_table(stream)
    section_table = read_section_table(stream)
    segment_table = read_segment_table(stream)

    data = stream.bin_str


if __name__ == "__main__":
    parse(sys.argv[1])
