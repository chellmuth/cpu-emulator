import sys
from dataclasses import dataclass
from typing import List, Optional

from byte_stream import BitStream
from core import Byte, Word
import disassembler

@dataclass
class Section:
    permissions: Byte
    offset: Word
    name: str
    size: Word

@dataclass
class SectionList:
    sections: List[Section]

@dataclass
class Symbol:
    name: str
    is_defined: bool
    section: Optional[Word]
    offset: Optional[Word]

@dataclass
class SymbolList:
    symbols: List[Symbol]


@dataclass
class Relocation:
    section: Word
    offset: Word
    symbol: str
    plus: Word

@dataclass
class RelocationList:
    relocations: List[Relocation]

@dataclass
class Segment:
    name: str
    offset: Word
    base: Word
    permissions: Byte
    _type: Byte

@dataclass
class SegmentList:
    segments: List[Segment]

@dataclass
class Orc:
    symbols: SymbolList
    relocations: RelocationList
    sections: SectionList
    segments: SegmentList
    data: str

def read_all(stream):
    data = []
    while(not stream.is_empty()):
        byte = read_byte(stream)
        data.append(byte)

    return data

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

def read_char(stream):
    char, = stream.read_int(7)
    return chr(char)

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

    section = None
    offset = None
    if is_defined:
        section = read_word(stream)
        offset = read_word(stream)

        print("section:", section)
        print("offset:", offset)

    return Symbol(
        name,
        is_defined,
        section,
        offset
    )

def read_symbol_table(stream):
    num_entries = read_word(stream)
    print("num_entries:", num_entries, num_entries.int_value())

    symbols = []
    for i in range(num_entries.int_value()):
        print(f"symbol: {i}")
        symbols.append(read_symbol(stream))

    return symbols

def read_relocation(stream):
    offset = read_word(stream)
    section = read_word(stream)
    symbol = read_text(stream)
    plus = read_word(stream)

    print("section:", section)
    print("offset:", offset)
    print("symbol:", symbol)
    print("plus:", plus)

    return Relocation(
        section,
        offset,
        symbol,
        plus
    )

def read_relocation_table(stream):
    num_entries = read_word(stream).int_value()
    print("relocation entries:", num_entries)

    relocations = []
    for _ in range(num_entries):
        relocations.append(read_relocation(stream))

    return relocations

def read_section(stream):
    permissions = read_byte(stream)
    # print("permissions:", permissions.hex_str())

    offset = read_word(stream)
    name = read_text(stream)
    size = read_word(stream)

    return Section(
        permissions,
        offset,
        name,
        size
    )

def read_section_table(stream):
    num_entries = read_word(stream).int_value()
    print("section entries:", num_entries)

    sections = []
    for _ in range(num_entries):
        sections.append(read_section(stream))

    return sections

def read_segment(stream):
    name = read_text(stream)
    offset = read_word(stream)
    base = read_word(stream)

    print("name:", name)
    print("offset:", offset)
    print("base:", base)

    permissions = read_byte(stream)
    # print("permissions:", permissions.hex_str())

    segment_type = read_byte(stream)
    print("segment type:", segment_type.hex_str())

    return Segment(
        name,
        offset,
        base,
        permissions,
        segment_type
    )

def read_segment_table(stream):
    num_entries = read_word(stream).int_value()

    segments = []
    for _ in range(num_entries):
        segments.append(read_segment(stream))

    return segments

def cat_section(orc, section, offset=0):
    base = section.offset.int_value()

    program = ""
    for i in range(section.size.int_value() - offset):
        b = orc.data[base + offset + i]
        program += b.bin_str(padded=True)

    bs = BitStream(program)

    bs.cat()

def cat_symbol(orc, symbol):
    print("cat symbol:", symbol)
    section = orc.section_table[symbol.section.int_value() - 1]
    cat_section(orc, section, offset=symbol.offset.int_value())

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

    data = read_all(stream)

    orc = Orc(
        symbol_table,
        relocation_table,
        section_table,
        segment_table,
        data
    )

    breakpoint()

if __name__ == "__main__":
    parse(sys.argv[1])
