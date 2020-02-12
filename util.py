def pad(bits_str, length, endian="little"):
    if endian == "big":
        return ("0" * length + bits_str)[-length:]
    else:
        return (bits_str + "0" * length)[:length]

def pad_left(bits_str, length):
    return ("0" * length + bits_str)[-length:]

def pad_right(bits_str, length):
    return (bits_str + "0" * length)[:length]

def fill_to_real_byte(bits_str):
    count = 8 - (len(bits_str) % 8)
    return bits_str + ("0" * count )

def int_to_bits(int_value, length):
    return pad(bin(int_value)[2:], length)

def unpad_hex(hex_str):
    return hex(int(hex_str, 16))[2:]
