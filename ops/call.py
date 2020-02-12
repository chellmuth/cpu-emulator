import instruction_base
from core import MachineUpdate, Register, Word

class CallRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("CAL", value_register)

    def run(self, machine):
        return_pointer = machine.registers[Register.pc].incremented(self.size)
        increment_amount = machine.registers[self.value_register]

        return MachineUpdate(
            memory={
                machine.registers[Register.sp]: return_pointer
            },
            registers={
                Register.pc: machine.registers[Register.pc].incremented(increment_amount),
                Register.sp: machine.registers[Register.sp].incremented(-4)
            }
        )

class CallConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("CAL", value_word)

    def run(self, machine):
        return_pointer = machine.registers[Register.pc].incremented(self.size)
        increment_amount = self.value_word.int_value()

        return MachineUpdate(
            memory={
                machine.registers[Register.sp]: return_pointer
            },
            registers={
                Register.pc: machine.registers[Register.pc].incremented(increment_amount),
                Register.sp: machine.registers[Register.sp].incremented(-4)
            }
        )

class CallAbsoluteRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("AAL", value_register)

    def run(self, machine):
        return_pointer = machine.registers[Register.pc].incremented(self.size)
        updated_pc = self.value_register.incremented(13)

        return MachineUpdate(
            memory={
                machine.registers[Register.sp]: return_pointer
            },
            registers={
                Register.pc: updated_pc,
                Register.sp: machine.registers[Register.sp].incremented(-4)
            }
        )

class CallAbsoluteConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("AAL", value_word)

    def run(self, machine):
        return_pointer = machine.registers[Register.pc].incremented(self.size)
        updated_pc = self.value_word.incremented(13) # todo: spec error

        return MachineUpdate(
            memory={
                machine.registers[Register.sp]: return_pointer
            },
            registers={
                Register.pc: updated_pc,
                Register.sp: machine.registers[Register.sp].incremented(-4)
            }
        )
