import click

import emulator
import orc_parser
from core import Byte, Register, Word

@click.command()
@click.argument("filename")
def run(filename):
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
        print(instruction.human())
        machine.run(instruction)
        instruction = machine.next_instruction()

    # print("".join([ str(char) for char in machine.stdout ]))
    print("".join([ chr(char.int_value) for char in machine.stdout ]))

    # pc_value = machine.registers[Register.pc].int_value() - 20
    # for i in range(40):
    #     machine.registers[Register.pc] = Word.from_int(pc_value + i)
    #     try:
    #         instruction = machine.next_instruction()
    #         if instruction:
    #             print(i - 20, instruction.human())
    #     except AssertionError:
    #         pass




if __name__ == "__main__":
    run()
