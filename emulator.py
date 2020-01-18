from core import Byte, Word, Flag, Register
from ops.add import add

class Machine:
    def __init__(self):
        self.memory = {}
        self.registers = [ Word(Byte(0b0), Byte(0b0), Byte(0b0), Byte(0b0)) for _ in Register ]
        self.flags = set()

    def __repr__(self):
        return "\n".join([str(self.registers), str(self.memory)])

    def add_register(self, dest, src):
        result, flags = add(self.registers[src].low_byte(), self.registers[dest].low_byte())

        self.registers[dest] = Word(result, Byte(0b0), Byte(0b0), Byte(0b0))
        self.flags = flags

    def add_constant(self, dest, constant):
        result, flags = add(self.registers[dest].low_byte(), constant)

        self.registers[dest] = Word(result, Byte(0b0), Byte(0b0), Byte(0b0))
        self.flags = flags

    def store_byte_constant(self, dest, constant):
        self.memory[constant] = self.registers[dest].low_byte()

class Opcode:
    AddRegister = Byte(0b0100000)
    AddConstant = Byte(0b0110000)

    StoreByteConstant = Byte(0b0111010)

if __name__ == "__main__":
    machine = Machine()

    instructions = [
        (Byte(0b0110000), Register.rc, Byte(0b1)),
        (Byte(0b0110000), Register.rd, Byte(0b1000)),
        (Byte(0b0100000), Register.rd, Register.rc),
        (Byte(0b0111010), Register.rd, Word.from_int(1001)),
    ]

    for instruction in instructions:
        opcode, arg1, arg2 = instruction
        if opcode == Opcode.AddRegister:
            machine.add_register(arg1, arg2)
        elif opcode == Opcode.AddConstant:
            machine.add_constant(arg1, arg2)
        elif opcode == Opcode.StoreByteConstant:
            machine.store_byte_constant(arg1, arg2)

    print(machine)
