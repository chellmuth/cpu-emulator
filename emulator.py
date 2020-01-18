from core import Byte, Flag, Register
from ops.add import add

class Machine:
    def __init__(self):
        self.registers = [ Byte(0b0) for _ in Register ]
        self.flags = [ Byte(0b0) for _ in Flag ]

    def __repr__(self):
        return str(self.registers)

    def add_register(self, dest, src):
        result, flags = add(self.registers[src], self.registers[dest])

        self.registers[dest] = result
        self.flags = flags

    def add_constant(self, dest, constant):
        result, flags = add(self.registers[dest], constant)

        self.registers[dest] = result
        self.flags = flags

class Opcode:
    AddRegister = Byte(0b0100000)
    AddConstant = Byte(0b0110000)

if __name__ == "__main__":
    machine = Machine()

    instructions = [
        (Byte(0b0110000), Register.rc, Byte(0b1)),
        (Byte(0b0110000), Register.rd, Byte(0b1000)),
        (Byte(0b0100000), Register.rd, Register.rc),
    ]

    for instruction in instructions:
        opcode, arg1, arg2 = instruction
        if opcode == Opcode.AddRegister:
            machine.add_register(arg1, arg2)
        elif opcode == Opcode.AddConstant:
            machine.add_constant(arg1, arg2)

    print(machine)
