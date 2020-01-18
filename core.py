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

class Byte:
    def __init__(self, int_value):
        assert(int_value >> 7) == 0
        self.int_value = int_value

    def __eq__(self, other):
        return self.int_value == other.int_value

    def __repr__(self):
        return bin(self.int_value)[2:]
