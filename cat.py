import sys

def pad(bits_str):
    return ("00000000" + bits_str)[-8:]

def cat(filename):
    with open(filename, "rb") as f:
        byte_stream = f.read()

        # from bytes -> list of binary-encoding strings [ "11010", "0111", ... ]
        bits_strs = [
            bin(byte)[2:] for byte in byte_stream
        ]

        # left-pad up to a full byte "11010" -> "00011010"
        byte_strs = [ pad(bits_str) for bits_str in bits_strs ]

        # one big sequence of binary
        bin_str = "".join(byte_strs)

        while len(bin_str) >= 7:
            # take seven bits from the front of the string, reverse them
            byte7 = bin_str[:7]
            padded_bin_str = byte7
            reversed_padded_bin_str = padded_bin_str[::-1]

            # convert from "100" -> "0b100" -> 4 -> ascii_lookup[4]
            ascii_byte7 = chr(int("0b" + reversed_padded_bin_str, 2))
            print(ascii_byte7, end="")

            bin_str = bin_str[7:]

if __name__ == "__main__":
    cat(sys.argv[1])
