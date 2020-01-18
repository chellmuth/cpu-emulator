from core import Byte, Flag, Register
from ops.add import add

class Machine:
    def __init__(self):
        self.registers = [ Byte(0b0) for _ in Register ]
        self.flags = [ Byte(0b0) for _ in Flag ]

    def __repr__(self):
        return str(self.registers)

    def add_from_register(self, dest, src):
        result, flags = add(self.registers[src], self.registers[dest])

        self.registers[dest] = result
        self.flags = flags

    def add_from_constant(self, dest, constant):
        result, flags = add(self.registers[dest], constant)

        self.registers[dest] = result
        self.flags = flags

if __name__ == "__main__":
    m = Machine()

    m.add_from_constant(Register.rc, Byte(0b1))
    m.add_from_constant(Register.rd, Byte(0b1000))
    m.add_from_register(Register.rd, Register.rc)

    print(m)
