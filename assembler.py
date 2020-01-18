import sys

import util
from core import Register
from hex_parser import parse_hex_str

def is_register(arg):
    return arg.startswith("r")

def get_register_id(register_name):
    return util.pad(bin(Register[register_name])[2:], 4)

def get_const_binary(hex_str):
    return parse_hex_str(hex_str)

def assemble(filename):
    assembled_lines = []

    with open(filename, "r") as f:
        line = f.readline()
        tokens = line.replace(",", "").split(" ")
        command, arg1, arg2 = tokens

        if command == "ADD":
            dest = get_register_id(arg1)

            if is_register(arg2):
                type_code = "010"
                source = get_register_id(arg2)
                right_padding = "0" * 6
            else:
                type_code = "011"
                source = get_const_binary(arg2)
                right_padding = "0" * 3

            assembled_lines.append(
                type_code + "0000" + dest + source + right_padding
            )

    print(assembled_lines)

    with open("out.o", "wb") as f:
        for line in assembled_lines:
            line = util.fill_to_real_byte(line)
            byte_count = len(line) // 8

            int_values = []
            for i in range(byte_count):
                byte_str = line[i*8 : i*8 + 8]
                int_value = int(byte_str, 2)
                int_values.append(int_value)

            f.write(bytearray(int_values))

if __name__ == "__main__":
    assemble(sys.argv[1])
