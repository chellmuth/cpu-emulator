import util

class ByteStream:
    def __init__(self, filename):
        real_bytes = open(filename, "rb").read()

        # from bytes -> list of binary-encoding strings [ "11010", "0111", ... ]
        bits_strs = [
            bin(byte)[2:] for byte in real_bytes
        ]

        # left-pad up to a full byte "11010" -> "00011010"
        byte_strs = [ util.pad(bits_str, 8) for bits_str in bits_strs ]

        # one big sequence of binary
        self.bin_str = "".join(byte_strs)


    def read(self, byte_count):
        byte_list = []
        for _ in range(byte_count):
            if len(self.bin_str) >= 7:
                # take seven bits from the front of the string, reverse them
                byte_str = self.bin_str[:7]
                reversed_byte_str = byte_str[::-1]

                # byte_list.append(int(reversed_byte_str, 2))
                byte_list.append(int(byte_str, 2))

        return byte_list


class BitStream:
    def __init__(self, filename):
        real_bytes = open(filename, "rb").read()

        # from bytes -> list of binary-encoding strings [ "11010", "0111", ... ]
        bits_strs = [
            bin(byte)[2:] for byte in real_bytes
        ]

        # left-pad up to a full byte "11010" -> "00011010"
        byte_strs = [ util.pad(bits_str, 8) for bits_str in bits_strs ]

        # one big sequence of binary
        self.bin_str = "".join(byte_strs)
        print(self.bin_str)

    def is_empty(self):
        return len(self.bin_str) == 0

    def read_int(self, bit_count):
        assert(bit_count <= 7)

        bit_str = self.bin_str[:bit_count]
        self.bin_str = self.bin_str[bit_count:]

        return int(bit_str, 2),

    def read_str(self, bit_count):
        bit_str = self.bin_str[:bit_count]
        self.bin_str = self.bin_str[bit_count:]

        return bit_str,