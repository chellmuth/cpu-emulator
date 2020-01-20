import sys

import disassembler
import util
from byte_stream import BitStream
from core import Register
from hex_parser import parse_hex_str

def is_register(arg):
    return arg.startswith("r")

def get_register_id(register_name):
    return util.pad(bin(Register[register_name])[2:], 4)

def get_const_binary(hex_str, length=28):
    return util.pad(parse_hex_str(hex_str), length)

instructions = {
    "ADD": (1, 0),
    "SUB": (1, 1),
    "MUL": (1, 2),
    "DIV": (1, 3),
    "CMP": (1, 4),
    "TST": (1, 5),
    "AND": (1, 6),
    "ORR": (1, 7),
    "XOR": (1, 8),
    "STR": (1, 9),
    "STB": (1, 10),
    "LOD": (1, 11),

    "JMP": (2, 0),
    "JLT": (2, 1),
    "JEQ": (2, 2),
    "CAL": (2, 3),
    "PSH": (2, 4),
    "POP": (2, 5),
    "NOT": (2, 6),
    "OUT": (2, 7),
    "INP": (2, 8),
    "AMP": (2, 9),
    "ALT": (2, 10),
    "AEQ": (2, 11),
    "AAL": (2, 12),

    "RET": (3, 0),
    "NOP": (3, 1),
}

def assemble(filename):
    assembled_lines = []

    with open(filename, "r") as f:
        assembled_lines = [
            assemble_line(line)
            for line in f.readlines()
        ]

    # print(assembled_lines)

    with open("out.o", "wb") as f:
        contents = "".join(assembled_lines)

        contents = util.fill_to_real_byte(contents)
        byte_count = len(contents) // 8

        int_values = []
        for i in range(byte_count):
            byte_str = contents[i*8 : i*8 + 8]
            int_value = int(byte_str, 2)
            int_values.append(int_value)

        f.write(bytearray(int_values))

def assemble_line(line):
    split_instruction = line.strip().replace(",", "").split(" ", maxsplit=1)
    if len(split_instruction) > 1:
        command, tokens = split_instruction
    else:
        command, = split_instruction
        tokens = None

    instruction = instructions[command]
    instruction_type, op_code = instruction

    if instruction_type == 1:
        arg1, arg2 = tokens.split(" ")

        dest = get_register_id(arg1)

        if is_register(arg2):
            type_code = "010"
            source = get_register_id(arg2)
            right_padding = "0" * 6
        else:
            type_code = "011"
            source = get_const_binary(arg2)
            right_padding = "0" * 3

        return type_code + util.int_to_bits(op_code, 4) + dest + source + right_padding

    elif instruction_type == 2:
        arg = tokens

        if is_register(arg):
            type_code = "100"
            value = get_register_id(arg)
            right_padding = "0" * 3
        else:
            type_code = "101"
            value = get_const_binary(arg)
            right_padding = ""

        return type_code + util.int_to_bits(op_code, 4) + value + right_padding

    elif instruction_type == 3:
        arg = tokens

        type_code = "11"
        right_padding = "0" * 4

        return type_code + util.int_to_bits(op_code, 1) + right_padding

def parse_to_instruction(text):
    bin_str = assemble_line(text)
    stream = BitStream(bin_str)
    instruction = disassembler.disassemble_instruction(stream)
    return instruction

if __name__ == "__main__":
    assemble(sys.argv[1])
