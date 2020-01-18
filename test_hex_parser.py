from hex_parser import parse_hex_str

import pytest

def test_basic():
    assert parse_hex_str("0x0") == "0000000"
    assert parse_hex_str("0x1") == "0000001"
    assert parse_hex_str("0x2") == "0000010"
    assert parse_hex_str("0x3") == "0000011"
    assert parse_hex_str("0x4") == "0000100"
    assert parse_hex_str("0x5") == "0000101"
    assert parse_hex_str("0x6") == "0000110"
    assert parse_hex_str("0x7") == "0000111"
    assert parse_hex_str("0x8") == "0001000"
    assert parse_hex_str("0x9") == "0001001"
    assert parse_hex_str("0xa") == "0001010"
    assert parse_hex_str("0xb") == "0001011"
    assert parse_hex_str("0xc") == "0001100"
    assert parse_hex_str("0xd") == "0001101"
    assert parse_hex_str("0xe") == "0001110"
    assert parse_hex_str("0xf") == "0001111"

    assert parse_hex_str("0x10") == "0010000"
    assert parse_hex_str("0x11") == "0010001"
    assert parse_hex_str("0x1a") == "0011010"

    assert parse_hex_str("0x21") == "0100001"
    assert parse_hex_str("0x41") == "1000001"
    assert parse_hex_str("0x71") == "1110001"

    assert parse_hex_str("0x7f") == "1111111"

    with pytest.raises(ValueError):
        parse_hex_str("0x80")

def test_parse_bytes__little_endian():
    assert parse_hex_str("0x0103070f") == "0001111000011100000110000001"
