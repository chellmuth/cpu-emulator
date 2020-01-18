from enum import IntEnum

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
    @classmethod
    def from_int(cls, integer):
        mask = 0b1111111
        return cls(
            Byte(integer >> 0 & mask),
            Byte(integer >> 7 & mask),
            Byte(integer >> 14 & mask),
            Byte(integer >> 21 & mask),
        )

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

    def __repr__(self):
        return "[word=" + "-".join([str(b) for b in [self.byte1, self.byte2, self.byte3, self.byte4]]) + "]"

class Byte:
    def __init__(self, int_value):
        assert((int_value >> 7) == 0)
        self.int_value = int_value

    def __eq__(self, other):
        return self.int_value == other.int_value

    def __or__(self, other):
        return Byte(self.int_value | other.int_value)

    def __repr__(self):
        return bin(self.int_value)[2:]
