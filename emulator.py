from dataclasses import dataclass, field
from typing import Dict, Set

from core import Byte, Word, Flag, Register

@dataclass
class MachineUpdate:
    registers: Dict[Register, Word] = field(default_factory=dict)
    memory: Dict[Word, Word] = field(default_factory=dict)
    flags: Set[Flag] = field(default_factory=set)

class Memory:
    def __init__(self):
        self.size = 100
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
