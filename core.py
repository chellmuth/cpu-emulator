from enum import IntEnum

import util

class Register(IntEnum):
    ra = 0
    rb = 1
    rc = 2
    rd = 3
    rr = 4
    rs = 5
    rx = 6
    ry = 7
    rz = 8
    pc = 9

    # Not index-able
    sp = 10

class Flag(IntEnum):
    # Not index-able
    CF = 0 # Carry flag
    ZF = 1 # Zero flag
    OF = 2 # Overflow flag
    SF = 3 # Sign flag

class Word:
    size = 4

    @classmethod
    def from_int(cls, integer, endian="big"):
        mask = 0b1111111

        if endian == "little":
            return cls(
                Byte(integer >> 0 & mask),
                Byte(integer >> 7 & mask),
                Byte(integer >> 14 & mask),
                Byte(integer >> 21 & mask),
            )
        elif endian == "big":
            return cls(
                Byte(integer >> 21 & mask),
                Byte(integer >> 14 & mask),
                Byte(integer >> 7 & mask),
                Byte(integer >> 0 & mask),
            )
        else: raise ValueError

    # little-endian, byte1 is smallest
    def __init__(self, byte1, byte2, byte3, byte4):
        self.byte1 = byte1
        self.byte2 = byte2
        self.byte3 = byte3
        self.byte4 = byte4

    def low_byte(self):
        return self.byte1

    def __or__(self, other):
        return Word(
            self.byte1 | other.byte1,
            self.byte2 | other.byte2,
            self.byte3 | other.byte3,
            self.byte4 | other.byte4,
        )

    def hex_str(self, padded=True):
        hex_str = util.pad(self.byte1.hex_str(), 2) \
            + util.pad(self.byte2.hex_str(), 2) \
            + util.pad(self.byte3.hex_str(), 2) \
            + util.pad(self.byte4.hex_str(), 2)

        if padded:
            return "0x" + hex_str
        else:
            return "0x" + util.unpad_hex(hex_str)

    def int_value(self):
        return \
            self.byte1.int_value << 0 | \
            self.byte2.int_value << 7 | \
            self.byte3.int_value << 14 | \
            self.byte4.int_value << 21

    def __repr__(self):
        return "[word=" + "-".join([str(b) for b in [self.byte1, self.byte2, self.byte3, self.byte4]]) + "]"

class Byte:
    size = 1

    def __init__(self, int_value):
        assert((int_value >> 7) == 0)
        self.int_value = int_value

    def hex_str(self):
        return hex(self.int_value)[2:]

    def __eq__(self, other):
        return self.int_value == other.int_value

    def __or__(self, other):
        return Byte(self.int_value | other.int_value)

    def __repr__(self):
        return bin(self.int_value)[2:]
