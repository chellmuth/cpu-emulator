try:
    import readline
except:
    pass

import click

import hex_parser
import emulator
import orc_parser
from core import Byte, Register, Word

commands = [
    "continue",
    "debug",
    "disassemble",
    "memory",
    "print",
    "registers",
    "step",
    "web",
]

def completer(text, state):
    tokens = readline.get_line_buffer().split()
    if len(tokens) > 1:
        return None

    possibilities = []
    for command in commands:
        if command.startswith(text):
            possibilities.append(command)

    if state < len(possibilities):
        return possibilities[state] + " "

    return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

class HexIntParamType(click.ParamType):
    name = "hexint"

    def convert(self, value, param, ctx):
        try:
            if value[:2].lower() == "0x":
                return hex_parser.int_from_by7e_hex(value)
            self.fail("Expected value to start with 0x")
        except TypeError:
            self.fail("Type error")
        except ValueError:
            self.fail("Value error")

hexint = HexIntParamType()

@click.command()
@click.argument("filename")
@click.option("--break", "break_", type=hexint)
@click.option("--input", "input_", type=hexint, multiple=True)
def run(filename, break_, input_):
    orc = orc_parser.parse(filename)

    machine = emulator.Machine()
    if input_:
        machine.stdin = list(input_)

    for segment in orc.segments:
        for i in range(segment.size.int_value()):
            memory_location = Word.from_int(segment.base.int_value() + i)
            data_location = segment.offset.int_value() + i
            data_value = orc.data[data_location]
            machine.memory.write_byte(memory_location, data_value)

    machine.registers[Register.pc] = orc.entry_point

    instruction = machine.next_instruction()
    while instruction:
        print(machine.registers[Register.pc].hex_str(human=True), instruction.human())

        if machine.registers[Register.pc].int_value() == break_:
            command = input("> ").strip()
            while command:
                if command == "debug":
                    breakpoint()
                elif command == "continue":
                    break
                elif command == "step":
                    machine.run(instruction)
                    instruction = machine.next_instruction()
                    if instruction:
                        print(instruction.human())
                elif command == "registers":
                    for register in Register:
                        print(f"{register.name}: {machine.registers[register].hex_str()}")
                elif command.startswith("print"):
                    _, variable = command.split(" ")

                    if variable.startswith("0x"):
                        address_hex = variable
                        address = hex_parser.int_from_by7e_hex(address_hex)
                        word = machine.memory.read_word(address)
                    else:
                        register_name = variable
                        register = Register[register_name]
                        word = machine.registers[register]

                    print(word)
                elif command.startswith("memory"):
                    _, address_hex = command.split(" ")
                    address = hex_parser.int_from_by7e_hex(address_hex)

                    for section in range(4):
                        section_address = address + section * 4
                        word = machine.memory.read_word(section_address)
                        formatted_address = Word.from_int(section_address).hex_str(human=True)
                        print(formatted_address, word.hex_str())
                elif command.startswith("disassemble"):
                    _, address_hex = command.split(" ")
                    address = hex_parser.int_from_by7e_hex(address_hex)

                    for fake_address, fake_instruction in machine.glob_instructions(address):
                        formatted_address = Word.from_int(fake_address).hex_str(human=True)
                        print(formatted_address, fake_instruction.human())

                elif command == "web":
                    import app
                    app.routes.override_app(machine)
                    app.app.run()

                elif command == "help":
                    print(help_str)

                else:
                    print("Unknown command:", command)
                command = input("> ").strip()

        machine.run(instruction)
        instruction = machine.next_instruction()

    # print("".join([ str(char) for char in machine.stdout ]))
    print("".join([ chr(char.int_value) for char in machine.stdout ]))

help_str = """
debug
continue
step
registers
print {address | register}
memory {address}
disassemble {address}
web
"""


if __name__ == "__main__":
    # python run.py chall2.exe --input 0x61 --input 0x62 --input 0x64 --input 0x68 --input 0x65 --input 0x71 --input 0x26 --input 0x29 --input 0x3d --input 0x45 --input 0x7c --input 0x79 --input 0x79 --input 0x2a --input 0x38 --input 0x67 --input 0x25 --input 0x20 --input 0x1 --input 0x7f --input 0x5 --input 0x30 --input 0x38 --input 0x4d --input 0x60 --input 0x2b --input 0x12 --input 0x5b
    run()
