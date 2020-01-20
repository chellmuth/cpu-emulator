import instruction_base
from core import Flag, MachineUpdate, Register, Word

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

class JumpRelativeLessThanRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("JLT", value_register)

    def run(self, machine):
        if (Flag.SF in machine.flags) == (Flag.OF in machine.flags):
            return MachineUpdate()

        current = machine.registers[Register.pc].int_value()
        offset = machine.registers[self.value_register].int_value()
        updated_pc = Word.from_int(current + offset + self.size)

        return MachineUpdate(
            registers={
                Register.pc: updated_pc,
            }
        )

class JumpRelativeLessThanConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("JLT", value_word)

    def run(self, machine):
        if (Flag.SF in machine.flags) == (Flag.OF in machine.flags):
            return MachineUpdate()

        current = machine.registers[Register.pc].int_value()
        offset = self.value_word.int_value()
        updated_pc = Word.from_int(current + offset + self.size)

        return MachineUpdate(
            registers={
                Register.pc: updated_pc,
            }
        )

class JumpAbsoluteLessThanRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("ALT", value_register)

    def run(self, machine):
        if (Flag.SF in machine.flags) == (Flag.OF in machine.flags):
            return MachineUpdate()

        return MachineUpdate(
            registers={
                Register.pc: machine.registers[self.value_register],
            }
        )

class JumpAbsoluteLessThanConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("ALT", value_word)

    def run(self, machine):
        if (Flag.SF in machine.flags) == (Flag.OF in machine.flags):
            return MachineUpdate()

        return MachineUpdate(
            registers={
                Register.pc: self.value_word
            }
        )

class JumpRelativeEqualRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("JEQ", value_register)

    def run(self, machine):
        if Flag.ZF not in machine.flags:
            return MachineUpdate()

        current = machine.registers[Register.pc].int_value()
        offset = machine.registers[self.value_register].int_value()
        updated_pc = Word.from_int(current + offset + self.size)

        return MachineUpdate(
            registers={
                Register.pc: updated_pc,
            }
        )

class JumpRelativeEqualConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("JEQ", value_word)

    def run(self, machine):
        if Flag.ZF not in machine.flags:
            return MachineUpdate()

        current = machine.registers[Register.pc].int_value()
        offset = self.value_word.int_value()
        updated_pc = Word.from_int(current + offset + self.size)

        return MachineUpdate(
            registers={
                Register.pc: updated_pc,
            }
        )

class JumpAbsoluteEqualRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("AEQ", value_register)

    def run(self, machine):
        if Flag.ZF not in machine.flags:
            return MachineUpdate()

        return MachineUpdate(
            registers={
                Register.pc: machine.registers[self.value_register],
            }
        )

class JumpAbsoluteEqualConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("AEQ", value_word)

    def run(self, machine):
        if Flag.ZF not in machine.flags:
            return MachineUpdate()

        return MachineUpdate(
            registers={
                Register.pc: self.value_word
            }
        )
