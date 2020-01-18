def pad(bits_str, length):
    return ("0" * length + bits_str)[-length:]

def fill_to_real_byte(bits_str):
    count = 8 - (len(bits_str) % 8)
    return bits_str + ("0" * count )
