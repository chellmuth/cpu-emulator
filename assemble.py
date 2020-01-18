import sys

from core import Register

def pad(bits_str, length):
    return ("0" * length + bits_str)[-length:]

def is_register(arg):
    return arg.startswith("r")

def get_register_id(register_name):
    return pad(bin(Register[register_name])[2:], 4)

def get_const_binary(int_value):
    return pad("111", 28)

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

if __name__ == "__main__":
    assemble(sys.argv[1])
