from dataclasses import dataclass, field
from typing import Dict, Set

import disassembler
from byte_stream import BitStream
from core import Byte, Word, Flag, Register

@dataclass
class MachineUpdate:
    registers: Dict[Register, Word] = field(default_factory=dict)
    memory: Dict[Word, Word] = field(default_factory=dict)
    flags: Set[Flag] = field(default_factory=set)
    stdout: int = None

class Memory:
    def __init__(self):
        self.size = 500
        self.memory = [
            Byte(0b0) for _ in range(self.size)
        ]

    def write(self, address, value):
        self.memory[address.int_value()] = value

    def read_byte(self, address):
        return self.memory[address]

    def read_word(self, address):
        return Word(
            self.memory[address + 0],
            self.memory[address + 1],
            self.memory[address + 2],
            self.memory[address + 3],
        )

class Machine:
    def __init__(self):
        self.memory = Memory()
        self.registers = [ Word(Byte(0b0), Byte(0b0), Byte(0b0), Byte(0b0)) for _ in Register ]
        self.stdout = [ Byte(72), Byte(101) ]
        self.flags = set()

    def __repr__(self):
        return "\n".join([str(self.registers), str(self.memory)])

    def run(self, instruction):
        update = instruction.run(self)

        self.flags = update.flags

        for register, word in update.registers.items():
            self.registers[register] = word

        for address, word in update.memory.items():
            self.memory.write(address, word.low_byte())

        if update.stdout is not None:
            self.stdout.append(update.stdout)
            print(self.stdout)

        self.registers[Register.pc].increment(instruction.size)

    def next_instruction(self):
        base_address = self.registers[Register.pc].int_value()
        bin_str = "".join([
            self.memory.read_byte(base_address + offset).bin_str(padded=True)
            for offset in range(6) # max instruction size
        ])
        stream = BitStream(bin_str)
        return disassembler.disassemble_instruction(stream, strict=False)

    def glob_instructions(self, base_address=None):
        if base_address is None:
            base_address = self.registers[Register.pc].int_value()

        failed = False
        instructions = []
        while not failed:
            bin_str = "".join([
                self.memory.read_byte(base_address + offset).bin_str(padded=True)
                for offset in range(6) # max instruction size
            ])
            stream = BitStream(bin_str)
            instruction = disassembler.disassemble_instruction(stream, strict=False)
            if instruction:
                base_address += instruction.size
                instructions.append(instruction)
            else:
                failed = True

        return instructions
