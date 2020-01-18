from core import Byte, Word, Flag, Register
from ops.add import add
from ops.bitwise_or import bitwise_or

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

    def or_constant(self, dest, constant):
        self.registers[dest] = bitwise_or(self.registers[dest], constant)

    # def or_register(self, dest, src):
    #     self.registers[dest] = bitwise_or(self.registers[dest], self.registers[src])

class Opcode:
    AddRegister = Byte(0b0100000)
    AddConstant = Byte(0b0110000)

    StoreByteConstant = Byte(0b0111010)

    # OrRegister = Byte(0b0100111)
    OrConstant = Byte(0b0110111)

if __name__ == "__main__":
    machine = Machine()

    instructions = [
        (Byte(0b0110000), Register.rc, Byte(0b1)),
        (Byte(0b0110000), Register.rd, Byte(0b1000)),
        (Byte(0b0100000), Register.rd, Register.rc),
        (Byte(0b0111010), Register.rd, Word.from_int(1001)),
        (Byte(0b0110111), Register.ra, Word(Byte(0b0), Byte(0b1), Byte(0b1), Byte(0b1))),
        (Byte(0b0110111), Register.ra, Word(Byte(0b100), Byte(0b0), Byte(0b0), Byte(0b101))),
        (Byte(0b0111010), Register.ra, Word.from_int(100)),
    ]

    for instruction in instructions:
        opcode, arg1, arg2 = instruction
        if opcode == Opcode.AddRegister:
            machine.add_register(arg1, arg2)
        elif opcode == Opcode.AddConstant:
            machine.add_constant(arg1, arg2)
        elif opcode == Opcode.StoreByteConstant:
            machine.store_byte_constant(arg1, arg2)
        elif opcode == Opcode.OrConstant:
            machine.or_constant(arg1, arg2)
        # elif opcode == Opcode.OrRegister:
        #     machine.or_register(arg1, arg2)


    print(machine)
