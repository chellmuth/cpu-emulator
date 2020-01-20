import instruction_base
from core import Register, Word
from emulator import MachineUpdate

class JumpRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("JMP", value_register)

    def run(self, machine):
        current = machine.registers[Register.pc].int_value()
        offset = machine.registers[self.value_register].int_value()

        return MachineUpdate(
            registers={
                Register.pc: Word.from_int(current + offset),
            }
        )

class JumpConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("JMP", value_word)

    def run(self, machine):
        current = machine.registers[Register.pc].int_value()
        offset = self.value_word.int_value()

        return MachineUpdate(
            registers={
                Register.pc: Word.from_int(current + offset),
            }
        )
