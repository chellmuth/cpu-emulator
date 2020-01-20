import disassembler
from byte_stream import BitStream
from core import Byte, Flag, MachineUpdate, Register, Word

class Memory:
    size = 500
    def __init__(self):
        assert self.size % 4 == 0

        self.memory = [
            Byte(0b0) for _ in range(self.size)
        ]

    def write_byte(self, address_word, byte):
        self.memory[address_word.int_value()] = byte

    def write_word(self, address_word, word):
        address = address_word.int_value()

        self.memory[address + 0] = word.byte1
        self.memory[address + 1] = word.byte2
        self.memory[address + 2] = word.byte3
        self.memory[address + 3] = word.byte4

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
        self.registers = [
            Word(Byte(0b0), Byte(0b0), Byte(0b0), Byte(0b0))
            for _ in Register
        ]
        self.registers[Register.sp] = Word.from_int(self.memory.size - 1 - 4)
        self.stdout = [ Byte(72), Byte(101) ]
        self.flags = set()

    def __repr__(self):
        return "\n".join([str(self.registers), str(self.memory)])

    def run(self, instruction):
        update = instruction.run(self)

        self.flags = update.flags

        skip_pc = False
        for register, word in update.registers.items():
            self.registers[register] = word

            if register == Register.pc:
                skip_pc = True

        for address, value in update.memory.items():
            if value.size == 1:
                self.memory.write_byte(address, value)
            elif value.size == 4:
                self.memory.write_word(address, value)
            else: raise ValueError

        if update.stdout is not None:
            self.stdout.append(update.stdout)

        if not skip_pc:
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
