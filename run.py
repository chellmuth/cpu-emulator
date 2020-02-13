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
def run(filename, break_):
    print(breakpoint)
    orc = orc_parser.parse(filename)

    machine = emulator.Machine()

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
    run()
