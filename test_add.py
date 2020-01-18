from core import Byte, Flag
from ops.add import add

def test_one_plus_one():
    byte, flags = add(Byte(0b1), Byte(0b1))
    assert(byte == Byte(0b10))
    assert(not flags)

def test_set_zero_flag():
    byte, flags = add(Byte(0b0), Byte(0b0))
    assert(byte == Byte(0b0))
    assert(flags == set([Flag.ZF]))

def test_signed_flag():
    byte, flags = add(Byte(0b1000000), Byte(0b1))
    assert(byte == Byte(0b1000001))
    assert(flags == set([Flag.SF]))

def test_overflow_flag_on_7th_bit():
    byte, flags = add(Byte(0b1111111), Byte(0b1))
    assert(byte == Byte(0b0))
    assert(flags == set([Flag.CF]))

def test_unsigned_overflow_when_7th_bits_match():
    byte, flags = add(Byte(0b1000000), Byte(0b1000000))
    assert(byte == Byte(0b0))
    assert(flags == set([Flag.OF, Flag.CF]))

