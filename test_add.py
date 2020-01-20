from core import Byte, Flag, Word
from ops.add import add_word

def test_one_plus_one():
    word, flags = add_word(Word.from_int(1), Word.from_int(1))
    assert(word.int_value() == 2)
    assert(not flags)

def test_set_zero_flag():
    word, flags = add_word(Word.from_int(0), Word.from_int(0))
    assert(word.int_value() == 0)
    assert(flags == set([Flag.ZF]))

def test_signed_flag():
    word, flags = add_word(
        Word(Byte(0), Byte(0), Byte(0), Byte(0b1000000)),
        Word(Byte(0), Byte(0), Byte(0), Byte(0b1))
    )
    assert(word == Word(Byte(0), Byte(0), Byte(0), Byte(0b1000001)))
    assert(flags == set([Flag.SF]))

def test_overflow_flag_on_7th_bit():
    word, flags = add_word(
        Word(Byte(0), Byte(0), Byte(0), Byte(0b1111111)),
        Word(Byte(0), Byte(0), Byte(0), Byte(0b0000001))
    )
    assert(word.int_value() == 0)
    assert(flags == set([Flag.CF]))

def test_unsigned_overflow_when_7th_bits_match():
    word, flags = add_word(
        Word(Byte(0), Byte(0), Byte(0), Byte(0b1000000)),
        Word(Byte(0), Byte(0), Byte(0), Byte(0b1000000))
    )
    assert(word.int_value() == 0)
    assert(flags == set([Flag.OF, Flag.CF]))

def test_full_word_addition_with_carry_across_bytes():
    word, flags = add_word(
        Word(Byte(0b1000000), Byte(0b0), Byte(0b1), Byte(0b0011)),
        Word(Byte(0b1000000), Byte(0b0), Byte(0b1), Byte(0b1000))
    )
    assert(word == Word(Byte(0b0), Byte(0b1), Byte(0b10), Byte(0b1011)))
    assert(not flags)
