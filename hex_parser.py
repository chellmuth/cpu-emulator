import util

def _split_bytes(hex_str):
    if len(hex_str) % 2 == 1:
        hex_str = "0" + hex_str

    return [
        hex_str[i * 2 : i * 2 + 2]
        for i in range(len(hex_str) // 2)
    ]

def _int_to_padded_bin_str(int_value, endian="little"):
    return util.pad(bin(int_value)[2:], 7, endian)

def parse_hex_str(hex_str):
    assert(hex_str.startswith("0x"))

    int_values = []

    byte_strs = _split_bytes(hex_str[2:])
    for byte_str in byte_strs:
        int_value = int(byte_str, 16)

        if int_value & 0b10000000:
            breakpoint()
            raise ValueError

        int_values.append(int_value)

    return "".join(
        _int_to_padded_bin_str(i, endian="little")
        for i in int_values
    )
