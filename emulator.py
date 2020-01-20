from dataclasses import dataclass
from typing import Dict, Set

from core import Byte, Word, Flag, Register
from ops.add import add
from ops.bitwise_or import bitwise_or

@dataclass
class MachineUpdate:
    registers: Dict[Register, Word]
    flags: Set[Flag]

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
