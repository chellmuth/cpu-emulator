import util

class ByteStream:
    def __init__(self, filename, reverse_bits=False):
        self.reverse_bits = reverse_bits

        real_bytes = open(filename, "rb").read()

        # from bytes -> list of binary-encoding strings [ "11010", "0111", ... ]
        bits_strs = [
            bin(byte)[2:] for byte in real_bytes
        ]

        # left-pad up to a full byte "11010" -> "00011010"
        byte_strs = [ util.pad(bits_str, 8) for bits_str in bits_strs ]

        # one big sequence of binary
        self.bin_str = "".join(byte_strs)

        # print(self.bin_str)

    def is_empty(self):
        # todo: pad the input to always have a full byte at the end
        return len(self.bin_str) < 7

    def read(self, byte_count):
        byte_list = []
        for _ in range(byte_count):
            if len(self.bin_str) >= 7:
                # take seven bits from the front of the string, reverse them
                byte_str = self.bin_str[:7]

                if self.reverse_bits:
                    reversed_byte_str = byte_str[::-1]
                else:
                    reversed_byte_str = byte_str

                byte_list.append(int(reversed_byte_str, 2))

                self.bin_str = self.bin_str[7:]

        return byte_list


class BitStream:
    @classmethod
    def from_filename(cls, filename):
        real_bytes = open(filename, "rb").read()
        return cls(real_bytes)

    def __init__(self, real_bytes):
        # from bytes -> list of binary-encoding strings [ "11010", "0111", ... ]
        bits_strs = [
            bin(byte)[2:] for byte in real_bytes
        ]

        # left-pad up to a full byte "11010" -> "00011010"
        byte_strs = [ util.pad(bits_str, 8) for bits_str in bits_strs ]

        # one big sequence of binary
        self.bin_str = "".join(byte_strs)
        # print(self.bin_str)

    def is_empty(self):
        # todo: pad the input to always have a full byte at the end
        return len(self.bin_str) < 7

    def read_int(self, bit_count):
        assert(bit_count <= 7)

        bit_str = self.bin_str[:bit_count]
        self.bin_str = self.bin_str[bit_count:]

        return int(bit_str, 2),

    def read_str(self, bit_count):
        bit_str = self.bin_str[:bit_count]
        self.bin_str = self.bin_str[bit_count:]

        return bit_str,
