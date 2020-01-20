from core import Byte, Flag, Word
from ops.subtract import subtract_word

def test_three_minus_one():
    word, flags = subtract_word(Word.from_int(3), Word.from_int(1))
    assert(word.int_value() == 2)
    assert(not flags)

def test_one_minus_one_sets_zero_flag():
    word, flags = subtract_word(Word.from_int(1), Word.from_int(1))
    assert(word.int_value() == 0)
    assert(flags == set([Flag.ZF]))

def test_signed_flag():
    # result = -2 -> (2 == 0b0000010)
    # 2's complement -> 0b1111101 + 0b1 -> 0b1111110
    word, flags = subtract_word(Word.from_int(1), Word.from_int(3))
    assert(word == Word(Byte(0b1111110), Byte(0x7f), Byte(0x7f), Byte(0x7f)))
    assert(flags == set([Flag.SF]))

def test_signed_underflow():
    # TODO: Support negative numbers!
    pass

# def test_overflow_flag_on_7th_bit():
#     word, flags = add_word(
#         Word(Byte(0), Byte(0), Byte(0), Byte(0b1111111)),
#         Word(Byte(0), Byte(0), Byte(0), Byte(0b0000001))
#     )
#     assert(word.int_value() == 0)
#     assert(flags == set([Flag.CF]))

# def test_unsigned_overflow_when_7th_bits_match():
#     word, flags = add_word(
#         Word(Byte(0), Byte(0), Byte(0), Byte(0b1000000)),
#         Word(Byte(0), Byte(0), Byte(0), Byte(0b1000000))
#     )
#     assert(word.int_value() == 0)
#     assert(flags == set([Flag.OF, Flag.CF]))

# def test_full_word_addition_with_carry_across_bytes():
#     word, flags = add_word(
#         Word(Byte(0b1000000), Byte(0b0), Byte(0b1), Byte(0b0011)),
#         Word(Byte(0b1000000), Byte(0b0), Byte(0b1), Byte(0b1000))
#     )
#     assert(word == Word(Byte(0b0), Byte(0b1), Byte(0b10), Byte(0b1011)))
#     assert(not flags)
