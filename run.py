import click

import emulator
import orc_parser
from core import Byte, Register, Word

class HexIntParamType(click.ParamType):
    name = "hexint"

    def convert(self, value, param, ctx):
        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
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
    print(breakpoint)
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
        if machine.registers[Register.pc].int_value() == break_:
            breakpoint()

        print(machine.registers[Register.pc].hex_str(), instruction.human())
        machine.run(instruction)
        instruction = machine.next_instruction()

    # print("".join([ str(char) for char in machine.stdout ]))
    print("".join([ chr(char.int_value) for char in machine.stdout ]))



if __name__ == "__main__":
    # python run.py chall2.exe --input 0x61 --input 0x62 --input 0x64 --input 0x68 --input 0x65 --input 0x71 --input 0x26 --input 0x29 --input 0x3d --input 0x45 --input 0x7c --input 0x79 --input 0x79 --input 0x2a --input 0x38 --input 0x67 --input 0x25 --input 0x20 --input 0x1 --input 0x7f --input 0x5 --input 0x30 --input 0x38 --input 0x4d --input 0x60 --input 0x2b --input 0x12 --input 0x5b
    run()
