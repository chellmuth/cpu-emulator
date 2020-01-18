from core import Byte, Flag

def add(byte1, byte2):
    flags = set()

    summed = byte1.int_value + byte2.int_value
    if summed == 0:
        flags.add(Flag.ZF)

    sign_bit = 1 << 6
    overflow_bit = 1 << 7

    if summed & sign_bit:
        flags.add(Flag.SF)

    if summed & overflow_bit:
        flags.add(Flag.CF)

        if not ((byte1.int_value & sign_bit) ^ (byte2.int_value & sign_bit)):
            flags.add(Flag.OF)

    return Byte(summed & 0b1111111), flags
