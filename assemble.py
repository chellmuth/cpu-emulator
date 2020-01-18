import sys

from core import Register

def is_register(arg):
    return arg.startswith("r")

def get_register_id(register_name):
    # NEEDS TO BE FORMATTED!
    return bin(Register[register_name])[2:]

def get_const_binary(int_value):
    return "111"

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
            else:        
                type_code = "011"
                source = get_const_binary(arg2)

            assembled_lines.append(
                type_code + "0000" + dest + source
            )

    print(assembled_lines)
if __name__ == "__main__":
    assemble(sys.argv[1])
