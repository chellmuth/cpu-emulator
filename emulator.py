from dataclasses import dataclass, field
from typing import Dict, Set

from core import Byte, Word, Flag, Register

@dataclass
class MachineUpdate:
    registers: Dict[Register, Word] = field(default_factory=dict)
    memory: Dict[Word, Word] = field(default_factory=dict)
    flags: Set[Flag] = field(default_factory=set)

class Machine:
    def __init__(self):
        self.memory = {}
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
            self.memory[address] = word.low_byte()
