import instruction_base
from core import Register, Word
from emulator import MachineUpdate

class JumpRelativeRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("JMP", value_register)

    def run(self, machine):
        current = machine.registers[Register.pc].int_value()
        offset = machine.registers[self.value_register].int_value()

        return MachineUpdate(
            registers={
                Register.pc: Word.from_int(current + offset + self.size),
            }
        )

class JumpRelativeConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("JMP", value_word)

    def run(self, machine):
        current = machine.registers[Register.pc].int_value()
        offset = self.value_word.int_value()

        return MachineUpdate(
            registers={
                Register.pc: Word.from_int(current + offset + self.size),
            }
        )

class JumpAbsoluteRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("AMP", value_register)

    def run(self, machine):
        return MachineUpdate(
            registers={
                Register.pc: machine.registers[self.value_register],
            }
        )

class JumpAbsoluteConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("AMP", value_word)

    def run(self, machine):
        return MachineUpdate(
            registers={
                Register.pc: self.value_word
            }
        )
